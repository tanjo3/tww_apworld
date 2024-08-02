import asyncio
import time
import traceback
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import dolphin_memory_engine

import Utils
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus, NetworkItem

from .Items import ITEM_TABLE, LOOKUP_ID_TO_NAME
from .Locations import ISLAND_NAME_TO_SALVAGE_BIT, ISLAND_NUMBER_TO_NAME, LOCATION_TABLE, TWWLocation, TWWLocationType

CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Please load a randomized ROM for The Wind Waker. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = (
    "Dolphin connection was lost. Please restart your emulator and make sure The Wind Waker is running."
)
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."


# This address is used to check/set the player's health for DeathLink.
CURR_HEALTH_ADDR = 0x803C4C0A

# These addresses are used for the Moblin's Letter check.
LETTER_BASE_ADDR = 0x803C4C8E
LETTER_OWND_ADDR = 0x803C4C98

# These addresses are used to check flags for locations.
CHARTS_BITFLD_ADDR = 0x803C4CFC
CHESTS_BITFLD_ADDR = 0x803C5380
SWITCHES_BITFLD_ADDR = 0x803C5384
PICKUPS_BITFLD_ADDR = 0x803C5394
SEA_ALT_BITFLD_ADDR = 0x803C4FAC

# The expected index for the next item that should be received. Uses event bits 0x60 and 0x61.
EXPECTED_INDEX_ADDR = 0x803C528C

# These bytes contain the bits whether the player has received the reward for finding a particular Tingle statue.
TINGLE_STATUE_1_ADDR = 0x803C523E  # 0x40 is the bit for Dragon Tingle statue.
TINGLE_STATUE_2_ADDR = 0x803C5249  # 0x0F are the bits for the remaining Tingle statues.

# These addresses contain the current high score for the Bird-Man Contest.
# `FCP_SCORE_LO_ADDR` is are the lower eight bits of the score, `FCP_SCORE_HI_ADDR` are the higher eight bits.
FCP_SCORE_LO_ADDR = 0x803C52D3
FCP_SCORE_HI_ADDR = 0x803C52D4

# This address contains the current stage ID.
CURR_STAGE_ID_ADDR = 0x803C53A4

# This address is used to check the stage name to verify the player is in-game before sending items.
CURR_STAGE_NAME_ADDR = 0x803C9D3C

# This is an array of length 0x10 where each element is a byte and contains item IDs for items to give the player.
# 0xFF represents no item. The array is read and cleared every frame.
GIVE_ITEM_ARRAY_ADDR = 0x803FE884

# This is the address that holds the player's slot name.
# This way, the player does not have to manually authenticate their slot name.
SLOT_NAME_ADDR = 0x803FE8A8

# This address is the start of an array that we use to inform us of which charts lead where.
# The array is of length 49 where each element is two bytes. The index represents the original destination of the chart
# and the value represents the new destination.
# The chart name is inferrable from the original destination of the chart.
CHARTS_MAPPING_ADDR = 0x803FE8E8

# This address contains the most recent spawn ID the player spawned from.
MOST_RECENT_SPAWN_ID_ADDR = 0x803C9D44

# This address contains the most recent room number the player spawned in.
MOST_RECENT_ROOM_NUMBER_ADDR = 0x803C9D46

# Values used to detect exiting onto the highest isle in Cliff Plateau Isles.
# 42. Starting at 1 and going left to right, top to bottom, Cliff Plateau Isles is the 42nd square in the sea stage.
CLIFF_PLATEAU_ISLES_ROOM_NUMBER = 0x2A
CLIFF_PLATEAU_ISLES_HIGHEST_ISLE_SPAWN_ID = 1  # As a note, the lower isle's spawn ID is 2.
# Dummy stage name used to identify the highest isle in Cliff Plateau Isles.
CLIFF_PLATEAU_ISLES_HIGHEST_ISLE_DUMMY_STAGE_NAME = "CliPlaH"

# Data storage key
AP_VISITED_STAGE_NAMES_KEY_FORMAT = "tww_visited_stages_%i"


class TWWCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_dolphin(self):
        """Prints the current Dolphin status to the client."""
        if isinstance(self.ctx, TWWContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")


class TWWContext(CommonContext):
    command_processor = TWWCommandProcessor
    game = "The Wind Waker"
    items_handling = 0b111

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.items_received_2: List[Tuple[NetworkItem, int]] = []
        self.dolphin_sync_task: Optional[asyncio.Task] = None
        self.dolphin_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.last_rcvd_index = -1
        self.has_send_death = False

        # A dictionary that maps salvage locations to their sunken treasure bit.
        self.salvage_locations_map: Dict[str, int] = {}

        # Name of the current stage as read from the game's memory. Sent to trackers whenever its value changes to
        # facilitate automatically switching to the map of the current stage.
        self.current_stage_name: str = ""

        # Set of visited stages. A dictionary (used as a set) of all visited stages is set in the server's data storage
        # and updated when the player visits a new stage for the first time. To track which stages are new, and need to
        # cause the server's data storage to update, the TWW AP Client keeps track of the visited stages in a set.
        # Trackers can request the dictionary from data storage to see which stages the player has visited.
        # Starts off as `None` until it has been read from the server.
        self.visited_stage_names: Union[Set[str], None] = None

        self.len_give_item_array = 0x10

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.auth = None
        self.salvage_locations_map = {}
        self.current_stage_name = ""
        self.visited_stage_names = None
        await super().disconnect(allow_autoreconnect)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TWWContext, self).server_auth(password_requested)
        if not self.auth:
            if self.awaiting_rom:
                return
            self.awaiting_rom = True
            logger.info("Awaiting connection to Dolphin to get player information")
            return
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.items_received_2 = []
            self.last_rcvd_index = -1
            self.update_salvage_locations_map()
            if "death_link" in args["slot_data"]:
                Utils.async_start(self.update_death_link(bool(args["slot_data"]["death_link"])))
            # Request the connected slot's dictionary (used as a set) of visited stages.
            visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
            Utils.async_start(self.send_msgs([{"cmd": "Get", "keys": [visited_stages_key]}]))
        elif cmd == "ReceivedItems":
            if args["index"] >= self.last_rcvd_index:
                self.last_rcvd_index = args["index"]
                for item in args["items"]:
                    self.items_received_2.append((item, self.last_rcvd_index))
                    self.last_rcvd_index += 1
            self.items_received_2.sort(key=lambda v: v[1])
        elif cmd == "Retrieved":
            requested_keys_dict = args["keys"]
            # Read the connected slot's dictionary (used as a set) of visited stages.
            if self.slot is not None:
                visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
                if visited_stages_key in requested_keys_dict:
                    visited_stages = requested_keys_dict[visited_stages_key]
                    # If it has not been set before, the value in the response will be None
                    visited_stage_names = set() if visited_stages is None else set(visited_stages.keys())
                    # If the current stage name is not in the set, send a message to update the dictionary on the
                    # server.
                    current_stage_name = self.current_stage_name
                    if current_stage_name and current_stage_name not in visited_stage_names:
                        visited_stage_names.add(current_stage_name)
                        Utils.async_start(self.update_visited_stages(current_stage_name))
                    self.visited_stage_names = visited_stage_names

    def on_deathlink(self, data: Dict[str, Any]):
        super().on_deathlink(data)
        _give_death(self)

    def run_gui(self):
        from kvui import GameManager

        class TWWManager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = "Archipelago The Wind Waker Client"

        self.ui = TWWManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def update_visited_stages(self, newly_visited_stage_name: str):
        """
        Update the server's data storage of the visited stage names to include the newly visited stage name.
        """
        if self.slot is not None:
            visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
            await self.send_msgs(
                [
                    {
                        "cmd": "Set",
                        "key": visited_stages_key,
                        "default": {},
                        "want_reply": False,
                        "operations": [{"operation": "update", "value": {newly_visited_stage_name: True}}],
                    }
                ]
            )

    def update_salvage_locations_map(self):
        self.salvage_locations_map = {}
        for offset in range(49):
            island_name = ISLAND_NUMBER_TO_NAME[offset + 1]
            salvage_bit = ISLAND_NAME_TO_SALVAGE_BIT[island_name]

            shuffled_island_number = read_short(CHARTS_MAPPING_ADDR + offset * 2)
            shuffled_island_name = ISLAND_NUMBER_TO_NAME[shuffled_island_number]
            salvage_location_name = f"{shuffled_island_name} - Sunken Treasure"

            self.salvage_locations_map[salvage_location_name] = salvage_bit


def read_short(console_address: int) -> int:
    return int.from_bytes(dolphin_memory_engine.read_bytes(console_address, 2), byteorder="big")


def write_short(console_address: int, value: int) -> None:
    dolphin_memory_engine.write_bytes(console_address, value.to_bytes(2, byteorder="big"))


def read_string(console_address: int, strlen: int) -> str:
    return dolphin_memory_engine.read_bytes(console_address, strlen).split(b"\0", 1)[0].decode()


def _give_death(ctx: TWWContext):
    if (
        ctx.slot is not None
        and dolphin_memory_engine.is_hooked()
        and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS
        and check_ingame()
    ):
        ctx.has_send_death = True
        write_short(CURR_HEALTH_ADDR, 0)


def _give_item(ctx: TWWContext, item_name: str) -> bool:
    if not check_ingame() or dolphin_memory_engine.read_byte(CURR_STAGE_ID_ADDR) == 0xFF:
        return False

    item_id = ITEM_TABLE[item_name].item_id

    # Loop through the give item array, placing the item in an empty slot.
    for idx in range(ctx.len_give_item_array):
        slot = dolphin_memory_engine.read_byte(GIVE_ITEM_ARRAY_ADDR + idx)
        if slot == 0xFF:
            dolphin_memory_engine.write_byte(GIVE_ITEM_ARRAY_ADDR + idx, item_id)
            return True

    # Unable to place the item in the array, so return `False`.
    return False


async def give_items(ctx: TWWContext):
    if check_ingame() and dolphin_memory_engine.read_byte(CURR_STAGE_ID_ADDR) != 0xFF:
        # Read the expected index of the player, which is the index of the latest item they've received.
        expected_idx = read_short(EXPECTED_INDEX_ADDR)

        # Loop through items to give.
        for item, idx in ctx.items_received_2:
            # If the index of the item is greater than the expected index of the player, give the player the item.
            if expected_idx <= idx:
                # Attempt to give the item and increment the expected index.
                while not _give_item(ctx, LOOKUP_ID_TO_NAME[item.item]):
                    await asyncio.sleep(0.01)

                # Increment the expected index.
                write_short(EXPECTED_INDEX_ADDR, idx + 1)


async def check_locations(ctx: TWWContext):
    # We check which locations are currently checked on the current stage.
    curr_stage_id = dolphin_memory_engine.read_byte(CURR_STAGE_ID_ADDR)

    # Read in various bitfields for the locations in the current stage.
    charts_bitfield = int.from_bytes(dolphin_memory_engine.read_bytes(CHARTS_BITFLD_ADDR, 8), byteorder="big")
    sea_alt_bitfield = dolphin_memory_engine.read_word(SEA_ALT_BITFLD_ADDR)
    chests_bitfield = dolphin_memory_engine.read_word(CHESTS_BITFLD_ADDR)
    switches_bitfield = int.from_bytes(dolphin_memory_engine.read_bytes(SWITCHES_BITFLD_ADDR, 10), byteorder="big")
    pickups_bitfield = dolphin_memory_engine.read_word(PICKUPS_BITFLD_ADDR)

    for location, data in LOCATION_TABLE.items():
        checked = False

        # Special-case checks
        if data.type == TWWLocationType.SPECL:
            # The flag for "Windfall Island - Maggie - Delivery Reward" is still unknown.
            # However, as a temporary workaround, we can just check if the player had Moblin's letter at some point,
            # but it's no longer in their Delivery Bag.
            if location == "Windfall Island - Maggie - Delivery Reward":
                was_moblins_owned = (dolphin_memory_engine.read_word(LETTER_OWND_ADDR) >> 15) & 1
                dbag_contents = [dolphin_memory_engine.read_byte(LETTER_BASE_ADDR + offset) for offset in range(8)]
                checked = was_moblins_owned and 0x9B not in dbag_contents

            # For Letter from Baito's Mother, we need to check two bytes.
            # 0x1 = Note to Mom sent, 0x2 = Mail sent by Baito's Mother, 0x3 = Mail read by Link
            if location == "Mailbox - Letter from Baito's Mother":
                checked = dolphin_memory_engine.read_byte(data.address) & 0x3 == 0x3

            # For Letter from Grandma, we need to check two bytes.
            # 0x1 = Grandma saved, 0x2 = Mail sent by Grandma, 0x3 = Mail read by Link
            if location == "Mailbox - Letter from Grandma":
                checked = dolphin_memory_engine.read_byte(data.address) & 0x3 == 0x3

            # For the Ankle's reward, we check if the bits for turning all five statues are set.
            # For some reason, the bit for the Dragon Tingle Statue is located in a separate location than the rest.
            if location == "Tingle Island - Ankle - Reward for All Tingle Statues":
                dragon_tingle_statue_rewarded = dolphin_memory_engine.read_byte(TINGLE_STATUE_1_ADDR) & 0x40 == 0x40
                other_tingle_statues_rewarded = dolphin_memory_engine.read_byte(TINGLE_STATUE_2_ADDR) & 0x0F == 0x0F
                checked = dragon_tingle_statue_rewarded and other_tingle_statues_rewarded

            # For the Bird-Man Contest, we check if the high score is greater than 250 yards.
            if location == "Flight Control Platform - Bird-Man Contest - First Prize":
                high_score = dolphin_memory_engine.read_byte(FCP_SCORE_LO_ADDR) + (
                    dolphin_memory_engine.read_byte(FCP_SCORE_HI_ADDR) << 8
                )
                checked = high_score > 250

        # Regular checks
        elif data.stage_id == curr_stage_id:
            if data.type == TWWLocationType.CHART:
                assert location in ctx.salvage_locations_map, f'Location "{location}" salvage bit not set!'
                salvage_bit = ctx.salvage_locations_map[location]
                checked = (charts_bitfield >> salvage_bit) & 1
            elif data.type == TWWLocationType.BOCTO:
                assert data.address is not None
                checked = (read_short(data.address) >> data.bit) & 1
            elif data.type == TWWLocationType.CHEST:
                checked = (chests_bitfield >> data.bit) & 1
            elif data.type == TWWLocationType.SWTCH:
                checked = (switches_bitfield >> data.bit) & 1
            elif data.type == TWWLocationType.PCKUP:
                checked = (pickups_bitfield >> data.bit) & 1
            elif data.type == TWWLocationType.EVENT:
                checked = (dolphin_memory_engine.read_byte(data.address) >> data.bit) & 1
            else:
                raise NotImplementedError(f"Unknown location type: {data.type}")

        # Sea (Alt) chests
        elif curr_stage_id == 0x0 and data.stage_id == 0x1:
            assert data.type == TWWLocationType.CHEST
            checked = (sea_alt_bitfield >> data.bit) & 1

        if checked:
            if data.code is None:
                if not ctx.finished_game:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True
            else:
                ctx.locations_checked.add(TWWLocation.get_apid(data.code))

    # Send the list of newly-checked locations to the server.
    locations_checked = ctx.locations_checked.difference(ctx.checked_locations)
    if locations_checked:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations_checked}])


async def check_current_stage_changed(ctx: TWWContext):
    new_stage_name = read_string(CURR_STAGE_NAME_ADDR, 8)

    # Special handling for the Cliff Plateau Isles Inner Cave exit that exits out onto the sea stage rather than a
    # unique stage.
    if (
        new_stage_name == "sea"
        and dolphin_memory_engine.read_byte(MOST_RECENT_ROOM_NUMBER_ADDR) == CLIFF_PLATEAU_ISLES_ROOM_NUMBER
        and read_short(MOST_RECENT_SPAWN_ID_ADDR) == CLIFF_PLATEAU_ISLES_HIGHEST_ISLE_SPAWN_ID
    ):
        new_stage_name = CLIFF_PLATEAU_ISLES_HIGHEST_ISLE_DUMMY_STAGE_NAME

    current_stage_name = ctx.current_stage_name
    if new_stage_name != current_stage_name:
        ctx.current_stage_name = new_stage_name
        # Send a Bounced message, containing the new stage name, to all trackers connected to the current slot.
        data_to_send = {"tww_stage_name": new_stage_name}
        message = {
            "cmd": "Bounce",
            "slots": [ctx.slot],
            "tags": ["Tracker"],
            "data": data_to_send,
        }
        await ctx.send_msgs([message])

        # If the stage has never been visited before, update the server's data storage to include that the stage has
        # been visited.
        visited_stage_names = ctx.visited_stage_names
        if visited_stage_names is not None and new_stage_name not in visited_stage_names:
            visited_stage_names.add(new_stage_name)
            await ctx.update_visited_stages(new_stage_name)


async def check_alive():
    cur_health = read_short(CURR_HEALTH_ADDR)
    return cur_health > 0


async def check_death(ctx: TWWContext):
    if ctx.slot is not None and check_ingame():
        cur_health = read_short(CURR_HEALTH_ADDR)
        if cur_health <= 0:
            if not ctx.has_send_death and time.time() >= ctx.last_death_link + 3:
                ctx.has_send_death = True
                await ctx.send_death(ctx.player_names[ctx.slot] + " ran out of hearts.")
        else:
            ctx.has_send_death = False


def check_ingame():
    return read_string(CURR_STAGE_NAME_ADDR, 8) not in ["", "sea_T", "Name"]


async def dolphin_sync_task(ctx: TWWContext):
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        try:
            if dolphin_memory_engine.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                if not check_ingame():
                    # Reset give item array while not in game.
                    dolphin_memory_engine.write_bytes(GIVE_ITEM_ARRAY_ADDR, bytes([0xFF] * ctx.len_give_item_array))
                    await asyncio.sleep(0.1)
                    continue
                if ctx.slot is not None:
                    if "DeathLink" in ctx.tags:
                        await check_death(ctx)
                    await give_items(ctx)
                    await check_locations(ctx)
                    await check_current_stage_changed(ctx)
                else:
                    if not ctx.auth:
                        ctx.auth = read_string(SLOT_NAME_ADDR, 0x40)
                    if ctx.awaiting_rom:
                        await ctx.server_auth()
                await asyncio.sleep(0.1)
            else:
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Dolphin...")
                dolphin_memory_engine.hook()
                if dolphin_memory_engine.is_hooked():
                    if dolphin_memory_engine.read_bytes(0x80000000, 6) != b"GZLE99":
                        logger.info(CONNECTION_REFUSED_GAME_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dolphin_memory_engine.un_hook()
                        await asyncio.sleep(5)
                    else:
                        logger.info(CONNECTION_CONNECTED_STATUS)
                        ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                        ctx.locations_checked = set()
                else:
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    await asyncio.sleep(5)
                    continue
        except Exception:
            dolphin_memory_engine.un_hook()
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            await asyncio.sleep(5)
            continue


def main(connect=None, password=None):
    Utils.init_logging("The Wind Waker Client")

    async def _main(connect, password):
        ctx = TWWContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await asyncio.sleep(3)
            await ctx.dolphin_sync_task

    import colorama

    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser()
    args = parser.parse_args()
    main(args.connect, args.password)

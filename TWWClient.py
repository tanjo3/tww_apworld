import asyncio
import time
import traceback
from typing import Any

import Utils
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus, NetworkItem

from .inc.packages import dolphin_memory_engine
from .Items import ITEM_TABLE, LOOKUP_ID_TO_NAME
from .Locations import LOCATION_TABLE, TWWLocationType

CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Please load a randomized ROM for TWW. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = "Dolphin connection was lost. Please restart your emulator and make sure TWW is running."
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."

# We re-purpose the small key counter and dungeon flag bytes for Ganon's Tower for this
EXPECTED_INDEX_ADDR = 0x803C50C8

SPOILS_BASE_ADDR = 0x803C4C7E
BAIT_BASE_ADDR = 0x803C4C86
BAIT_COUNT_BASE_ADDR = 0x803C4CAC
LETTER_BASE_ADDR = 0x803C4C8E
LETTER_OWND_ADDR = 0x803C4C98
CHARTS_BASE_ADDR = 0x803C4CDC

TOTG_RAISED_ADDR = 0x803C524A

PICTO_BOX_IDS = [0x23, 0x26]
BOW_IDS = [0x27, 0x35, 0x36]
SWORD_IDS = [0x38, 0x39, 0x3A, 0x3E]
SHIELD_IDS = [0x3B, 0x3C]
BOTTLE_ADDRS = [0x803C4C52, 0x803C4C53, 0x803C4C54, 0x803C4C55]

WALLET_ADDR = 0x803C4C1A
MAGIC_METER_ADDR_1 = 0x803C4C1B
MAGIC_METER_ADDR_2 = 0x803C4C1C

GIVE_HEALTH_ADDR = 0x803CA764
GIVE_RUPEE_ADDR = 0x803CA768
GIVE_SKS_ADDR = 0x803CA77D

MAX_HEALTH_ADDR = 0x803C4C08
CURR_HEALTH_ADDR = 0x803C4C0A

STAGE_INFO_ADDR = 0x803C4F88
CURR_STAGE_INFO_ADDR = 0x803C5380
CURR_STAGE_ID_ADDR = 0x803C53A4

CHARTS_BITFLD_ADDR = 0x803C4CFC
SEA_ALT_BITFLD_ADDR = 0x803C4FAC

CHESTS_BITFLD_ADDR = 0x803C5380
SWITCHES_BITFLD_ADDR = 0x803C5384
PICKUPS_BITFLD_ADDR = 0x803C5394
CURR_STAGE_SKS_ADDR = 0x803C53A0
CURR_STAGE_DUNGEON_FLAGS_ADDR = 0x803C53A1

PLAYER_X_POS = 0x803E440C


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
        self.awaiting_auth = False
        self.items_received_2: list[tuple[NetworkItem, int]] = []
        self.dolphin_sync_task = None
        self.dolphin_status = CONNECTION_INITIAL_STATUS
        self.last_rcvd_index = -1
        self.has_send_death = False
        self.last_death_link_send = time.time()

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.auth = None
        await super().disconnect(allow_autoreconnect)

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.items_received_2 = []
            self.last_rcvd_index = -1
            if "death_link" in args["slot_data"]:
                Utils.async_start(self.update_death_link(bool(args["slot_data"]["death_link"])))
        if cmd == "ReceivedItems":
            if args["index"] >= self.last_rcvd_index:
                self.last_rcvd_index = args["index"]
                for item in args["items"]:
                    self.items_received_2.append((item, self.last_rcvd_index))
                    self.last_rcvd_index += 1
            self.items_received_2.sort(key=lambda v: v[1])

    def on_deathlink(self, data: dict[str, Any]):
        super().on_deathlink(data)
        _give_death(self)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TWWContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def run_gui(self):
        from kvui import GameManager

        class TWWManager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = "Archipelago The Wind Waker Client"

        self.ui = TWWManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def read_short(console_address: int):
    return int.from_bytes(dolphin_memory_engine.read_bytes(console_address, 2))


def write_short(console_address: int, value: int):
    dolphin_memory_engine.write_bytes(console_address, value.to_bytes(2))


def _count_expected_heart_pieces(ctx: TWWContext):
    heart_pieces, heart_containers = 0, 0
    for item in ctx.items_received:
        if item.item == ITEM_TABLE["Piece of Heart"].code:
            heart_pieces += 1
        elif item.item == ITEM_TABLE["Heart Container"].code:
            heart_containers += 1

    # Player starts with 12 heart pieces in the base randomizer
    starting_heart_pieces = 3 * 4

    return starting_heart_pieces + heart_pieces + heart_containers * 4


def _give_death(ctx: TWWContext):
    if (
        ctx.slot
        and dolphin_memory_engine.is_hooked()
        and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS
        and check_ingame()
    ):
        write_short(CURR_HEALTH_ADDR, 0)


def _give_item(address: int | None, value: int | None, owned_address: int | None, bit_to_set: int | None):
    if address is not None:
        assert value is not None
        dolphin_memory_engine.write_byte(address, value)

    if owned_address is not None:
        assert bit_to_set is not None
        current_value = dolphin_memory_engine.read_byte(owned_address)
        dolphin_memory_engine.write_byte(owned_address, current_value | 1 << bit_to_set)


def _give_spoil(address: int, spoil_id: int):
    # The Spoils Bag has 8 slots. If the given spoil is already owned, increment its counter by one. Otherwise, add the
    # spoil to next available slot.
    for offset in range(8):
        slot = dolphin_memory_engine.read_byte(SPOILS_BASE_ADDR + offset)
        if slot == spoil_id or slot == 0xFF:
            # Set Spoils Bag slot to that spoil type
            dolphin_memory_engine.write_byte(SPOILS_BASE_ADDR + offset, spoil_id)

            # Increment counter for that spoil by 1
            dolphin_memory_engine.write_byte(address, dolphin_memory_engine.read_byte(address) + 1)

            break


def _give_bait(bait_id: int):
    # The Bait Bag has 8 slots. Put the bait in the next available slot and set its count to 3.
    for offset in range(8):
        if dolphin_memory_engine.read_byte(BAIT_BASE_ADDR + offset) == 0xFF:
            # Set Bait Bag slot to that bait type
            dolphin_memory_engine.write_byte(BAIT_BASE_ADDR + offset, bait_id)

            # Set count to 3, even for Hyoi Pears (slot will be set to 0xFF after single use)
            dolphin_memory_engine.write_byte(BAIT_COUNT_BASE_ADDR + offset, 3)

            break


def _give_letter(value: int, bit_to_set: int):
    # Don't give the letter if the player has already received it
    if (dolphin_memory_engine.read_word(LETTER_OWND_ADDR) >> bit_to_set) & 1:
        return

    # The Delivery Bag has 8 slots. Put the item in the next available slot.
    for offset in range(8):
        if dolphin_memory_engine.read_byte(LETTER_BASE_ADDR + offset) == 0xFF:
            dolphin_memory_engine.write_byte(LETTER_BASE_ADDR + offset, value)
            break

    # Also, set the flag that the letter has been owned
    current_value = dolphin_memory_engine.read_word(LETTER_OWND_ADDR)
    dolphin_memory_engine.write_word(LETTER_OWND_ADDR, current_value | 1 << bit_to_set)


def _give_pearl(address: int, value: int, owned_address: int, bit_to_set: int):
    current_value = dolphin_memory_engine.read_byte(address)
    dolphin_memory_engine.write_byte(address, current_value | value)

    current_value = dolphin_memory_engine.read_byte(owned_address)
    dolphin_memory_engine.write_byte(owned_address, current_value | 1 << bit_to_set)

    # Raise TotG if player has all three pearls
    if dolphin_memory_engine.read_byte(address) == 0xD0:
        dolphin_memory_engine.write_byte(TOTG_RAISED_ADDR, 0x40)


def _give_other_dungeon_item(stage_id: int, item_bit: int):
    stage_info_addr = STAGE_INFO_ADDR + 0x24 * stage_id

    # address + 0x21 is the bitfield of dungeon-specific flags for this dungeon
    current_value = dolphin_memory_engine.read_byte(stage_info_addr + 0x21)
    dolphin_memory_engine.write_byte(stage_info_addr + 0x21, current_value | 1 << item_bit)

    # If the player is currently in that dungeon, update current stage bits as well
    curr_stage_id = dolphin_memory_engine.read_byte(CURR_STAGE_ID_ADDR)
    if curr_stage_id == stage_id:
        current_value = dolphin_memory_engine.read_byte(CURR_STAGE_INFO_ADDR + 0x21)
        dolphin_memory_engine.write_byte(CURR_STAGE_INFO_ADDR + 0x21, current_value | 1 << item_bit)


def _give_small_key(stage_id: int):
    stage_info_addr = STAGE_INFO_ADDR + 0x24 * stage_id
    curr_stage_id = dolphin_memory_engine.read_byte(CURR_STAGE_ID_ADDR)

    if curr_stage_id == stage_id:
        # If the player is currently in that dungeon, give the player a small key for that dungeon
        dolphin_memory_engine.write_byte(GIVE_SKS_ADDR, 1)
    else:
        # address + 0x20 is the current number of small keys the dungeon
        current_value = dolphin_memory_engine.read_byte(stage_info_addr + 0x20)
        dolphin_memory_engine.write_byte(stage_info_addr + 0x20, current_value + 1)


def _give_chart(owned_address: int, bit_to_set: int):
    current_value = dolphin_memory_engine.read_word(owned_address)
    dolphin_memory_engine.write_word(owned_address, current_value | 1 << bit_to_set)


def _give_rupees(amount: int):
    dolphin_memory_engine.write_word(GIVE_RUPEE_ADDR, amount)


def _give_heart_pieces(max_hp: int):
    # Ensure max HP is valid
    max_hp = min(max_hp, 20 * 4)

    write_short(MAX_HEALTH_ADDR, max_hp)

    # Full heal the player when they receive a Piece of Heart or Heart Container
    dolphin_memory_engine.write_float(GIVE_HEALTH_ADDR, float(20 * 4))


def _give_item_progressive(address: int, owned_bitfield: int, item_ids: list[int]):
    # Calculate the next amount of the progressive item
    next_amount = dolphin_memory_engine.read_byte(owned_bitfield).bit_length()
    next_amount = min(next_amount, len(item_ids) - 1)

    dolphin_memory_engine.write_byte(address, item_ids[next_amount])
    dolphin_memory_engine.write_byte(owned_bitfield, 1 << next_amount)


def _give_capacities_progressive(maximum_address: int, count_address: int, capacities: list[int]):
    current_max = dolphin_memory_engine.read_byte(maximum_address)
    if current_max == capacities[-1]:
        return

    next_max = capacities[capacities.index(current_max) + 1]
    dolphin_memory_engine.write_byte(maximum_address, next_max)
    dolphin_memory_engine.write_byte(count_address, next_max)


def _give_wallet_progressive():
    # Calculate the next amount of the progressive wallet
    next_amount = dolphin_memory_engine.read_byte(WALLET_ADDR).bit_length()
    next_amount = min(next_amount, 2)

    dolphin_memory_engine.write_byte(WALLET_ADDR, 1 << next_amount)


def _give_bottle_progressive():
    for addr in BOTTLE_ADDRS:
        if dolphin_memory_engine.read_byte(addr) == 0xFF:
            # 0x50 is empty bottle contents
            _give_item(addr, 0x50, None, None)
            break


def _give_item_by_name(ctx: TWWContext, item: str):
    assert item in ITEM_TABLE, f"Unknown item: {item}"

    if check_ingame():
        data = ITEM_TABLE[item]
        match data.type:
            case "Item":
                _give_item(data.address, data.value, data.owned_bitfield, data.bit_to_set)

            case "Spoil":
                _give_spoil(data.address, data.value)

            case "Bait":
                _give_bait(data.value)

            case "Letter":
                _give_letter(data.value, data.bit_to_set)

            case "Pearl":
                _give_pearl(data.address, data.value, data.owned_bitfield, data.bit_to_set)

            case "Prog":
                match item:
                    case "Progressive Sword":
                        _give_item_progressive(data.address, data.owned_bitfield, SWORD_IDS)

                    case "Progressive Shield":
                        _give_item_progressive(data.address, data.owned_bitfield, SHIELD_IDS)

                    case "Progressive Picto Box":
                        _give_item_progressive(data.address, data.owned_bitfield, PICTO_BOX_IDS)

                    case "Progressive Bow":
                        _give_item_progressive(data.address, data.owned_bitfield, BOW_IDS)

                    case "Progressive Magic Meter":
                        _give_capacities_progressive(data.address, data.owned_bitfield, [0, 16, 32])

                    case "Progressive Quiver" | "Progressive Bomb Bag":
                        _give_capacities_progressive(data.address, data.owned_bitfield, [30, 60, 99])

                    case "Progressive Wallet":
                        _give_wallet_progressive()

                    case "Empty Bottle":
                        _give_bottle_progressive()

            case "Chart":
                _give_chart(data.owned_bitfield, data.bit_to_set)

            case "Rupee":
                _give_rupees(data.value)

            case "Heart":
                _give_heart_pieces(_count_expected_heart_pieces(ctx))

            case "BKey" | "Map" | "Compass":
                _give_other_dungeon_item(data.value, data.bit_to_set)

            case "SKey":
                _give_small_key(data.value)

            case _:
                raise Exception(f"Unknown item type: {data.type}")


async def give_items(ctx: TWWContext):
    if check_ingame():
        expected_idx = read_short(EXPECTED_INDEX_ADDR)
        for item, idx in ctx.items_received_2:
            if expected_idx <= idx:
                item_name = LOOKUP_ID_TO_NAME[item.item]
                _give_item_by_name(ctx, item_name)
                write_short(EXPECTED_INDEX_ADDR, idx + 1)
                # await asyncio.sleep(0.01)  # wait a bit for values to update


async def check_locations(ctx: TWWContext):
    # We check which locations are currently checked on the current stage
    curr_stage_id = dolphin_memory_engine.read_byte(CURR_STAGE_ID_ADDR)

    # Read in various bitfields for the locations in the current stage
    charts_bitfield = int.from_bytes(dolphin_memory_engine.read_bytes(CHARTS_BITFLD_ADDR, 8))
    sea_alt_bitfield = dolphin_memory_engine.read_word(SEA_ALT_BITFLD_ADDR)
    chests_bitfield = dolphin_memory_engine.read_word(CHESTS_BITFLD_ADDR)
    switches_bitfield = int.from_bytes(dolphin_memory_engine.read_bytes(SWITCHES_BITFLD_ADDR, 10))
    pickups_bitfield = dolphin_memory_engine.read_word(PICKUPS_BITFLD_ADDR)

    for location, data in LOCATION_TABLE.items():
        checked = False

        # Special-case checks
        if data.type == TWWLocationType.SPECL:
            if location == "Outset Island - Orca - Give 10 Knight's Crests":
                checked = (dolphin_memory_engine.read_byte(0x803C5237) >> 5) & 1
            if location == "Windfall Island - Chu Jelly Juice Shop - Give 15 Green Chu Jelly":
                checked = (dolphin_memory_engine.read_byte(0x803C5239) >> 2) & 1
            if location == "Windfall Island - Chu Jelly Juice Shop - Give 15 Blue Chu Jelly":
                checked = (dolphin_memory_engine.read_byte(0x803C5239) >> 1) & 1
            if location == "Windfall Island - Battlesquid - First Prize":
                checked = (dolphin_memory_engine.read_byte(0x803C532A) >> 0) & 1
            if location == "Windfall Island - Battlesquid - Second Prize":
                checked = (dolphin_memory_engine.read_byte(0x803C532A) >> 1) & 1
            if location == "Windfall Island - Battlesquid - Under 20 Shots Prize":
                checked = (dolphin_memory_engine.read_byte(0x803C532B) >> 0) & 1
            if location == "Dragon Roost Island - Rito Aerie - Mail Sorting":
                checked = dolphin_memory_engine.read_byte(0x803C52EE) == 0x3
            if location == "The Great Sea - Cyclos":
                checked = (dolphin_memory_engine.read_byte(0x803C5253) >> 4) & 1
            if location == "The Great Sea - Withered Trees":
                checked = (dolphin_memory_engine.read_byte(0x803C525A) >> 5) & 1
            if location == "Rock Spire Isle - Beedle's Special Shop Ship - 500 Rupee Item":
                checked = (dolphin_memory_engine.read_byte(0x803C524C) >> 5) & 1
            if location == "Rock Spire Isle - Beedle's Special Shop Ship - 950 Rupee Item":
                checked = (dolphin_memory_engine.read_byte(0x803C524C) >> 4) & 1
            if location == "Rock Spire Isle - Beedle's Special Shop Ship - 900 Rupee Item":
                checked = (dolphin_memory_engine.read_byte(0x803C524C) >> 3) & 1

        # Regular checks
        elif data.stage_id == curr_stage_id:
            match data.type:
                case TWWLocationType.CHART:
                    checked = (charts_bitfield >> data.bit) & 1
                case TWWLocationType.BOCTO:
                    checked = (read_short(data.address) >> data.bit) & 1
                case TWWLocationType.CHEST:
                    checked = (chests_bitfield >> data.bit) & 1
                case TWWLocationType.SWTCH:
                    checked = (switches_bitfield >> data.bit) & 1
                case TWWLocationType.PCKUP:
                    checked = (pickups_bitfield >> data.bit) & 1

        # Sea (Alt) chests
        elif curr_stage_id == 0x0 and data.stage_id == 0x1:
            assert data.type == TWWLocationType.CHEST
            checked = (sea_alt_bitfield >> data.bit) & 1

        if checked:
            if data.code:
                ctx.locations_checked.add(data.code)
            else:
                if not ctx.finished_game:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True

    # Send the list of newly-checked locations to the server
    locations_checked = ctx.locations_checked.difference(ctx.checked_locations)
    if locations_checked:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations_checked}])


async def check_alive():
    cur_health = read_short(CURR_HEALTH_ADDR)
    return cur_health > 0


async def check_death(ctx: TWWContext):
    cur_health = read_short(CURR_HEALTH_ADDR)
    if cur_health <= 0:
        if not ctx.has_send_death and time.time() >= ctx.last_death_link + 3:
            ctx.has_send_death = True
            await ctx.send_death(ctx.player_names[ctx.slot] + " ran out of hearts.")
    else:
        ctx.has_send_death = False


def check_ingame():
    player_x_pos = dolphin_memory_engine.read_word(PLAYER_X_POS)
    return player_x_pos != 0xC83E0680 and player_x_pos != 0xC83C2F33 and player_x_pos != 0xC6C68C00


async def dolphin_sync_task(ctx: TWWContext):
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        try:
            if dolphin_memory_engine.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                if ctx.server and ctx.slot:
                    if "DeathLink" in ctx.tags:
                        await check_death(ctx)
                    await give_items(ctx)
                    await check_locations(ctx)
                await asyncio.sleep(0.5)
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
                    elif not check_ingame():
                        logger.info(CONNECTION_REFUSED_SAVE_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_SAVE_STATUS
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

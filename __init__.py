import os
from dataclasses import fields
from itertools import chain

from BaseClasses import ItemClassification as IC
from BaseClasses import Region, Tutorial
from Fill import fill_restrictive
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_item_rule
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess

from .Items import ITEM_TABLE, TWWItem
from .Locations import LOCATION_TABLE, TWWFlag, TWWLocation
from .Macros import *
from .Options import TWWOptions
from .Regions import *
from .Rules import set_rules


def run_client():
    print("Running TWW Client")
    from .TWWClient import main  # lazy import

    launch_subprocess(main, name="WindWakerClient")


components.append(
    Component("TWW Client", func=run_client, component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".aptww"))
)


class TWWWeb(WebWorld):
    theme = "ocean"
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Archipelago The Wind Waker software on your computer.",
            "English",
            "setup_en.md",
            "setup/en",
            ["tanjo3"],
        )
    ]


class TWWWorld(World):
    """
    Legend has it that whenever evil has appeared, a hero named Link has arisen to defeat it. The legend continues on
    the surface of a vast and mysterious sea as Link sets sail in his most epic, awe-inspiring adventure yet. Aided by a
    magical conductor's baton called the Wind Waker, he will face unimaginable monsters, explore puzzling dungeons, and
    meet a cast of unforgettable characters as he searches for his kidnapped sister."""

    game: str = "The Wind Waker"
    options_dataclass = TWWOptions
    options: TWWOptions

    topology_present: bool = True

    item_name_to_id: dict[str, int] = {name: data.code for name, data in ITEM_TABLE.items() if data.code}
    location_name_to_id: dict[str, int] = {name: data.code for name, data in LOCATION_TABLE.items() if data.code}

    item_name_groups = {
        "pearls": {
            "Nayru's Pearl",
            "Din's Pearl",
            "Farore's Pearl",
        },
        "shards": {
            "Triforce Shard 1",
            "Triforce Shard 2",
            "Triforce Shard 3",
            "Triforce Shard 4",
            "Triforce Shard 5",
            "Triforce Shard 6",
            "Triforce Shard 7",
            "Triforce Shard 8",
        },
        "tingle_statues": {
            "Dragon Tingle Statue",
            "Forbidden Tingle Statue",
            "Goddess Tingle Statue",
            "Earth Tingle Statue",
            "Wind Tingle Statue",
        },
    }

    web = TWWWeb()

    def __init__(self, *args, **kwargs):
        super(TWWWorld, self).__init__(*args, **kwargs)

        self.itempool: list[TWWItem] = []
        self.pre_fill_items: list[TWWItem] = []
        self.dungeon_local_item_names: set[str] = set()

    def _gather_dungeon_locations(self, dungeon: str):
        dungeon_regions: dict[str, list[str]] = {
            "DRC": ["Dragon Roost Cavern"],
            "FW": ["Forbidden Woods"],
            "TotG": ["Tower of the Gods"],
            "FF": ["Forsaken Fortress"],
            "ET": ["Earth Temple"],
            "WT": ["Wind Temple"],
        }

        # If miniboss entrances are not shuffled, include the miniboss arena as a dungeon location (for key placement)
        if not self.options.randomize_miniboss_entrances:
            dungeon_regions["FW"].append(f"Forbidden Woods Miniboss Arena")
            dungeon_regions["TotG"].append(f"Tower of the Gods Miniboss Arena")
            dungeon_regions["ET"].append(f"Earth Temple Miniboss Arena")
            dungeon_regions["WT"].append(f"Wind Temple Miniboss Arena")

        unfilled_locations = self.multiworld.get_unfilled_locations(self.player)
        is_dungeon_location = lambda location: location.region in dungeon_regions[dungeon]
        return [location for location in unfilled_locations if is_dungeon_location(location)]

    def _get_access_rule(self, region):
        snake_case_region = region.lower().replace("'", "").replace(" ", "_")
        return f"can_access_{snake_case_region}"

    def _get_locations(self):
        return self.multiworld.get_locations(self.player)

    def _randomize_entrances(self):
        # Copy over the lists of entrances by type
        entrances = [
            DUNGEON_ENTRANCES.copy(),
            MINIBOSS_ENTRANCES.copy(),
            BOSS_ENTRANCES.copy(),
            SECRET_CAVES_ENTRANCES.copy(),
            SECRET_CAVES_INNER_ENTRANCES.copy(),
            FAIRY_FOUNTAIN_ENTRANCES.copy(),
        ]
        exits = [
            DUNGEON_EXITS.copy(),
            MINIBOSS_EXITS.copy(),
            BOSS_EXITS.copy(),
            SECRET_CAVES_EXITS.copy(),
            SECRET_CAVES_INNER_EXITS.copy(),
            FAIRY_FOUNTAIN_EXITS.copy(),
        ]

        # Retrieve the entrance randomization option
        options = [
            self.options.randomize_dungeon_entrances,
            self.options.randomize_secret_cave_entrances,
            self.options.randomize_miniboss_entrances,
            self.options.randomize_boss_entrances,
            self.options.randomize_secret_cave_inner_entrances,
            self.options.randomize_fairy_fountain_entrances,
        ]

        entrance_exit_pairs: list[tuple[Region, Region]] = []
        if self.options.mix_entrances == "mix_dungeons":
            # Flatten the lists of entrances/exits into two lists
            all_entrances = list(chain.from_iterable(entrances))
            all_exits = list(chain.from_iterable(exits))

            # Shuffle both lists
            self.multiworld.random.shuffle(all_entrances)
            self.multiworld.random.shuffle(all_exits)

            for entrance, exit in zip(all_entrances, all_exits):
                entrance_exit_pairs.append((self.get_region(entrance), self.get_region(exit)))
        else:
            # Connect entrances to exits of the same type
            for option, entrance_group, exit_group in zip(options, entrances, exits):
                # If the entrance group is randomized, shuffle their order
                if option:
                    self.multiworld.random.shuffle(entrance_group)
                    self.multiworld.random.shuffle(exit_group)

                for entrance, exit in zip(entrance_group, exit_group):
                    entrance_exit_pairs.append((self.get_region(entrance), self.get_region(exit)))

        # TODO: verify that entrance randomization resulted in a valid world

        return entrance_exit_pairs

    def _set_nonprogress_locations(self):
        enabled_flags = TWWFlag.ALWAYS

        # Set the flags for progression location by checking player's settings
        if self.options.progression_dungeons:
            enabled_flags |= TWWFlag.DUNGEON
        if self.options.progression_tingle_chests:
            enabled_flags |= TWWFlag.TNGL_CT
        if self.options.progression_dungeon_secrets:
            enabled_flags |= TWWFlag.DG_SCRT
        if self.options.progression_puzzle_secret_caves:
            enabled_flags |= TWWFlag.PZL_CVE
        if self.options.progression_combat_secret_caves:
            enabled_flags |= TWWFlag.CBT_CVE
        if self.options.progression_savage_labyrinth:
            enabled_flags |= TWWFlag.SAVAGE
        if self.options.progression_great_fairies:
            enabled_flags |= TWWFlag.GRT_FRY
        if self.options.progression_short_sidequests:
            enabled_flags |= TWWFlag.SHRT_SQ
        if self.options.progression_long_sidequests:
            enabled_flags |= TWWFlag.LONG_SQ
        if self.options.progression_spoils_trading:
            enabled_flags |= TWWFlag.SPOILS
        if self.options.progression_minigames:
            enabled_flags |= TWWFlag.MINIGME
        if self.options.progression_battlesquid:
            enabled_flags |= TWWFlag.SPLOOSH
        if self.options.progression_free_gifts:
            enabled_flags |= TWWFlag.FREE_GF
        if self.options.progression_platforms_rafts:
            enabled_flags |= TWWFlag.PLTFRMS
        if self.options.progression_submarines:
            enabled_flags |= TWWFlag.SUBMRIN
        if self.options.progression_eye_reef_chests:
            enabled_flags |= TWWFlag.EYE_RFS
        if self.options.progression_big_octos_gunboats:
            enabled_flags |= TWWFlag.BG_OCTO
        if self.options.progression_triforce_charts:
            enabled_flags |= TWWFlag.TRI_CHT
        if self.options.progression_treasure_charts:
            enabled_flags |= TWWFlag.TRE_CHT
        if self.options.progression_expensive_purchases:
            enabled_flags |= TWWFlag.XPENSVE
        if self.options.progression_island_puzzles:
            enabled_flags |= TWWFlag.ISLND_P
        if self.options.progression_misc:
            enabled_flags |= TWWFlag.MISCELL

        for location in self.multiworld.get_locations(self.player):
            # If not all the flags for a location are set, then force that location to have a non-progress item
            if location.flags & enabled_flags != location.flags:
                add_item_rule(
                    location,
                    lambda item: item.classification == IC.useful or item.classification == IC.filler,
                )

    def generate_early(self):
        # Collect dungeon items to place later in their own dungeons, if key-lunacy is off
        if not self.options.keylunacy:
            for item, data in ITEM_TABLE.items():
                if data.type in ["SmallKey", "BigKey", "DungeonMap", "Compass"]:
                    self.dungeon_local_item_names.add(item)

        # If sword mode is Start with Hero's Sword, then send the player a starting sword
        if self.options.sword_mode == "start_with_sword":
            self.options.start_inventory.value["Progressive Sword"] = (
                self.options.start_inventory.value.get("Progressive Sword", 0) + 1
            )

    def create_regions(self):
        # "Menu" is the required starting point
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        # "The Great Sea" region contains all locations not in a randomizable region
        great_sea_region = Region("The Great Sea", self.player, self.multiworld)
        self.multiworld.regions.append(great_sea_region)

        # Add all randomizable regions
        for region in ALL_ENTRANCES + ALL_EXITS:
            self.multiworld.regions.append(Region(region, self.player, self.multiworld))

        # Assign each location to their region
        for location, data in LOCATION_TABLE.items():
            region = self.get_region(data.region)
            region.locations.append(TWWLocation(self.player, location, region, data))

        # Connect the "Menu" region to the "The Great Sea" region
        menu_region.connect(great_sea_region)

        # Connect the dungeon, secret caves, and fairy fountain regions to the "The Great Sea" region
        for entrance in DUNGEON_ENTRANCES + SECRET_CAVES_ENTRANCES + FAIRY_FOUNTAIN_ENTRANCES:
            rule = lambda state, entrance=entrance: getattr(Macros, self._get_access_rule(entrance))(state, self.player)
            great_sea_region.connect(self.get_region(entrance), rule=rule)

        # Connect nested regions with their parent region
        for entrance in MINIBOSS_ENTRANCES + BOSS_ENTRANCES + SECRET_CAVES_INNER_ENTRANCES:
            parent_region_name = entrance.split(" in ")[-1]
            # consider Hyrule Castle and Forsaken Fortress as part of The Great Sea (these regions are not randomizable)
            if parent_region_name in ["Hyrule Castle", "Forsaken Fortress"]:
                parent_region_name = "The Great Sea"
            rule = lambda state, entrance=entrance: getattr(Macros, self._get_access_rule(entrance))(state, self.player)
            self.get_region(parent_region_name).connect(self.get_region(entrance), rule=rule)

        # Randomize entrances to exits, if the option is set
        entrance_exit_pairs = self._randomize_entrances()

        # Connect entrances to exits
        for entrance_region, exit_region in entrance_exit_pairs:
            rule = lambda state, exit=exit_region.name: getattr(Macros, self._get_access_rule(exit))(state, self.player)
            entrance_region.connect(exit_region, rule=rule)

    def create_item(self, item: str) -> TWWItem:
        # TODO: calculate nonprogress items dynamically
        set_non_progress = False
        if not self.options.progression_triforce_charts and item.startswith("Triforce Chart"):
            set_non_progress = True
        if not self.options.progression_treasure_charts and item.startswith("Treasure Chart"):
            set_non_progress = True

        if item in ITEM_TABLE:
            return TWWItem(item, self.player, ITEM_TABLE[item], set_non_progress)
        raise Exception(f"Invalid item name: {item}")

    def pre_fill(self):
        def prefill_state(base_state):
            state = base_state.copy()
            for item in self.get_pre_fill_items():
                self.collect(state, item)
            return state

        self._set_nonprogress_locations()

        # Pre-fill dungeon items
        locations = list(self.multiworld.get_unfilled_locations(self.player))
        self.multiworld.random.shuffle(locations)

        # Set up initial state
        state = CollectionState(self.multiworld)
        for item in self.itempool:
            self.collect(state, item)

        # Place the dungeon items in their own dungeons, if key-lunacy is not enabled
        for dungeon in ["DRC", "FW", "TotG", "FF", "ET", "WT"]:
            dungeon_items = [item for item in self.pre_fill_items if item.name.startswith(dungeon)]
            dungeon_locations = self._gather_dungeon_locations(dungeon)
            self.multiworld.random.shuffle(dungeon_locations)
            fill_restrictive(
                self.multiworld,
                prefill_state(state),
                dungeon_locations,
                dungeon_items,
                single_player_placement=True,
                lock=True,
                allow_excluded=True,
            )

    def create_items(self):
        exclude = [item.name for item in self.multiworld.precollected_items[self.player]]
        for item, data in ITEM_TABLE.items():
            if item == "Victory":
                self.get_location("Defeat Ganondorf").place_locked_item(self.create_item(item))
            else:
                copies_to_place = data.quantity - exclude.count(item)
                for _ in range(copies_to_place):
                    if item in self.dungeon_local_item_names:
                        self.pre_fill_items.append(self.create_item(item))
                    else:
                        self.itempool.append(self.create_item(item))

        self.multiworld.itempool += self.itempool

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def generate_output(self, output_directory: str):
        # Output seed name to seed RNG in randomizer client
        output_file = f"Seed: {self.multiworld.seed_name}\n"

        # Include slot number as well in RNG seed
        output_file += f"Slot: {self.player}\n"
        output_file += "\n\n"

        # Output relevant options to file
        output_file += "Options:\n"
        for field in fields(self.options):
            output_file += f"    {field.name}: {getattr(self.options, field.name).value}\n"
        output_file += "\n\n"

        # Output which item has been placed at each location
        # TODO: revisit once item models are working
        output_file += "Locations:\n"
        locations = self.multiworld.get_locations(self.player)
        for location in locations:
            if location.name != "Defeat Ganondorf":
                output_file += f"    {location.name}: {location.item.name}\n"
        output_file += "\n\n"

        # Output the mapping of entrances to exits
        output_file += "Entrances:\n"
        entrances = self.multiworld.get_entrances(self.player)
        for entrance in entrances:
            if entrance.parent_region.name in ALL_ENTRANCES:
                output_file += f"    {entrance.parent_region.name}: {entrance.connected_region.name}\n"

        # Output the plando details to file
        file_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.aptww")
        with open(file_path, "w") as f:
            f.write(output_file)

    def fill_slot_data(self):
        return {"death_link": self.options.death_link.value}

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
from .Locations import LOCATION_TABLE, VANILLA_DUNGEON_ITEM_LOCATIONS, TWWFlag, TWWLocation
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

        self.vanilla_dungeon_item_names: set[str] = set()
        self.own_dungeon_item_names: set[str] = set()
        self.any_dungeon_item_names: set[str] = set()

    def _get_access_rule(self, region):
        snake_case_region = region.lower().replace("'", "").replace(" ", "_")
        return f"can_access_{snake_case_region}"

    def _get_locations(self):
        return self.multiworld.get_locations(self.player)

    def _get_unfilled_dungeon_locations(self):
        dungeon_regions = ["Dragon Roost Cavern", "Forbidden Woods", "Tower of the Gods", "Earth Temple", "Wind Temple"]

        # If miniboss entrances are not shuffled, include miniboss arenas as a dungeon regions
        if not self.options.randomize_miniboss_entrances:
            dungeon_regions += [
                "Forbidden Woods Miniboss Arena",
                "Tower of the Gods Miniboss Arena",
                "Earth Temple Miniboss Arena",
                "Wind Temple Miniboss Arena",
            ]

        # Forsaken Fortress is an odd dungeon as it exists on the Great Sea
        # Simply keep a list of all locations in the dungeon, except the boss Heart Container
        ff_dungeon_locations = [
            "Forsaken Fortress - Phantom Ganon",
            "Forsaken Fortress - Chest Outside Upper Jail Cell",
            "Forsaken Fortress - Chest Inside Lower Jail Cell",
            "Forsaken Fortress - Chest Guarded By Bokoblin",
            "Forsaken Fortress - Chest on Bed",
        ]

        unfilled_locations = self.multiworld.get_unfilled_locations(self.player)
        is_dungeon_location = (
            lambda location: location.name in ff_dungeon_locations or location.region in dungeon_regions
        )
        return [location for location in unfilled_locations if is_dungeon_location(location)]

    def _get_unfilled_locations_in_dungeon(self, dungeon: str):
        dungeon_regions: dict[str, str] = {
            "DRC": "Dragon Roost Cavern",
            "FW": "Forbidden Woods",
            "TotG": "Tower of the Gods",
            "FF": "Forsaken Fortress",
            "ET": "Earth Temple",
            "WT": "Wind Temple",
        }

        unfilled_locations = self._get_unfilled_dungeon_locations()
        is_dungeon_location = lambda location: location.name.startswith(dungeon_regions[dungeon])
        return [location for location in unfilled_locations if is_dungeon_location(location)]

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
                entrance_region = self.multiworld.get_region(entrance, self.player)
                exit_region = self.multiworld.get_region(exit, self.player)
                entrance_exit_pairs.append((entrance_region, exit_region))
        else:
            # Connect entrances to exits of the same type
            for option, entrance_group, exit_group in zip(options, entrances, exits):
                # If the entrance group is randomized, shuffle their order
                if option:
                    self.multiworld.random.shuffle(entrance_group)
                    self.multiworld.random.shuffle(exit_group)

                for entrance, exit in zip(entrance_group, exit_group):
                    entrance_region = self.multiworld.get_region(entrance, self.player)
                    exit_region = self.multiworld.get_region(exit, self.player)
                    entrance_exit_pairs.append((entrance_region, exit_region))

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
        # Handle randomization options for dungeon items
        for item, data in ITEM_TABLE.items():
            match data.type:
                case "Map" | "Compass":
                    if self.options.randomize_mapcompass == "startwith":
                        self.options.start_inventory.value[item] = data.quantity
                    elif self.options.randomize_mapcompass == "vanilla":
                        self.vanilla_dungeon_item_names.add(item)
                    elif self.options.randomize_mapcompass == "dungeon":
                        self.own_dungeon_item_names.add(item)
                    elif self.options.randomize_mapcompass == "any_dungeon":
                        self.any_dungeon_item_names.add(item)
                    elif self.options.randomize_mapcompass == "local":
                        self.options.local_items.value.add(item)

                case "SKey":
                    if self.options.randomize_smallkeys == "startwith":
                        self.options.start_inventory.value[item] = data.quantity
                    elif self.options.randomize_smallkeys == "vanilla":
                        self.vanilla_dungeon_item_names.add(item)
                    elif self.options.randomize_smallkeys == "dungeon":
                        self.own_dungeon_item_names.add(item)
                    elif self.options.randomize_smallkeys == "any_dungeon":
                        self.any_dungeon_item_names.add(item)
                    elif self.options.randomize_smallkeys == "local":
                        self.options.local_items.value.add(item)

                case "BKey":
                    if self.options.randomize_bigkeys == "startwith":
                        self.options.start_inventory.value[item] = data.quantity
                    elif self.options.randomize_bigkeys == "vanilla":
                        self.vanilla_dungeon_item_names.add(item)
                    elif self.options.randomize_bigkeys == "dungeon":
                        self.own_dungeon_item_names.add(item)
                    elif self.options.randomize_bigkeys == "any_dungeon":
                        self.any_dungeon_item_names.add(item)
                    elif self.options.randomize_bigkeys == "local":
                        self.options.local_items.value.add(item)

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
            region = self.multiworld.get_region(data.region, self.player)
            region.locations.append(TWWLocation(self.player, location, region, data))

        # Connect the "Menu" region to the "The Great Sea" region
        menu_region.connect(great_sea_region)

        # Connect the dungeon, secret caves, and fairy fountain regions to the "The Great Sea" region
        for entrance in DUNGEON_ENTRANCES + SECRET_CAVES_ENTRANCES + FAIRY_FOUNTAIN_ENTRANCES:
            rule = lambda state, entrance=entrance: getattr(Macros, self._get_access_rule(entrance))(state, self.player)
            connecting_region = self.multiworld.get_region(entrance, self.player)
            great_sea_region.connect(connecting_region, rule=rule)

        # Connect nested regions with their parent region
        for entrance in MINIBOSS_ENTRANCES + BOSS_ENTRANCES + SECRET_CAVES_INNER_ENTRANCES:
            parent_region_name = entrance.split(" in ")[-1]
            # consider Hyrule Castle and Forsaken Fortress as part of The Great Sea (these regions are not randomizable)
            if parent_region_name in ["Hyrule Castle", "Forsaken Fortress"]:
                parent_region_name = "The Great Sea"
            rule = lambda state, entrance=entrance: getattr(Macros, self._get_access_rule(entrance))(state, self.player)
            parent_region = self.multiworld.get_region(parent_region_name, self.player)
            connecting_region = self.multiworld.get_region(entrance, self.player)
            parent_region.connect(connecting_region, rule=rule)

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
        # Set nonprogress location from options
        self._set_nonprogress_locations()

        # Set up initial all_state
        all_state_base = CollectionState(self.multiworld)
        for item in self.itempool:
            self.collect(all_state_base, item)
        for item in self.get_pre_fill_items():
            self.collect(all_state_base, item)
        all_state_base.sweep_for_events()

        # First, place small keys in their own dungeon
        for dungeon in ["DRC", "FW", "TotG", "FF", "ET", "WT"]:
            own_dungeon_small_keys = [
                item
                for item in self.pre_fill_items
                if item.type == "SKey" and item.name in self.own_dungeon_item_names and item.name.startswith(dungeon)
            ]
            dungeon_locations = self._get_unfilled_locations_in_dungeon(dungeon)
            self.multiworld.random.shuffle(dungeon_locations)
            fill_restrictive(
                self.multiworld,
                all_state_base,
                dungeon_locations,
                own_dungeon_small_keys,
                single_player_placement=True,
                lock=True,
                allow_excluded=True,
            )

        # Next, place big keys in their own dungeon
        for dungeon in ["DRC", "FW", "TotG", "FF", "ET", "WT"]:
            own_dungeon_big_keys = [
                item
                for item in self.pre_fill_items
                if item.type == "BKey" and item.name in self.own_dungeon_item_names and item.name.startswith(dungeon)
            ]
            dungeon_locations = self._get_unfilled_locations_in_dungeon(dungeon)
            self.multiworld.random.shuffle(dungeon_locations)
            fill_restrictive(
                self.multiworld,
                all_state_base,
                dungeon_locations,
                own_dungeon_big_keys,
                single_player_placement=True,
                lock=True,
                allow_excluded=True,
            )

        # Next, place small keys in any dungeon
        any_dungeon_small_keys = [
            item for item in self.pre_fill_items if item.type == "SKey" and item.name in self.any_dungeon_item_names
        ]
        all_dungeon_locations = self._get_unfilled_dungeon_locations()
        self.multiworld.random.shuffle(all_dungeon_locations)
        fill_restrictive(
            self.multiworld,
            all_state_base,
            all_dungeon_locations,
            any_dungeon_small_keys,
            single_player_placement=True,
            lock=True,
            allow_excluded=True,
        )

        # Next, place big keys in any dungeon
        any_dungeon_big_keys = [
            item for item in self.pre_fill_items if item.type == "BKey" and item.name in self.any_dungeon_item_names
        ]
        all_dungeon_locations = self._get_unfilled_dungeon_locations()
        self.multiworld.random.shuffle(all_dungeon_locations)
        fill_restrictive(
            self.multiworld,
            all_state_base,
            all_dungeon_locations,
            any_dungeon_big_keys,
            single_player_placement=True,
            lock=True,
            allow_excluded=True,
        )

        # Now, place dungeon maps and compasses in their own dungeons
        for dungeon in ["DRC", "FW", "TotG", "FF", "ET", "WT"]:
            own_dungeon_mapcompass = [
                item
                for item in self.pre_fill_items
                if item.type in ["Map", "Compass"]
                and item.name in self.own_dungeon_item_names
                and item.name.startswith(dungeon)
            ]
            dungeon_locations = self._get_unfilled_locations_in_dungeon(dungeon)
            self.multiworld.random.shuffle(dungeon_locations)
            fill_restrictive(
                self.multiworld,
                all_state_base,
                dungeon_locations,
                own_dungeon_mapcompass,
                single_player_placement=True,
                lock=True,
                allow_excluded=True,
            )

        # Finally, place dungeon maps and compasses in any dungeon
        any_dungeon_mapcompass = [
            item
            for item in self.pre_fill_items
            if item.type in ["Map", "Compass"] and item.name in self.any_dungeon_item_names
        ]
        all_dungeon_locations = self._get_unfilled_dungeon_locations()
        self.multiworld.random.shuffle(all_dungeon_locations)
        fill_restrictive(
            self.multiworld,
            all_state_base,
            all_dungeon_locations,
            any_dungeon_mapcompass,
            single_player_placement=True,
            lock=True,
            allow_excluded=True,
        )

    def create_items(self):
        exclude = [item.name for item in self.multiworld.precollected_items[self.player]]
        for item, data in ITEM_TABLE.items():
            if item == "Victory":
                # Victory item is always on Defeat Ganondorf location
                self.multiworld.get_location("Defeat Ganondorf", self.player).place_locked_item(self.create_item(item))
            elif item in self.vanilla_dungeon_item_names:
                # Place desired vanilla dungeon item in their vanilla locations
                for location in VANILLA_DUNGEON_ITEM_LOCATIONS[item]:
                    self.multiworld.get_location(location, self.player).place_locked_item(self.create_item(item))
            else:
                copies_to_place = data.quantity - exclude.count(item)
                for _ in range(copies_to_place):
                    if item in self.own_dungeon_item_names or item in self.any_dungeon_item_names:
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
                if location.item:
                    output_file += f'    {location.name}: "{location.item.name}"\n'
                else:
                    output_file += f'    {location.name}: "Nothing"\n'
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

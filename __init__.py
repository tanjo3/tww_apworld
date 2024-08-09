import copy
import os
from dataclasses import fields
from typing import ClassVar, Dict, List, Set, Tuple, Type

import yaml

from BaseClasses import ItemClassification as IC
from BaseClasses import LocationProgressType, Region, Tutorial
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_item_rule
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess

from . import Macros
from .Dungeons import Dungeon, create_dungeons
from .Entrances import (
    ALL_ENTRANCES,
    ALL_EXITS,
    BOSS_ENTRANCES,
    BOSS_EXIT_TO_DUNGEON,
    DUNGEON_ENTRANCES,
    FAIRY_FOUNTAIN_ENTRANCES,
    MINIBOSS_ENTRANCES,
    MINIBOSS_EXIT_TO_DUNGEON,
    SECRET_CAVE_ENTRANCES,
    SECRET_CAVE_INNER_ENTRANCES,
    EntranceRandomizer,
)
from .ItemPool import generate_itempool
from .Items import ISLAND_NUMBER_TO_CHART_NAME, ITEM_TABLE, TWWItem, item_name_groups
from .Locations import (
    DUNGEON_NAMES,
    ISLAND_NUMBER_TO_NAME,
    LOCATION_TABLE,
    TWWFlag,
    TWWLocation,
    split_location_name_by_zone,
)
from .Options import TWWOptions, tww_option_groups
from .Rules import set_rules

VERSION: Tuple[int, int, int] = (2, 5, 0)


def run_client():
    print("Running The Wind Waker Client")
    from .TWWClient import main  # lazy import

    launch_subprocess(main, name="TheWindWakerClient")


components.append(
    Component(
        "The Wind Waker Client",
        func=run_client,
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".aptww"),
    )
)


class TWWWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Archipelago The Wind Waker software on your computer.",
            "English",
            "setup_en.md",
            "setup/en",
            ["tanjo3", "Lunix"],
        )
    ]
    theme = "ocean"
    option_groups = tww_option_groups
    rich_text_options_doc = True


class TWWWorld(World):
    """
    Legend has it that whenever evil has appeared, a hero named Link has arisen to defeat it. The legend continues on
    the surface of a vast and mysterious sea as Link sets sail in his most epic, awe-inspiring adventure yet. Aided by a
    magical conductor's baton called the Wind Waker, he will face unimaginable monsters, explore puzzling dungeons, and
    meet a cast of unforgettable characters as he searches for his kidnapped sister."""

    options_dataclass = TWWOptions
    options: TWWOptions

    game: ClassVar[str] = "The Wind Waker"
    topology_present: bool = True

    item_name_to_id: ClassVar[Dict[str, int]] = {
        name: TWWItem.get_apid(data.code) for name, data in ITEM_TABLE.items() if data.code is not None
    }
    location_name_to_id: ClassVar[Dict[str, int]] = {
        name: TWWLocation.get_apid(data.code) for name, data in LOCATION_TABLE.items() if data.code is not None
    }

    item_name_groups: ClassVar[Dict[str, Set[str]]] = item_name_groups

    required_client_version: Tuple[int, int, int] = (0, 5, 0)

    web: ClassVar[TWWWeb] = TWWWeb()

    create_items = generate_itempool

    set_rules = set_rules

    def __init__(self, *args, **kwargs):
        self.dungeon_local_item_names: Set[str] = set()
        self.dungeon_specific_item_names: Set[str] = set()
        self.dungeons: Dict[str, Dungeon] = {}

        self.required_boss_item_locations: List[str] = []
        self.required_dungeons: List[str] = []
        self.required_bosses: List[str] = []
        self.banned_locations: List[str] = []
        self.banned_dungeons: List[str] = []
        self.banned_bosses: List[str] = []

        self.island_number_to_chart_name = copy.deepcopy(ISLAND_NUMBER_TO_CHART_NAME)

        super(TWWWorld, self).__init__(*args, **kwargs)

        self.entrances = EntranceRandomizer(self)

    def _randomize_charts(self):
        # This code comes straight from the base randomizer's chart randomizer.

        original_item_names = list(self.island_number_to_chart_name.values())

        # Shuffles the list of island numbers.
        # The shuffled island numbers determine which sector each chart points to.
        shuffled_island_numbers = list(self.island_number_to_chart_name.keys())
        self.multiworld.random.shuffle(shuffled_island_numbers)

        for original_item_name in original_item_names:
            shuffled_island_number = shuffled_island_numbers.pop()
            self.island_number_to_chart_name[shuffled_island_number] = original_item_name

            # Properly adjust the flags for sunken treasure locations.
            island_name = ISLAND_NUMBER_TO_NAME[shuffled_island_number]
            island_location = self.get_location(f"{island_name} - Sunken Treasure")
            if original_item_name.startswith("Triforce Chart "):
                island_location.flags = TWWFlag.TRI_CHT
            else:
                island_location.flags = TWWFlag.TRE_CHT

    def _randomize_required_bosses(self):
        if not self.options.progression_dungeons:
            raise OptionError("Cannot make bosses required when progression dungeons are disabled.")

        dungeon_names = set(DUNGEON_NAMES)

        # Assert that the user is not including and excluding a dungeon at the same time.
        if len(self.options.included_dungeons.value & self.options.excluded_dungeons.value) != 0:
            raise OptionError("Conflict found in the lists of required and banned dungeons for required bosses mode.")

        # If the user enforces a dungeon location to be priority, consider that when selecting required bosses.
        required_dungeons = self.options.included_dungeons.value
        for location_name in self.options.priority_locations.value:
            dungeon_name, _ = split_location_name_by_zone(location_name)
            if dungeon_name in dungeon_names:
                required_dungeons.add(dungeon_name)

        # Ensure that we aren't prioritizing more dungeon locations than requested number of required bosses.
        num_required_bosses = self.options.num_required_bosses
        if len(required_dungeons) > num_required_bosses:
            raise OptionError("Could not select required bosses to satisfy options set by user.")

        # Ensure that after removing excluded dungeons that we still have enough dungeons to satisfy user options.
        num_remaining = num_required_bosses - len(required_dungeons)
        remaining_dungeon_options = dungeon_names - required_dungeons - self.options.excluded_dungeons.value
        if len(remaining_dungeon_options) < num_remaining:
            raise OptionError("Could not select required bosses to satisfy options set by user.")

        # Finish selecting required bosses.
        required_dungeons.update(self.multiworld.random.sample(list(remaining_dungeon_options), num_remaining))

        # Exclude locations which are not in the dungeon of a required boss.
        banned_dungeons = dungeon_names - required_dungeons
        for location_name, location_data in LOCATION_TABLE.items():
            dungeon_name, _ = split_location_name_by_zone(location_name)
            if dungeon_name in banned_dungeons and TWWFlag.DUNGEON in location_data.flags:
                self.banned_locations.append(location_name)
            elif location_name == "Mailbox - Letter from Orca" and "Forbidden Woods" in banned_dungeons:
                self.banned_locations.append(location_name)
            elif location_name == "Mailbox - Letter from Baito" and "Earth Temple" in banned_dungeons:
                self.banned_locations.append(location_name)
            elif location_name == "Mailbox - Letter from Aryll" and "Forsaken Fortress" in banned_dungeons:
                self.banned_locations.append(location_name)
            elif location_name == "Mailbox - Letter from Tingle" and "Forsaken Fortress" in banned_dungeons:
                self.banned_locations.append(location_name)
        for location_name in self.banned_locations:
            self.get_location(location_name).progress_type = LocationProgressType.EXCLUDED

        # Record the item location names for required bosses.
        self.required_boss_item_locations: List[str] = []
        self.required_bosses: List[str] = []
        self.banned_bosses: List[str] = []
        possible_boss_item_locations = [loc for loc, data in LOCATION_TABLE.items() if TWWFlag.BOSS in data.flags]
        for location_name in possible_boss_item_locations:
            dungeon_name, specific_location_name = split_location_name_by_zone(location_name)
            assert specific_location_name.endswith(" Heart Container")
            boss_name = specific_location_name[: -len(" Heart Container")]

            if dungeon_name in required_dungeons:
                self.required_boss_item_locations.append(location_name)
                self.required_bosses.append(boss_name)
            else:
                self.banned_bosses.append(boss_name)
        self.required_dungeons = list(required_dungeons)
        self.banned_dungeons = list(banned_dungeons)

    def _set_nonprogress_locations(self):
        enabled_flags = TWWFlag.ALWAYS

        # Set the flags for progression location by checking player's settings.
        if self.options.progression_dungeons:
            enabled_flags |= TWWFlag.DUNGEON
            enabled_flags |= TWWFlag.BOSS
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
            # If not all the flags for a location are set, then force that location to have a non-progress item.
            if location.flags & enabled_flags != location.flags:
                location.progress_type = LocationProgressType.EXCLUDED

    def generate_early(self):
        options = self.options

        # Force vanilla dungeon items when dungeons are not progression.
        if not options.progression_dungeons:
            if options.randomize_smallkeys.value > 0:
                options.randomize_smallkeys.value = 1
            if options.randomize_bigkeys.value > 0:
                options.randomize_bigkeys.value = 1
            if options.randomize_mapcompass.value > 0:
                options.randomize_mapcompass.value = 1

        for dungeon_item in ["randomize_smallkeys", "randomize_bigkeys", "randomize_mapcompass"]:
            option = getattr(options, dungeon_item)
            if option == "local":
                options.local_items.value |= self.item_name_groups[option.item_name_group]
            elif option.in_dungeon:
                self.dungeon_local_item_names |= self.item_name_groups[option.item_name_group]
                if option == "dungeon":
                    self.dungeon_specific_item_names |= self.item_name_groups[option.item_name_group]

    create_dungeons = create_dungeons

    def create_regions(world):
        def get_access_rule(region: str) -> str:
            snake_case_region = region.lower().replace("'", "").replace(" ", "_")
            return f"can_access_{snake_case_region}"

        multiworld = world.multiworld
        player = world.player
        options = world.options

        # "Menu" is the required starting point.
        menu_region = Region("Menu", player, multiworld)
        multiworld.regions.append(menu_region)

        # "The Great Sea" region contains all locations not in a randomizable region.
        great_sea_region = Region("The Great Sea", player, multiworld)
        multiworld.regions.append(great_sea_region)

        # Add all randomizable regions.
        for region in ALL_ENTRANCES:
            multiworld.regions.append(Region(region.entrance_name, player, multiworld))
        for region in ALL_EXITS:
            multiworld.regions.append(Region(region.unique_name, player, multiworld))

        # Create the dungeon classes.
        world.create_dungeons()

        # Assign each location to their region.
        for location, data in LOCATION_TABLE.items():
            region = world.get_region(data.region)
            location = TWWLocation(player, location, region, data)

            # Additionally, assign dungeon locations to the appropriate dungeon.
            if region.name in world.dungeons:
                location.dungeon = world.dungeons[region.name]
            elif region.name in MINIBOSS_EXIT_TO_DUNGEON and not options.randomize_miniboss_entrances:
                location.dungeon = world.dungeons[MINIBOSS_EXIT_TO_DUNGEON[region.name]]
            elif region.name in BOSS_EXIT_TO_DUNGEON and not options.randomize_boss_entrances:
                location.dungeon = world.dungeons[BOSS_EXIT_TO_DUNGEON[region.name]]
            elif location.name in [
                "Forsaken Fortress - Phantom Ganon",
                "Forsaken Fortress - Chest Outside Upper Jail Cell",
                "Forsaken Fortress - Chest Inside Lower Jail Cell",
                "Forsaken Fortress - Chest Guarded By Bokoblin",
                "Forsaken Fortress - Chest on Bed",
            ]:
                location.dungeon = world.dungeons["Forsaken Fortress"]
            region.locations.append(location)

        # Connect the "Menu" region to the "The Great Sea" region.
        menu_region.connect(great_sea_region)

        # Connect the dungeon, secret caves, and fairy fountain regions to the "The Great Sea" region.
        for entrance in DUNGEON_ENTRANCES + SECRET_CAVE_ENTRANCES + FAIRY_FOUNTAIN_ENTRANCES:
            rule = lambda state, entrance=entrance.entrance_name: getattr(Macros, get_access_rule(entrance))(
                state, player
            )
            great_sea_region.connect(world.get_region(entrance.entrance_name), rule=rule)

        # Connect nested regions with their parent region.
        for entrance in MINIBOSS_ENTRANCES + BOSS_ENTRANCES + SECRET_CAVE_INNER_ENTRANCES:
            parent_region_name = entrance.entrance_name.split(" in ")[-1]
            # Consider Hyrule Castle and Forsaken Fortress as part of The Great Sea (regions are not randomizable).
            if parent_region_name in ["Hyrule Castle", "Forsaken Fortress"]:
                parent_region_name = "The Great Sea"
            rule = lambda state, entrance=entrance.entrance_name: getattr(Macros, get_access_rule(entrance))(
                state, player
            )
            parent_region = world.get_region(parent_region_name)
            parent_region.connect(world.get_region(entrance.entrance_name), rule=rule)

        # Randomize which chart points to each sector, if the option is enabled.
        if world.options.randomize_charts:
            world._randomize_charts()

        # Set nonprogress location from options.
        world._set_nonprogress_locations()

        # Select required bosses.
        if world.options.required_bosses:
            world._randomize_required_bosses()

        # Connect the regions together in the multiworld. Randomize entrances to exits, if the option is set.
        world.entrances.randomize_entrances()

    def pre_fill(self):
        # Ban the Bait Bag slot from having bait.
        beedle_20 = self.get_location("The Great Sea - Beedle's Shop Ship - 20 Rupee Item")
        add_item_rule(beedle_20, lambda item: item.name not in ["All-Purpose Bait", "Hyoi Pear"])

        # Also ban the same item from appearing more than once in the Rock Spire Isle shop ship.
        beedle_500 = self.get_location("Rock Spire Isle - Beedle's Special Shop Ship - 500 Rupee Item")
        beedle_950 = self.get_location("Rock Spire Isle - Beedle's Special Shop Ship - 950 Rupee Item")
        beedle_900 = self.get_location(
            "Rock Spire Isle - Beedle's Special Shop Ship - 900 Rupee Item",
        )
        add_item_rule(
            beedle_500,
            lambda item, locs=[beedle_950, beedle_900]: (
                (item.game == "The Wind Waker" and all(l.item is None or item.name != l.item.name for l in locs))
                or (
                    item.game != "The Wind Waker"
                    and all(l.item is None or l.item.game == "The Wind Waker" for l in locs)
                )
            ),
        )
        add_item_rule(
            beedle_950,
            lambda item, locs=[beedle_500, beedle_900]: (
                (item.game == "The Wind Waker" and all(l.item is None or item.name != l.item.name for l in locs))
                or (
                    item.game != "The Wind Waker"
                    and all(l.item is None or l.item.game == "The Wind Waker" for l in locs)
                )
            ),
        )
        add_item_rule(
            beedle_900,
            lambda item, locs=[beedle_500, beedle_950]: (
                (item.game == "The Wind Waker" and all(l.item is None or item.name != l.item.name for l in locs))
                or (
                    item.game != "The Wind Waker"
                    and all(l.item is None or l.item.game == "The Wind Waker" for l in locs)
                )
            ),
        )

    @classmethod
    def stage_pre_fill(cls, world):
        from .Dungeons import fill_dungeons_restrictive

        fill_dungeons_restrictive(world)

    def generate_output(self, output_directory: str):
        multiworld = self.multiworld
        player = self.player

        # Determine the current arrangement for charts.
        # Create a list where the original island number is the index and the value is the new island number.
        # Without randomized charts, this array would be just a ordered list of the numbers 1 to 49.
        # With randomized charts, the new island number is where the chart for the original island now leads.
        chart_name_to_island_number = {
            chart_name: island_number for island_number, chart_name in self.island_number_to_chart_name.items()
        }
        charts_mapping: List[int] = []
        for i in range(1, 49 + 1):
            original_chart_name = ISLAND_NUMBER_TO_CHART_NAME[i]
            new_island_number = chart_name_to_island_number[original_chart_name]
            charts_mapping.append(new_island_number)

        # Output seed name and slot number to seed RNG in randomizer client.
        output_data = {
            "Version": list(VERSION),
            "Seed": multiworld.seed_name,
            "Slot": player,
            "Name": self.player_name,
            "Options": {},
            "Required Bosses": self.required_boss_item_locations,
            "Locations": {},
            "Entrances": {},
            "Charts": charts_mapping,
        }

        # Output relevant options to file.
        for field in fields(self.options):
            output_data["Options"][field.name] = getattr(self.options, field.name).value

        # Temporarily force boss rematches to be skipped until Jalhalla bug is fixed.
        output_data["Options"]["skip_rematch_bosses"] = True

        # Output which item has been placed at each location.
        locations = multiworld.get_locations(player)
        for location in locations:
            if location.name != "Defeat Ganondorf":
                if location.item:
                    item_info = {
                        "player": location.item.player,
                        "name": location.item.name,
                        "game": location.item.game,
                        "classification": location.item.classification.name,
                    }
                else:
                    item_info = {
                        "name": "Nothing",
                        "game": "The Wind Waker",
                        "classification": "filler",
                    }
                output_data["Locations"][location.name] = item_info

        # Output the mapping of entrances to exits.
        all_entrance_names = [en.entrance_name for en in ALL_ENTRANCES]
        entrances = multiworld.get_entrances(player)
        for entrance in entrances:
            if entrance.parent_region.name in all_entrance_names:
                output_data["Entrances"][entrance.parent_region.name] = entrance.connected_region.name

        # Output the plando details to file.
        file_path = os.path.join(output_directory, f"{multiworld.get_out_file_name_base(player)}.aptww")
        with open(file_path, "w") as f:
            f.write(yaml.dump(output_data, sort_keys=False))

    def create_item(self, item: str) -> TWWItem:
        # TODO: calculate nonprogress items dynamically
        adjusted_classification = None
        if self.options.sword_mode == "swords_optional" and item == "Progressive Sword":
            adjusted_classification = IC.useful
        if not self.options.progression_dungeons and item.endswith(" Key"):
            adjusted_classification = IC.filler
        if not self.options.progression_triforce_charts and item.startswith("Triforce Chart"):
            adjusted_classification = IC.filler
        if not self.options.progression_treasure_charts and item.startswith("Treasure Chart"):
            adjusted_classification = IC.filler

        if item in ITEM_TABLE:
            return TWWItem(item, self.player, ITEM_TABLE[item], adjusted_classification)
        raise KeyError(f"Invalid item name: {item}")

    def get_filler_item_name(self) -> str:
        # Use the same weights for filler items that are used in the base randomizer.
        filler_consumables = [
            "Yellow Rupee",
            "Red Rupee",
            "Purple Rupee",
            "Orange Rupee",
            "Joy Pendant",
        ]
        filler_weights = [3, 7, 10, 15, 3]
        return self.multiworld.random.choices(filler_consumables, weights=filler_weights, k=1)[0]

    def get_pre_fill_items(self):
        res = []
        if self.dungeon_local_item_names:
            for dungeon in self.dungeons.values():
                for item in dungeon.all_items:
                    if item.name in self.dungeon_local_item_names:
                        res.append(item)
        return res

    def fill_slot_data(self):
        slot_data = {
            "progression_dungeons": self.options.progression_dungeons.value,
            "progression_tingle_chests": self.options.progression_tingle_chests.value,
            "progression_dungeon_secrets": self.options.progression_dungeon_secrets.value,
            "progression_puzzle_secret_caves": self.options.progression_puzzle_secret_caves.value,
            "progression_combat_secret_caves": self.options.progression_combat_secret_caves.value,
            "progression_savage_labyrinth": self.options.progression_savage_labyrinth.value,
            "progression_great_fairies": self.options.progression_great_fairies.value,
            "progression_short_sidequests": self.options.progression_short_sidequests.value,
            "progression_long_sidequests": self.options.progression_long_sidequests.value,
            "progression_spoils_trading": self.options.progression_spoils_trading.value,
            "progression_minigames": self.options.progression_minigames.value,
            "progression_battlesquid": self.options.progression_battlesquid.value,
            "progression_free_gifts": self.options.progression_free_gifts.value,
            "progression_mail": self.options.progression_mail.value,
            "progression_platforms_rafts": self.options.progression_platforms_rafts.value,
            "progression_submarines": self.options.progression_submarines.value,
            "progression_eye_reef_chests": self.options.progression_eye_reef_chests.value,
            "progression_big_octos_gunboats": self.options.progression_big_octos_gunboats.value,
            "progression_triforce_charts": self.options.progression_triforce_charts.value,
            "progression_treasure_charts": self.options.progression_treasure_charts.value,
            "progression_expensive_purchases": self.options.progression_expensive_purchases.value,
            "progression_island_puzzles": self.options.progression_island_puzzles.value,
            "progression_misc": self.options.progression_misc.value,
            "randomize_mapcompass": self.options.randomize_mapcompass.value,
            "randomize_smallkeys": self.options.randomize_smallkeys.value,
            "randomize_bigkeys": self.options.randomize_bigkeys.value,
            "sword_mode": self.options.sword_mode.value,
            "required_bosses": self.options.required_bosses.value,
            "num_required_bosses": self.options.num_required_bosses.value,
            "chest_type_matches_contents": self.options.chest_type_matches_contents.value,
            "included_dungeons": self.options.included_dungeons.value,
            "excluded_dungeons": self.options.excluded_dungeons.value,
            # "trap_chests": self.options.trap_chests.value,
            "hero_mode": self.options.hero_mode.value,
            "logic_obscurity": self.options.logic_obscurity.value,
            "logic_precision": self.options.logic_precision.value,
            "enable_tuner_logic": self.options.enable_tuner_logic.value,
            "randomize_dungeon_entrances": self.options.randomize_dungeon_entrances.value,
            "randomize_secret_cave_entrances": self.options.randomize_secret_cave_entrances.value,
            "randomize_miniboss_entrances": self.options.randomize_miniboss_entrances.value,
            "randomize_boss_entrances": self.options.randomize_boss_entrances.value,
            "randomize_secret_cave_inner_entrances": self.options.randomize_secret_cave_inner_entrances.value,
            "randomize_fairy_fountain_entrances": self.options.randomize_fairy_fountain_entrances.value,
            "mix_entrances": self.options.mix_entrances.value,
            "randomize_enemies": self.options.randomize_enemies.value,
            # "randomize_music": self.options.randomize_music.value,
            "randomize_starting_island": self.options.randomize_starting_island.value,
            "randomize_charts": self.options.randomize_charts.value,
            # "hoho_hints": self.options.hoho_hints.value,
            # "fishmen_hints": self.options.fishmen_hints.value,
            # "korl_hints": self.options.korl_hints.value,
            # "num_item_hints": self.options.num_item_hints.value,
            # "num_location_hints": self.options.num_location_hints.value,
            # "num_barren_hints": self.options.num_barren_hints.value,
            # "num_path_hints": self.options.num_path_hints.value,
            # "prioritize_remote_hints": self.options.prioritize_remote_hints.value,
            "swift_sail": self.options.swift_sail.value,
            "instant_text_boxes": self.options.instant_text_boxes.value,
            "reveal_full_sea_chart": self.options.reveal_full_sea_chart.value,
            "add_shortcut_warps_between_dungeons": self.options.add_shortcut_warps_between_dungeons.value,
            # "skip_rematch_bosses": self.options.skip_rematch_bosses.value,
            "remove_music": self.options.remove_music.value,
            "death_link": self.options.death_link.value,
        }

        # Add entrances to slot_data. This is the same data that is written to the .aptww file.
        all_entrance_names = [en.entrance_name for en in ALL_ENTRANCES]
        entrances = {
            entrance.parent_region.name: entrance.connected_region.name
            for entrance in self.multiworld.get_entrances(self.player)
            if entrance.parent_region.name in all_entrance_names
        }
        slot_data["entrances"] = entrances

        return slot_data

import os
from dataclasses import fields
from typing import Any, ClassVar, Dict, List, Mapping, Set, Tuple, Union

import yaml

from BaseClasses import Item
from BaseClasses import ItemClassification as IC
from BaseClasses import MultiWorld, Region, Tutorial
from Options import Toggle
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_item_rule
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess

from . import Macros
from .Items import ISLAND_NUMBER_TO_CHART_NAME, ITEM_TABLE, TWWItem, item_name_groups
from .Locations import LOCATION_TABLE, TWWFlag, TWWLocation
from .Options import TWWOptions, tww_option_groups
from .randomizers.Charts import ChartRandomizer
from .randomizers.Dungeons import Dungeon, create_dungeons
from .randomizers.Entrances import (
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
from .randomizers.ItemPool import generate_itempool
from .randomizers.RequiredBosses import RequiredBossesRandomizer
from .Rules import set_rules

VERSION: Tuple[int, int, int] = (2, 6, 0)


def run_client() -> None:
    print("Running The Wind Waker Client")
    from .TWWClient import main  # lazy import

    launch_subprocess(main, name="TheWindWakerClient")


components.append(
    Component(
        "The Wind Waker Client", func=run_client, component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".aptww")
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
        super(TWWWorld, self).__init__(*args, **kwargs)

        self.dungeon_local_item_names: Set[str] = set()
        self.dungeon_specific_item_names: Set[str] = set()
        self.dungeons: Dict[str, Dungeon] = {}

        self.nonprogress_locations: Set[str] = set()

        self.charts = ChartRandomizer(self)
        self.entrances = EntranceRandomizer(self)
        self.boss_reqs = RequiredBossesRandomizer(self)

    def _determine_item_classification(self, name: str) -> Union[IC, None]:
        # TODO: calculate nonprogress items dynamically
        adjusted_classification = None
        if self.options.sword_mode == "swords_optional" and name == "Progressive Sword":
            adjusted_classification = IC.useful
        if not self.options.progression_dungeons and name.endswith(" Key"):
            adjusted_classification = IC.filler
        if not self.options.progression_triforce_charts and name.startswith("Triforce Chart"):
            adjusted_classification = IC.filler
        if not self.options.progression_treasure_charts and name.startswith("Treasure Chart"):
            adjusted_classification = IC.filler

        return adjusted_classification

    def _determine_nonprogress_locations(self) -> Set[str]:
        def add_flag(option: Toggle, flag: TWWFlag) -> TWWFlag:
            return flag if option else TWWFlag.ALWAYS

        options = self.options

        enabled_flags = TWWFlag.ALWAYS
        enabled_flags |= add_flag(options.progression_dungeons, TWWFlag.DUNGEON | TWWFlag.BOSS)
        enabled_flags |= add_flag(options.progression_tingle_chests, TWWFlag.TNGL_CT)
        enabled_flags |= add_flag(options.progression_dungeon_secrets, TWWFlag.DG_SCRT)
        enabled_flags |= add_flag(options.progression_puzzle_secret_caves, TWWFlag.PZL_CVE)
        enabled_flags |= add_flag(options.progression_combat_secret_caves, TWWFlag.CBT_CVE)
        enabled_flags |= add_flag(options.progression_savage_labyrinth, TWWFlag.SAVAGE)
        enabled_flags |= add_flag(options.progression_great_fairies, TWWFlag.GRT_FRY)
        enabled_flags |= add_flag(options.progression_short_sidequests, TWWFlag.SHRT_SQ)
        enabled_flags |= add_flag(options.progression_long_sidequests, TWWFlag.LONG_SQ)
        enabled_flags |= add_flag(options.progression_spoils_trading, TWWFlag.SPOILS)
        enabled_flags |= add_flag(options.progression_minigames, TWWFlag.MINIGME)
        enabled_flags |= add_flag(options.progression_battlesquid, TWWFlag.SPLOOSH)
        enabled_flags |= add_flag(options.progression_free_gifts, TWWFlag.FREE_GF)
        enabled_flags |= add_flag(options.progression_platforms_rafts, TWWFlag.PLTFRMS)
        enabled_flags |= add_flag(options.progression_submarines, TWWFlag.SUBMRIN)
        enabled_flags |= add_flag(options.progression_eye_reef_chests, TWWFlag.EYE_RFS)
        enabled_flags |= add_flag(options.progression_big_octos_gunboats, TWWFlag.BG_OCTO)
        enabled_flags |= add_flag(options.progression_triforce_charts, TWWFlag.TRI_CHT)
        enabled_flags |= add_flag(options.progression_treasure_charts, TWWFlag.TRE_CHT)
        enabled_flags |= add_flag(options.progression_expensive_purchases, TWWFlag.XPENSVE)
        enabled_flags |= add_flag(options.progression_island_puzzles, TWWFlag.ISLND_P)
        enabled_flags |= add_flag(options.progression_misc, TWWFlag.MISCELL)

        # If not all the flags for a location are set, then force that location to have a non-progress item.
        nonprogress_locations: Set[str] = set()
        for location in self.multiworld.get_locations(self.player):
            assert isinstance(location, TWWLocation)
            if location.flags & enabled_flags != location.flags:
                nonprogress_locations.add(location.name)

        return nonprogress_locations

    def generate_early(self) -> None:
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
                else:
                    self.options.local_items.value |= self.dungeon_local_item_names

    create_dungeons = create_dungeons

    def create_regions(self) -> None:
        def get_access_rule(region: str) -> str:
            snake_case_region = region.lower().replace("'", "").replace(" ", "_")
            return f"can_access_{snake_case_region}"

        multiworld = self.multiworld
        player = self.player
        options = self.options

        # "Menu" is the required starting point.
        menu_region = Region("Menu", player, multiworld)
        multiworld.regions.append(menu_region)

        # "The Great Sea" region contains all locations not in a randomizable region.
        great_sea_region = Region("The Great Sea", player, multiworld)
        multiworld.regions.append(great_sea_region)

        # Add all randomizable regions.
        for _entrance in ALL_ENTRANCES:
            multiworld.regions.append(Region(_entrance.entrance_name, player, multiworld))
        for _exit in ALL_EXITS:
            multiworld.regions.append(Region(_exit.unique_name, player, multiworld))

        # Select required bosses.
        if self.options.required_bosses:
            self.boss_reqs.randomize_required_bosses()

        # Create the dungeon classes.
        self.create_dungeons()

        # Assign each location to their region.
        for _location, data in LOCATION_TABLE.items():
            region = self.get_region(data.region)
            location = TWWLocation(player, _location, region, data)

            # Additionally, assign dungeon locations to the appropriate dungeon.
            if region.name in self.dungeons:
                location.dungeon = self.dungeons[region.name]
            elif region.name in MINIBOSS_EXIT_TO_DUNGEON and not options.randomize_miniboss_entrances:
                location.dungeon = self.dungeons[MINIBOSS_EXIT_TO_DUNGEON[region.name]]
            elif region.name in BOSS_EXIT_TO_DUNGEON and not options.randomize_boss_entrances:
                location.dungeon = self.dungeons[BOSS_EXIT_TO_DUNGEON[region.name]]
            elif location.name in [
                "Forsaken Fortress - Phantom Ganon",
                "Forsaken Fortress - Chest Outside Upper Jail Cell",
                "Forsaken Fortress - Chest Inside Lower Jail Cell",
                "Forsaken Fortress - Chest Guarded By Bokoblin",
                "Forsaken Fortress - Chest on Bed",
            ]:
                location.dungeon = self.dungeons["Forsaken Fortress"]
            region.locations.append(location)

        # Connect the "Menu" region to the "The Great Sea" region.
        menu_region.connect(great_sea_region)

        # Connect the dungeon, secret caves, and fairy fountain regions to the "The Great Sea" region.
        for entrance in DUNGEON_ENTRANCES + SECRET_CAVE_ENTRANCES + FAIRY_FOUNTAIN_ENTRANCES:
            great_sea_region.connect(
                self.get_region(entrance.entrance_name),
                rule=lambda state, entrance=entrance.entrance_name: getattr(Macros, get_access_rule(entrance))(
                    state, player
                ),
            )

        # Connect nested regions with their parent region.
        for entrance in MINIBOSS_ENTRANCES + BOSS_ENTRANCES + SECRET_CAVE_INNER_ENTRANCES:
            parent_region_name = entrance.entrance_name.split(" in ")[-1]
            # Consider Hyrule Castle and Forsaken Fortress as part of The Great Sea (regions are not randomizable).
            if parent_region_name in ["Hyrule Castle", "Forsaken Fortress"]:
                parent_region_name = "The Great Sea"
            parent_region = self.get_region(parent_region_name)
            parent_region.connect(
                self.get_region(entrance.entrance_name),
                rule=lambda state, entrance=entrance.entrance_name: getattr(Macros, get_access_rule(entrance))(
                    state, player
                ),
            )

        self.post_create_regions()

    def post_create_regions(self) -> None:
        # Randomize which chart points to each sector, if the option is enabled.
        if self.options.randomize_charts:
            self.charts.randomize_charts()

        # Determine nonprogress location from options.
        self.nonprogress_locations |= self._determine_nonprogress_locations()

        # With all non-progress locations set, exclude them from containing progression.
        for location_name in self.nonprogress_locations:
            self.options.exclude_locations.value.add(location_name)

        # Connect the regions together in the multiworld. Randomize entrances to exits, if the option is set.
        self.entrances.randomize_entrances()

    def pre_fill(self) -> None:
        # Ban the Bait Bag slot from having bait.
        beedle_20 = self.get_location("The Great Sea - Beedle's Shop Ship - 20 Rupee Item")
        add_item_rule(beedle_20, lambda item: item.name not in ["All-Purpose Bait", "Hyoi Pear"])

        # Also ban the same item from appearing more than once in the Rock Spire Isle shop ship.
        beedle_500 = self.get_location("Rock Spire Isle - Beedle's Special Shop Ship - 500 Rupee Item")
        beedle_950 = self.get_location("Rock Spire Isle - Beedle's Special Shop Ship - 950 Rupee Item")
        beedle_900 = self.get_location("Rock Spire Isle - Beedle's Special Shop Ship - 900 Rupee Item")
        add_item_rule(
            beedle_500,
            lambda item, locations=[beedle_950, beedle_900]: (
                (
                    item.game == "The Wind Waker"
                    and all(location.item is None or item.name != location.item.name for location in locations)
                )
                or (
                    item.game != "The Wind Waker"
                    and all(location.item is None or location.item.game == "The Wind Waker" for location in locations)
                )
            ),
        )
        add_item_rule(
            beedle_950,
            lambda item, locations=[beedle_500, beedle_900]: (
                (
                    item.game == "The Wind Waker"
                    and all(location.item is None or item.name != location.item.name for location in locations)
                )
                or (
                    item.game != "The Wind Waker"
                    and all(location.item is None or location.item.game == "The Wind Waker" for location in locations)
                )
            ),
        )
        add_item_rule(
            beedle_900,
            lambda item, locations=[beedle_500, beedle_950]: (
                (
                    item.game == "The Wind Waker"
                    and all(location.item is None or item.name != location.item.name for location in locations)
                )
                or (
                    item.game != "The Wind Waker"
                    and all(location.item is None or location.item.game == "The Wind Waker" for location in locations)
                )
            ),
        )

    @classmethod
    def stage_pre_fill(cls, world: MultiWorld) -> None:
        from .randomizers.Dungeons import fill_dungeons_restrictive

        fill_dungeons_restrictive(world)

    def generate_output(self, output_directory: str) -> None:
        multiworld = self.multiworld
        player = self.player

        # Determine the current arrangement for charts.
        # Create a list where the original island number is the index and the value is the new island number.
        # Without randomized charts, this array would be just a ordered list of the numbers 1 to 49.
        # With randomized charts, the new island number is where the chart for the original island now leads.
        chart_name_to_island_number = {
            chart_name: island_number for island_number, chart_name in self.charts.island_number_to_chart_name.items()
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
            "Required Bosses": self.boss_reqs.required_boss_item_locations,
            "Locations": {},
            "Entrances": {},
            "Charts": charts_mapping,
        }

        # Output relevant options to file.
        for field in fields(self.options):
            output_data["Options"][field.name] = getattr(self.options, field.name).value

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
                    item_info = {"name": "Nothing", "game": "The Wind Waker", "classification": "filler"}
                output_data["Locations"][location.name] = item_info

        # Output the mapping of entrances to exits.
        all_entrance_names = [en.entrance_name for en in ALL_ENTRANCES]
        entrances = multiworld.get_entrances(player)
        for entrance in entrances:
            assert entrance.parent_region is not None
            if entrance.parent_region.name in all_entrance_names:
                assert entrance.connected_region is not None
                output_data["Entrances"][entrance.parent_region.name] = entrance.connected_region.name

        # Output the plando details to file.
        file_path = os.path.join(output_directory, f"{multiworld.get_out_file_name_base(player)}.aptww")
        with open(file_path, "w") as f:
            f.write(yaml.dump(output_data, sort_keys=False))

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]) -> None:
        # Regardless of ER settings, always hint the outermost entrance for every "interior" location
        hint_data[self.player] = {}
        for location in self.multiworld.get_locations(self.player):
            if location.address is not None and location.item is not None:
                zone_exit = self.entrances.get_zone_exit_for_item_location(location.name)
                if zone_exit is not None:
                    outermost_entrance = self.entrances.get_outermost_entrance_for_exit(zone_exit)
                    assert outermost_entrance is not None and outermost_entrance.island_name is not None
                    hint_data[self.player][location.address] = outermost_entrance.island_name

    def create_item(self, name: str) -> TWWItem:
        if name in ITEM_TABLE:
            return TWWItem(name, self.player, ITEM_TABLE[name], self._determine_item_classification(name))
        raise KeyError(f"Invalid item name: {name}")

    def get_filler_item_name(self) -> str:
        # Use the same weights for filler items that are used in the base randomizer.
        filler_consumables = ["Yellow Rupee", "Red Rupee", "Purple Rupee", "Orange Rupee", "Joy Pendant"]
        filler_weights = [3, 7, 10, 15, 3]
        return self.multiworld.random.choices(filler_consumables, weights=filler_weights, k=1)[0]

    def get_pre_fill_items(self) -> List[Item]:
        res = []
        if self.dungeon_local_item_names:
            for dungeon in self.dungeons.values():
                for item in dungeon.all_items:
                    if item.name in self.dungeon_local_item_names:
                        res.append(item)
        return res

    def fill_slot_data(self) -> Mapping[str, Any]:
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
            "skip_rematch_bosses": self.options.skip_rematch_bosses.value,
            "remove_music": self.options.remove_music.value,
            "death_link": self.options.death_link.value,
        }

        # Add entrances to slot_data. This is the same data that is written to the .aptww file.
        all_entrance_names = [en.entrance_name for en in ALL_ENTRANCES]
        entrances = {
            entrance.parent_region.name: entrance.connected_region.name
            for entrance in self.multiworld.get_entrances(self.player)
            if entrance.parent_region is not None
            and entrance.connected_region is not None
            and entrance.parent_region.name in all_entrance_names
        }
        slot_data["entrances"] = entrances

        return slot_data

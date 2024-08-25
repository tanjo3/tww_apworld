from typing import List

from BaseClasses import LocationProgressType
from Options import OptionError

from ..Locations import DUNGEON_NAMES, LOCATION_TABLE, TWWFlag, split_location_name_by_zone


class RequiredBossesRandomizer:
    def __init__(self, world):
        self.world = world
        self.multiworld = world.multiworld

        self.required_boss_item_locations: List[str] = []
        self.required_dungeons: List[str] = []
        self.required_bosses: List[str] = []
        self.banned_locations: List[str] = []
        self.banned_dungeons: List[str] = []
        self.banned_bosses: List[str] = []

    def validate_boss_options(self, options):
        if not options.progression_dungeons:
            raise OptionError("Cannot make bosses required when progression dungeons are disabled.")

        if len(options.included_dungeons.value & options.excluded_dungeons.value) != 0:
            raise OptionError("Conflict found in the lists of required and banned dungeons for required bosses mode.")

    def randomize_required_bosses(self):
        options = self.world.options

        # Validate constraints on required bosses options.
        self.validate_boss_options(options)

        # If the user enforces a dungeon location to be priority, consider that when selecting required bosses.
        dungeon_names = set(DUNGEON_NAMES)
        required_dungeons = options.included_dungeons.value
        for location_name in options.priority_locations.value:
            dungeon_name, _ = split_location_name_by_zone(location_name)
            if dungeon_name in dungeon_names:
                required_dungeons.add(dungeon_name)

        # Ensure that we aren't prioritizing more dungeon locations than requested number of required bosses.
        num_required_bosses = options.num_required_bosses
        if len(required_dungeons) > num_required_bosses:
            raise OptionError("Could not select required bosses to satisfy options set by user.")

        # Ensure that after removing excluded dungeons that we still have enough dungeons to satisfy user options.
        num_remaining = num_required_bosses - len(required_dungeons)
        remaining_dungeon_options = dungeon_names - required_dungeons - options.excluded_dungeons.value
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
            self.world.get_location(location_name).progress_type = LocationProgressType.EXCLUDED

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
from typing import Dict, List

from BaseClasses import ItemClassification
from Fill import FillError

from ..Items import ITEM_TABLE, item_factory
from .Dungeons import get_dungeon_item_pool_player

VANILLA_DUNGEON_ITEM_LOCATIONS: Dict[str, List[str]] = {
    "DRC Small Key": [
        "Dragon Roost Cavern - First Room",
        "Dragon Roost Cavern - Boarded Up Chest",
        "Dragon Roost Cavern - Rat Room Boarded Up Chest",
        "Dragon Roost Cavern - Bird's Nest",
    ],
    "FW Small Key": [
        "Forbidden Woods - Vine Maze Right Chest"
    ],
    "TotG Small Key": [
        "Tower of the Gods - Hop Across Floating Boxes",
        "Tower of the Gods - Floating Platforms Room"
    ],
    "ET Small Key": [
        "Earth Temple - Transparent Chest in First Crypt",
        "Earth Temple - Casket in Second Crypt",
        "Earth Temple - End of Foggy Room With Floormasters",
    ],
    "WT Small Key": [
        "Wind Temple - Spike Wall Room - First Chest",
        "Wind Temple - Chest Behind Seven Armos"
    ],

    "DRC Big Key":  ["Dragon Roost Cavern - Big Key Chest"],
    "FW Big Key":   ["Forbidden Woods - Big Key Chest"],
    "TotG Big Key": ["Tower of the Gods - Big Key Chest"],
    "ET Big Key":   ["Earth Temple - Big Key Chest"],
    "WT Big Key":   ["Wind Temple - Big Key Chest"],

    "DRC Dungeon Map":  ["Dragon Roost Cavern - Alcove With Water Jugs"],
    "FW Dungeon Map":   ["Forbidden Woods - First Room"],
    "TotG Dungeon Map": ["Tower of the Gods - Chest Behind Bombable Walls"],
    "FF Dungeon Map":   ["Forsaken Fortress - Chest Outside Upper Jail Cell"],
    "ET Dungeon Map":   ["Earth Temple - Transparent Chest In Warp Pot Room"],
    "WT Dungeon Map":   ["Wind Temple - Chest In Many Cyclones Room"],

    "DRC Compass":  ["Dragon Roost Cavern - Rat Room"],
    "FW Compass":   ["Forbidden Woods - Vine Maze Left Chest"],
    "TotG Compass": ["Tower of the Gods - Skulls Room Chest"],
    "FF Compass":   ["Forsaken Fortress - Chest Guarded By Bokoblin"],
    "ET Compass":   ["Earth Temple - Chest In Three Blocks Room"],
    "WT Compass":   ["Wind Temple - Chest In Middle Of Hub Room"],
}


def generate_itempool(world):
    multiworld = world.multiworld

    # Get the core pool of items.
    pool, precollected_items = get_pool_core(world)

    # Add precollected items to the multiworld's `precollected_items` list.
    for item in precollected_items:
        multiworld.push_precollected(item_factory(item, world))

    # Place a "Victory" item on "Defeat Ganondorf" for the spoiler log.
    world.get_location("Defeat Ganondorf").place_locked_item(item_factory("Victory", world))

    # Create the pool of the remaining shuffled items.
    items = item_factory(pool, world)
    multiworld.random.shuffle(items)

    multiworld.itempool += items

    # Dungeon items should already be created, so handle those separately.
    handle_dungeon_items(world)


def get_pool_core(world):
    pool: List[str] = []
    precollected_items: List[str] = []
    n_pending_junk: int = 0

    # Add regular items to the item pool.
    for item, data in ITEM_TABLE.items():
        if data.type == "Item":
            pool.extend([item] * data.quantity)

    # If the player starts with a sword, add one to the precollected items list and remove one from the item pool.
    if world.options.sword_mode == "start_with_sword":
        precollected_items.append("Progressive Sword")
        n_pending_junk += 1
        pool.remove("Progressive Sword")
    # Or, if it's swordless mode, remove all swords from the item pool.
    elif world.options.sword_mode == "swordless":
        while "Progressive Sword" in pool:
            n_pending_junk += 1
            pool.remove("Progressive Sword")

    # Place filler items to replace the items we've removed from the pool core.
    pool.extend([world.get_filler_item_name() for _ in range(n_pending_junk)])

    return pool, precollected_items


def handle_dungeon_items(world):
    player = world.player
    multiworld = world.multiworld
    options = world.options

    dungeon_items = [
        item
        for item in get_dungeon_item_pool_player(world)
        if item.name not in multiworld.worlds[player].dungeon_local_item_names
    ]

    for x in range(len(dungeon_items) - 1, -1, -1):
        item = dungeon_items[x]

        # Consider dungeon items in non-required dungeons as filler
        if item.dungeon.name in world.boss_reqs.banned_dungeons:
            item.classification = ItemClassification.filler

        if item.type == "Big Key":
            option = options.randomize_bigkeys
        elif item.type == "Small Key":
            option = options.randomize_smallkeys
        else:
            option = options.randomize_mapcompass

        if option == "startwith":
            dungeon_items.pop(x)
            multiworld.push_precollected(item)
            multiworld.itempool.append(item_factory(world.get_filler_item_name(), world))
        elif option == "vanilla":
            for location_name in VANILLA_DUNGEON_ITEM_LOCATIONS[item.name]:
                location = world.get_location(location_name)
                if location.item is None:
                    dungeon_items.pop(x)
                    location.place_locked_item(item)
                    break
            else:
                raise FillError(f"Could not place dungeon item in vanilla location: {item}")

    multiworld.itempool.extend([item for item in dungeon_items])

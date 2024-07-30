from typing import Dict, List

from .Items import ITEM_TABLE, item_factory


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
    pool, placed_items, precollected_items = get_pool_core(world)

    # Add precollected items to the multiworld's `precollected_items` list.
    for item in precollected_items:
        multiworld.push_precollected(item_factory(item, world))

    # Set placed items to their location and lock that item to that location.
    for location, item in placed_items.items():
        world.get_location(location).place_locked_item(item_factory(item, world))

    # Create the pool of the remaining shuffled items.
    items = item_factory(pool, world)
    multiworld.random.shuffle(items)

    multiworld.itempool += items


def get_pool_core(world):
    options = world.options

    pool: List[str] = []
    placed_items: Dict[str, str] = {}
    precollected_items: List[str] = []
    n_pending_junk: int = 0

    def place_item(loc, item):
        assert loc not in placed_items, f"Item {item.name} has already been placed!"
        placed_items[loc] = item

    # Properly categorize each item in the item table.
    for item, data in ITEM_TABLE.items():
        # Big Key
        if data.type == "Big Key":
            if options.randomize_bigkeys == "startwith":
                precollected_items.extend([item] * data.quantity)
                n_pending_junk += data.quantity
            elif options.randomize_bigkeys == "vanilla":
                for loc in VANILLA_DUNGEON_ITEM_LOCATIONS[item]:
                    place_item(loc, item)
            elif not options.randomize_bigkeys.in_dungeon:
                pool.extend([item] * data.quantity)

        # Small Key
        elif data.type == "Small Key":
            if options.randomize_smallkeys == "startwith":
                precollected_items.extend([item] * data.quantity)
                n_pending_junk += data.quantity
            elif options.randomize_smallkeys == "vanilla":
                for loc in VANILLA_DUNGEON_ITEM_LOCATIONS[item]:
                    place_item(loc, item)
            elif not options.randomize_smallkeys.in_dungeon:
                pool.extend([item] * data.quantity)

        # Dungeon Map or Compass
        elif data.type in ("Map", "Compass"):
            if options.randomize_mapcompass == "startwith":
                precollected_items.extend([item] * data.quantity)
                n_pending_junk += data.quantity
            elif options.randomize_mapcompass == "vanilla":
                for loc in VANILLA_DUNGEON_ITEM_LOCATIONS[item]:
                    place_item(loc, item)
            elif not options.randomize_mapcompass.in_dungeon:
                pool.extend([item] * data.quantity)

        # The rest of the items
        elif data.type == "Item":
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

    # Place a "Victory" item on "Defeat Ganondorf" for the spoiler log.
    place_item("Defeat Ganondorf", "Victory")

    return pool, placed_items, precollected_items

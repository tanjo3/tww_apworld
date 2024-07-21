from typing import Dict, List

from .Items import ITEM_TABLE, item_factory
from .Locations import VANILLA_DUNGEON_ITEM_LOCATIONS


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

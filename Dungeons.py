from typing import Set, Tuple

from BaseClasses import CollectionState, MultiWorld
from Fill import fill_restrictive

from .Items import item_factory


class Dungeon:
    def __init__(
        self,
        name: str,
        big_key,
        small_keys,
        dungeon_items,
        player: int,
    ):
        self.name = name
        self.big_key = big_key
        self.small_keys = small_keys
        self.dungeon_items = dungeon_items
        self.player = player

    @property
    def keys(self):
        return self.small_keys + ([self.big_key] if self.big_key else [])

    @property
    def all_items(self):
        return self.dungeon_items + self.keys

    def __eq__(self, other) -> bool:
        if isinstance(other, Dungeon):
            return self.name == other.name and self.player == other.player
        return False

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.name} (Player {self.player})"


def create_dungeons(world):
    player = world.player

    def make_dungeon(name, big_key, small_keys, dungeon_items):
        dungeon = Dungeon(
            name,
            big_key,
            small_keys,
            dungeon_items,
            player,
        )
        for item in dungeon.all_items:
            item.dungeon = dungeon
        return dungeon

    DRC = make_dungeon(
        "Dragon Roost Cavern",
        item_factory("DRC Big Key", world),
        item_factory(["DRC Small Key"] * 4, world),
        item_factory(["DRC Dungeon Map", "DRC Compass"], world),
    )
    FW = make_dungeon(
        "Forbidden Woods",
        item_factory("FW Big Key", world),
        item_factory(["FW Small Key"] * 1, world),
        item_factory(["FW Dungeon Map", "FW Compass"], world),
    )
    TOTG = make_dungeon(
        "Tower of the Gods",
        item_factory("TotG Big Key", world),
        item_factory(["TotG Small Key"] * 2, world),
        item_factory(["TotG Dungeon Map", "TotG Compass"], world),
    )
    FF = make_dungeon(
        "Forsaken Fortress",
        None,
        [],
        item_factory(["FF Dungeon Map", "FF Compass"], world),
    )
    ET = make_dungeon(
        "Earth Temple",
        item_factory("ET Big Key", world),
        item_factory(["ET Small Key"] * 3, world),
        item_factory(["ET Dungeon Map", "ET Compass"], world),
    )
    WT = make_dungeon(
        "Wind Temple",
        item_factory("WT Big Key", world),
        item_factory(["WT Small Key"] * 2, world),
        item_factory(["WT Dungeon Map", "WT Compass"], world),
    )

    for dungeon in [DRC, FW, TOTG, FF, ET, WT]:
        world.dungeons[dungeon.name] = dungeon


def get_dungeon_item_pool(multiworld: MultiWorld):
    return [
        item for world in multiworld.get_game_worlds("The Wind Waker") for item in get_dungeon_item_pool_player(world)
    ]


def get_dungeon_item_pool_player(world):
    return [item for dungeon in world.dungeons.values() for item in dungeon.all_items]


def get_unfilled_dungeon_locations(multiworld: MultiWorld):
    return [
        location
        for world in multiworld.get_game_worlds("The Wind Waker")
        for location in multiworld.get_locations(world.player)
        if location.dungeon and not location.item
    ]


def fill_dungeons_restrictive(multiworld: MultiWorld):
    localized: Set[Tuple[int, str]] = set()
    dungeon_specific: Set[Tuple[int, str]] = set()
    for subworld in multiworld.get_game_worlds("The Wind Waker"):
        player = subworld.player
        if player not in multiworld.groups:
            localized |= {(player, item_name) for item_name in subworld.dungeon_local_item_names}
            dungeon_specific |= {(player, item_name) for item_name in subworld.dungeon_specific_item_names}

    if localized:
        in_dungeon_items = [item for item in get_dungeon_item_pool(multiworld) if (item.player, item.name) in localized]
        if in_dungeon_items:
            locations = [location for location in get_unfilled_dungeon_locations(multiworld)]
            for location in locations:
                orig_rule = location.item_rule
                if dungeon_specific:
                    # Restrict dungeon items to be in their own dungeons.
                    dungeon = location.dungeon
                    location.item_rule = lambda item, dungeon=dungeon, orig_rule=orig_rule: (
                        not (item.player, item.name) in dungeon_specific or item.dungeon is dungeon
                    ) and orig_rule(item)
                else:
                    # Restrict dungeon items to be in any dungeon in the player's local world.
                    player = location.player
                    location.item_rule = lambda item, player=player, orig_rule=orig_rule: (
                        item.player == player
                    ) and orig_rule(item)

            multiworld.random.shuffle(locations)

            # Dungeon-locked items have to be placed first, to not run out of spaces for dungeon-locked items.
            # Subsort in the order Small Key, Big Key, Other before placing dungeon items.
            sort_order = {"Small Key": 3, "Big Key": 2}
            in_dungeon_items.sort(
                key=lambda item: sort_order.get(item.type, 1)
                + (5 if (item.player, item.name) in dungeon_specific else 0),
                reverse=True,
            )

            # Construct a partial `all_state` which contains only the items from `get_pre_fill_items`, which aren't
            # in a dungeon.
            in_dungeon_player_ids = {item.player for item in in_dungeon_items}
            all_state_base = CollectionState(multiworld)
            for item in multiworld.itempool:
                multiworld.worlds[item.player].collect(all_state_base, item)
            pre_fill_items = []
            for player in in_dungeon_player_ids:
                pre_fill_items += multiworld.worlds[player].get_pre_fill_items()
            for item in in_dungeon_items:
                try:
                    pre_fill_items.remove(item)
                except ValueError:
                    # `pre_fill_items` should be a subset of `in_dungeon_items`, but just in case.
                    pass
            for item in pre_fill_items:
                multiworld.worlds[item.player].collect(all_state_base, item)
            all_state_base.sweep_for_events()

            # Remove completion condition so that minimal-accessibility worlds place keys properly.
            for player in (item.player for item in in_dungeon_items):
                if all_state_base.has("Victory", player):
                    all_state_base.remove(multiworld.worlds[player].create_item("Victory"))

            fill_restrictive(
                multiworld,
                all_state_base,
                locations,
                in_dungeon_items,
                lock=True,
                allow_excluded=True,
                name="TWW Dungeon Items",
            )

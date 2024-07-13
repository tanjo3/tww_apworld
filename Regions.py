DUNGEON_ENTRANCES = [
    "Dungeon Entrance on Dragon Roost Island",
    "Dungeon Entrance in Forest Haven Sector",
    "Dungeon Entrance in Tower of the Gods Sector",
    "Dungeon Entrance on Headstone Island",
    "Dungeon Entrance on Gale Isle",
]
DUNGEON_EXITS = [
    "Dragon Roost Cavern",
    "Forbidden Woods",
    "Tower of the Gods",
    "Earth Temple",
    "Wind Temple",
]

MINIBOSS_ENTRANCES = [
    "Miniboss Entrance in Forbidden Woods",
    "Miniboss Entrance in Tower of the Gods",
    "Miniboss Entrance in Earth Temple",
    "Miniboss Entrance in Wind Temple",
    "Miniboss Entrance in Hyrule Castle",
]
MINIBOSS_EXITS = [
    "Forbidden Woods Miniboss Arena",
    "Tower of the Gods Miniboss Arena",
    "Earth Temple Miniboss Arena",
    "Wind Temple Miniboss Arena",
    "Master Sword Chamber",
]

BOSS_ENTRANCES = [
    "Boss Entrance in Dragon Roost Cavern",
    "Boss Entrance in Forbidden Woods",
    "Boss Entrance in Tower of the Gods",
    "Boss Entrance in Forsaken Fortress",
    "Boss Entrance in Earth Temple",
    "Boss Entrance in Wind Temple",
]
BOSS_EXITS = [
    "Gohma Boss Arena",
    "Kalle Demos Boss Arena",
    "Gohdan Boss Arena",
    "Helmaroc King Boss Arena",
    "Jalhalla Boss Arena",
    "Molgera Boss Arena",
]

SECRET_CAVES_ENTRANCES = [
    "Secret Cave Entrance on Outset Island",
    "Secret Cave Entrance on Dragon Roost Island",
    "Secret Cave Entrance on Fire Mountain",
    "Secret Cave Entrance on Ice Ring Isle",
    "Secret Cave Entrance on Private Oasis",
    "Secret Cave Entrance on Needle Rock Isle",
    "Secret Cave Entrance on Angular Isles",
    "Secret Cave Entrance on Boating Course",
    "Secret Cave Entrance on Stone Watcher Island",
    "Secret Cave Entrance on Overlook Island",
    "Secret Cave Entrance on Bird's Peak Rock",
    "Secret Cave Entrance on Pawprint Isle",
    "Secret Cave Entrance on Pawprint Isle Side Isle",
    "Secret Cave Entrance on Diamond Steppe Island",
    "Secret Cave Entrance on Bomb Island",
    "Secret Cave Entrance on Rock Spire Isle",
    "Secret Cave Entrance on Shark Island",
    "Secret Cave Entrance on Cliff Plateau Isles",
    "Secret Cave Entrance on Horseshoe Island",
    "Secret Cave Entrance on Star Island",
]
SECRET_CAVES_EXITS = [
    "Savage Labyrinth",
    "Dragon Roost Island Secret Cave",
    "Fire Mountain Secret Cave",
    "Ice Ring Isle Secret Cave",
    "Cabana Labyrinth",
    "Needle Rock Isle Secret Cave",
    "Angular Isles Secret Cave",
    "Boating Course Secret Cave",
    "Stone Watcher Island Secret Cave",
    "Overlook Island Secret Cave",
    "Bird's Peak Rock Secret Cave",
    "Pawprint Isle Chuchu Cave",
    "Pawprint Isle Wizzrobe Cave",
    "Diamond Steppe Island Warp Maze Cave",
    "Bomb Island Secret Cave",
    "Rock Spire Isle Secret Cave",
    "Shark Island Secret Cave",
    "Cliff Plateau Isles Secret Cave",
    "Horseshoe Island Secret Cave",
    "Star Island Secret Cave",
]

SECRET_CAVES_INNER_ENTRANCES = [
    "Inner Entrance in Ice Ring Isle Secret Cave",
    "Inner Entrance in Cliff Plateau Isles Secret Cave",
]
SECRET_CAVES_INNER_EXITS = [
    "Ice Ring Isle Inner Cave",
    "Cliff Plateau Isles Inner Cave",
]

FAIRY_FOUNTAIN_ENTRANCES = [
    "Fairy Fountain Entrance on Outset Island",
    "Fairy Fountain Entrance on Thorned Fairy Island",
    "Fairy Fountain Entrance on Eastern Fairy Island",
    "Fairy Fountain Entrance on Western Fairy Island",
    "Fairy Fountain Entrance on Southern Fairy Island",
    "Fairy Fountain Entrance on Northern Fairy Island",
]
FAIRY_FOUNTAIN_EXITS = [
    "Outset Fairy Fountain",
    "Thorned Fairy Fountain",
    "Eastern Fairy Fountain",
    "Western Fairy Fountain",
    "Southern Fairy Fountain",
    "Northern Fairy Fountain",
]

# This dictionary maps exits to entrances located in that exit.
ENTRANCE_ACCESSIBILITY: dict[str, list[str]] = {
    "The Great Sea": [
        "Dungeon Entrance on Dragon Roost Island",
        "Dungeon Entrance in Forest Haven Sector",
        "Dungeon Entrance in Tower of the Gods Sector",
        "Dungeon Entrance on Headstone Island",
        "Dungeon Entrance on Gale Isle",
        "Miniboss Entrance in Hyrule Castle",
        "Boss Entrance in Forsaken Fortress",
        "Secret Cave Entrance on Outset Island",
        "Secret Cave Entrance on Dragon Roost Island",
        "Secret Cave Entrance on Fire Mountain",
        "Secret Cave Entrance on Ice Ring Isle",
        "Secret Cave Entrance on Private Oasis",
        "Secret Cave Entrance on Needle Rock Isle",
        "Secret Cave Entrance on Angular Isles",
        "Secret Cave Entrance on Boating Course",
        "Secret Cave Entrance on Stone Watcher Island",
        "Secret Cave Entrance on Overlook Island",
        "Secret Cave Entrance on Bird's Peak Rock",
        "Secret Cave Entrance on Pawprint Isle",
        "Secret Cave Entrance on Pawprint Isle Side Isle",
        "Secret Cave Entrance on Diamond Steppe Island",
        "Secret Cave Entrance on Bomb Island",
        "Secret Cave Entrance on Rock Spire Isle",
        "Secret Cave Entrance on Shark Island",
        "Secret Cave Entrance on Cliff Plateau Isles",
        "Secret Cave Entrance on Horseshoe Island",
        "Secret Cave Entrance on Star Island",
        "Fairy Fountain Entrance on Outset Island",
        "Fairy Fountain Entrance on Thorned Fairy Island",
        "Fairy Fountain Entrance on Eastern Fairy Island",
        "Fairy Fountain Entrance on Western Fairy Island",
        "Fairy Fountain Entrance on Southern Fairy Island",
        "Fairy Fountain Entrance on Northern Fairy Island",
    ],
    "Dragon Roost Cavern": [
        "Boss Entrance in Dragon Roost Cavern",
    ],
    "Forbidden Woods": [
        "Miniboss Entrance in Forbidden Woods",
        "Boss Entrance in Forbidden Woods",
    ],
    "Tower of the Gods": [
        "Miniboss Entrance in Tower of the Gods",
        "Boss Entrance in Tower of the Gods",
    ],
    "Earth Temple": [
        "Miniboss Entrance in Earth Temple",
        "Boss Entrance in Earth Temple",
    ],
    "Wind Temple": [
        "Miniboss Entrance in Wind Temple",
        "Boss Entrance in Wind Temple",
    ],
    "Ice Ring Isle Secret Cave": [
        "Inner Entrance in Ice Ring Isle Secret Cave",
    ],
    "Cliff Plateau Isles Secret Cave": [
        "Inner Entrance in Cliff Plateau Isles Secret Cave",
    ],
}

MINIBOSS_EXIT_TO_DUNGEON = {
    "Forbidden Woods Miniboss Arena": "Forbidden Woods",
    "Tower of the Gods Miniboss Arena": "Tower of the Gods",
    "Earth Temple Miniboss Arena": "Earth Temple",
    "Wind Temple Miniboss Arena": "Wind Temple",
}

BOSS_EXIT_TO_DUNGEON = {
    "Gohma Boss Arena": "Dragon Roost Cavern",
    "Kalle Demos Boss Arena": "Forbidden Woods",
    "Gohdan Boss Arena": "Tower of the Gods",
    "Helmaroc King Boss Arena": "Forsaken Fortress",
    "Jalhalla Boss Arena": "Earth Temple",
    "Molgera Boss Arena": "Wind Temple",
}

ALL_ENTRANCES = (
    DUNGEON_ENTRANCES
    + MINIBOSS_ENTRANCES
    + BOSS_ENTRANCES
    + SECRET_CAVES_ENTRANCES
    + SECRET_CAVES_INNER_ENTRANCES
    + FAIRY_FOUNTAIN_ENTRANCES
)
ALL_EXITS = (
    DUNGEON_EXITS
    + MINIBOSS_EXITS
    + BOSS_EXITS
    + SECRET_CAVES_EXITS
    + SECRET_CAVES_INNER_EXITS
    + FAIRY_FOUNTAIN_EXITS
)

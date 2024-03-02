from enum import Enum, Flag, auto
from typing import NamedTuple

from BaseClasses import Location, Region


class TWWFlag(Flag):
    ALWAYS = auto()
    DUNGEON = auto()
    TNGL_CT = auto()
    DG_SCRT = auto()
    PZL_CVE = auto()
    CBT_CVE = auto()
    SAVAGE = auto()
    GRT_FRY = auto()
    SHRT_SQ = auto()
    LONG_SQ = auto()
    SPOILS = auto()
    MINIGME = auto()
    SPLOOSH = auto()
    FREE_GF = auto()
    MAILBOX = auto()
    PLTFRMS = auto()
    SUBMRIN = auto()
    EYE_RFS = auto()
    BG_OCTO = auto()
    TRI_CHT = auto()
    TRE_CHT = auto()
    XPENSVE = auto()
    ISLND_P = auto()
    MISCELL = auto()
    OTHER = auto()


class TWWLocationType(Enum):
    CHART = auto()
    BOCTO = auto()
    CHEST = auto()
    SWTCH = auto()
    PCKUP = auto()
    EVENT = auto()
    SPECL = auto()


class TWWLocationData(NamedTuple):
    code: int | None
    flags: TWWFlag
    region: str
    stage_id: int
    type: TWWLocationType
    bit: int
    address: int | None = None


class TWWLocation(Location):
    game: str = "The Wind Waker"

    def __init__(self, player: int, name: str, parent: Region, data: TWWLocationData):
        super(TWWLocation, self).__init__(player, name, address=data.code, parent=parent)
        self.code = data.code
        self.flags = data.flags
        self.region = data.region
        self.stage_id = data.stage_id
        self.type = data.type
        self.bit = data.bit
        self.address = self.address


base_id = 2326528

LOCATION_TABLE: dict[str, TWWLocationData] = {
    # Outset Island
    "Outset Island - Underneath Link's House": TWWLocationData(
        base_id + 0, TWWFlag.MISCELL, "The Great Sea", 0xB, TWWLocationType.CHEST, 5
    ),
    "Outset Island - Mesa the Grasscutter's House": TWWLocationData(
        base_id + 1, TWWFlag.MISCELL, "The Great Sea", 0xB, TWWLocationType.CHEST, 4
    ),
    "Outset Island - Orca - Give 10 Knight's Crests": TWWLocationData(
        base_id + 2, TWWFlag.SPOILS, "The Great Sea", 0xB, TWWLocationType.EVENT, 5, 0x803C5237
    ),
    # "Outset Island - Orca - Hit 500 Times": TWWLocationData(
    #     base_id + 3, TWWFlag.OTHER, "The Great Sea"
    # ),
    # "Outset Island - Great Fairy": TWWLocationData(
    #     base_id + 4, TWWFlag.GRT_FRY, "The Great Sea"
    # ),
    "Outset Island - Jabun's Cave": TWWLocationData(
        base_id + 5, TWWFlag.ISLND_P, "The Great Sea", 0xB, TWWLocationType.CHEST, 6
    ),
    "Outset Island - Dig up Black Soil": TWWLocationData(
        base_id + 6, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.PCKUP, 2
    ),
    "Outset Island - Savage Labyrinth - Floor 30": TWWLocationData(
        base_id + 7, TWWFlag.SAVAGE, "Savage Labyrinth", 0xD, TWWLocationType.CHEST, 11
    ),
    "Outset Island - Savage Labyrinth - Floor 50": TWWLocationData(
        base_id + 8, TWWFlag.SAVAGE, "Savage Labyrinth", 0xD, TWWLocationType.CHEST, 12
    ),

    # Windfall Island
    "Windfall Island - Jail - Tingle - First Gift": TWWLocationData(
        base_id + 9, TWWFlag.FREE_GF, "The Great Sea", 0xB, TWWLocationType.SWTCH, 53
    ),
    "Windfall Island - Jail - Tingle - Second Gift": TWWLocationData(
        base_id + 10, TWWFlag.FREE_GF, "The Great Sea", 0xB, TWWLocationType.SWTCH, 54
    ),
    "Windfall Island - Jail - Maze Chest": TWWLocationData(
        base_id + 11, TWWFlag.ISLND_P, "The Great Sea", 0xB, TWWLocationType.CHEST, 0
    ),
    "Windfall Island - Chu Jelly Juice Shop - Give 15 Green Chu Jelly": TWWLocationData(
        base_id + 12, TWWFlag.SPOILS, "The Great Sea", 0xB, TWWLocationType.EVENT, 2, 0x803C5239
    ),
    "Windfall Island - Chu Jelly Juice Shop - Give 15 Blue Chu Jelly": TWWLocationData(
        base_id + 13, TWWFlag.SPOILS | TWWFlag.LONG_SQ, "The Great Sea", 0xB, TWWLocationType.EVENT, 1, 0x803C5239
    ),
    # "Windfall Island - Ivan - Catch Killer Bees": TWWLocationData(
    #     base_id + 14, TWWFlag.SHRT_SQ, "The Great Sea"
    # ),
    # "Windfall Island - Mrs. Marie - Catch Killer Bees": TWWLocationData(
    #     base_id + 15, TWWFlag.SHRT_SQ, "The Great Sea"
    # ),
    # "Windfall Island - Mrs. Marie - Give 1 Joy Pendant": TWWLocationData(
    #     base_id + 16, TWWFlag.SPOILS, "The Great Sea"
    # ),
    # "Windfall Island - Mrs. Marie - Give 21 Joy Pendants": TWWLocationData(
    #     base_id + 17, TWWFlag.SPOILS, "The Great Sea"
    # ),
    # "Windfall Island - Mrs. Marie - Give 40 Joy Pendants": TWWLocationData(
    #     base_id + 18, TWWFlag.SPOILS, "The Great Sea"
    # ),
    "Windfall Island - Lenzo's House - Left Chest": TWWLocationData(
        base_id + 19, TWWFlag.SHRT_SQ, "The Great Sea", 0xB, TWWLocationType.CHEST, 1
    ),
    "Windfall Island - Lenzo's House - Right Chest": TWWLocationData(
        base_id + 20, TWWFlag.SHRT_SQ, "The Great Sea", 0xB, TWWLocationType.CHEST, 2
    ),
    # "Windfall Island - Lenzo's House - Become Lenzo's Assistant": TWWLocationData(
    #     base_id + 21, TWWFlag.LONG_SQ, "The Great Sea"
    # ),
    # "Windfall Island - Lenzo's House - Bring Forest Firefly": TWWLocationData(
    #     base_id + 22, TWWFlag.LONG_SQ, "The Great Sea"
    # ),
    "Windfall Island - House of Wealth Chest": TWWLocationData(
        base_id + 23, TWWFlag.MISCELL, "The Great Sea", 0xB, TWWLocationType.CHEST, 3
    ),
    # "Windfall Island - Maggie's Father - Give 20 Skull Necklaces": TWWLocationData(
    #     base_id + 24, TWWFlag.SPOILS, "The Great Sea"
    # ),
    "Windfall Island - Maggie - Free Item": TWWLocationData(
        base_id + 25, TWWFlag.FREE_GF, "The Great Sea", 0xB, TWWLocationType.EVENT, 0, 0x803C5296
    ),
    # "Windfall Island - Maggie - Delivery Reward": TWWLocationData(
    #     base_id + 26, TWWFlag.SHRT_SQ, "The Great Sea"
    # ),
    # "Windfall Island - Cafe Bar - Postman": TWWLocationData(
    #     base_id + 27, TWWFlag.SHRT_SQ, "The Great Sea"
    # ),
    "Windfall Island - Kreeb - Light Up Lighthouse": TWWLocationData(
        # TODO: find the flag for the Kreeb item, currently using lit lighthouse flag
        base_id + 28, TWWFlag.SHRT_SQ, "The Great Sea", 0x0, TWWLocationType.SWTCH, 13
    ),
    "Windfall Island - Transparent Chest": TWWLocationData(
        base_id + 29, TWWFlag.SHRT_SQ, "The Great Sea", 0x0, TWWLocationType.CHEST, 10
    ),
    "Windfall Island - Tott - Teach Rhythm": TWWLocationData(
        base_id + 30, TWWFlag.FREE_GF, "The Great Sea", 0x0, TWWLocationType.EVENT, 6, 0x803C5238
    ),
    "Windfall Island - Pirate Ship": TWWLocationData(
        base_id + 31, TWWFlag.MINIGME, "The Great Sea", 0xD, TWWLocationType.CHEST, 5
    ),
    # "Windfall Island - 5 Rupee Auction": TWWLocationData(
    #     base_id + 32, TWWFlag.XPENSVE | TWWFlag.MINIGME, "The Great Sea"
    # ),
    # "Windfall Island - 40 Rupee Auction": TWWLocationData(
    #     base_id + 33, TWWFlag.XPENSVE | TWWFlag.MINIGME, "The Great Sea"
    # ),
    # "Windfall Island - 60 Rupee Auction": TWWLocationData(
    #     base_id + 34, TWWFlag.XPENSVE | TWWFlag.MINIGME, "The Great Sea"
    # ),
    # "Windfall Island - 80 Rupee Auction": TWWLocationData(
    #     base_id + 35, TWWFlag.XPENSVE | TWWFlag.MINIGME, "The Great Sea"
    # ),
    # "Windfall Island - Zunari - Stock Exotic Flower in Zunari's Shop": TWWLocationData(
    #     base_id + 36, TWWFlag.SHRT_SQ, "The Great Sea"
    # ),
    # "Windfall Island - Sam - Decorate the Town": TWWLocationData(
    #     base_id + 37, TWWFlag.LONG_SQ, "The Great Sea"
    # ),
    # "Windfall Island - Kane - Place Shop Guru Statue on Gate": TWWLocationData(
    #     base_id + 38, TWWFlag.OTHER, "The Great Sea"
    # ),
    # "Windfall Island - Kane - Place Postman Statue on Gate": TWWLocationData(
    #     base_id + 39, TWWFlag.OTHER, "The Great Sea"
    # ),
    # "Windfall Island - Kane - Place Six Flags on Gate": TWWLocationData(
    #     base_id + 40, TWWFlag.OTHER, "The Great Sea"
    # ),
    # "Windfall Island - Kane - Place Six Idols on Gate": TWWLocationData(
    #     base_id + 41, TWWFlag.OTHER, "The Great Sea"
    # ),
    # "Windfall Island - Mila - Follow the Thief": TWWLocationData(
    #     base_id + 42, TWWFlag.SHRT_SQ, "The Great Sea"
    # ),
    "Windfall Island - Battlesquid - First Prize": TWWLocationData(
        base_id + 43, TWWFlag.SPLOOSH, "The Great Sea", 0xB, TWWLocationType.EVENT, 0, 0x803C532A
    ),
    "Windfall Island - Battlesquid - Second Prize": TWWLocationData(
        base_id + 44, TWWFlag.SPLOOSH, "The Great Sea", 0xB, TWWLocationType.EVENT, 1, 0x803C532A
    ),
    "Windfall Island - Battlesquid - Under 20 Shots Prize": TWWLocationData(
        base_id + 45, TWWFlag.SPLOOSH, "The Great Sea", 0xB, TWWLocationType.EVENT, 0, 0x803C532B
    ),
    # "Windfall Island - Pompie and Vera - Secret Meeting Photo": TWWLocationData(
    #     base_id + 46, TWWFlag.SHRT_SQ, "The Great Sea"
    # ),
    # "Windfall Island - Kamo - Full Moon Photo": TWWLocationData(
    #     base_id + 47, TWWFlag.LONG_SQ, "The Great Sea"
    # ),
    # "Windfall Island - Minenco - Miss Windfall Photo": TWWLocationData(
    #     base_id + 48, TWWFlag.SHRT_SQ, "The Great Sea"
    # ),
    # "Windfall Island - Linda and Anton": TWWLocationData(
    #     base_id + 49, TWWFlag.LONG_SQ, "The Great Sea"
    # ),

    # Dragon Roost Island
    "Dragon Roost Island - Wind Shrine": TWWLocationData(
        base_id + 50, TWWFlag.MISCELL, "The Great Sea", 0x0, TWWLocationType.SWTCH, 32
    ),
    # "Dragon Roost Island - Rito Aerie - Give Hoskit 20 Golden Feathers": TWWLocationData(
    #     base_id + 51, TWWFlag.SPOILS, "The Great Sea"
    # ),
    "Dragon Roost Island - Chest on Top of Boulder": TWWLocationData(
        base_id + 52, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.CHEST, 8
    ),
    "Dragon Roost Island - Fly Across Platforms Around Island": TWWLocationData(
        base_id + 53, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.CHEST, 9
    ),
    "Dragon Roost Island - Rito Aerie - Mail Sorting": TWWLocationData(
        # TODO: find the flag for the Baito item, currently using bits for mail sorting with Rito postman
        base_id + 54, TWWFlag.MINIGME, "The Great Sea", 0xB, TWWLocationType.SPECL, 0
    ),
    "Dragon Roost Island - Secret Cave": TWWLocationData(
        base_id + 55, TWWFlag.CBT_CVE, "Dragon Roost Island Secret Cave", 0xD, TWWLocationType.CHEST, 0
    ),

    # Dragon Roost Cavern
    "Dragon Roost Cavern - First Room": TWWLocationData(
        base_id + 56, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 0
    ),
    "Dragon Roost Cavern - Alcove With Water Jugs": TWWLocationData(
        base_id + 57, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 2
    ),
    "Dragon Roost Cavern - Water Jug on Upper Shelf": TWWLocationData(
        base_id + 58, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Dragon Roost Cavern", 0x3, TWWLocationType.PCKUP, 1
    ),
    "Dragon Roost Cavern - Boarded Up Chest": TWWLocationData(
        base_id + 59, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 1
    ),
    "Dragon Roost Cavern - Chest Across Lava Pit": TWWLocationData(
        base_id + 60, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 13
    ),
    "Dragon Roost Cavern - Rat Room": TWWLocationData(
        base_id + 61, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 14
    ),
    "Dragon Roost Cavern - Rat Room Boarded Up Chest": TWWLocationData(
        base_id + 62, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 3
    ),
    "Dragon Roost Cavern - Bird's Nest": TWWLocationData(
        base_id + 63, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.PCKUP, 3
    ),
    "Dragon Roost Cavern - Dark Room": TWWLocationData(
        base_id + 64, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 4
    ),
    "Dragon Roost Cavern - Tingle Chest in Hub Room": TWWLocationData(
        base_id + 65, TWWFlag.TNGL_CT | TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 16
    ),
    "Dragon Roost Cavern - Pot on Upper Shelf in Pot Room": TWWLocationData(
        base_id + 66, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Dragon Roost Cavern", 0x3, TWWLocationType.PCKUP, 0
    ),
    "Dragon Roost Cavern - Pot Room Chest": TWWLocationData(
        base_id + 67, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 6
    ),
    "Dragon Roost Cavern - Miniboss": TWWLocationData(
        base_id + 68, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 17
    ),
    "Dragon Roost Cavern - Under Rope Bridge": TWWLocationData(
        base_id + 69, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 7
    ),
    "Dragon Roost Cavern - Tingle Statue Chest": TWWLocationData(
        base_id + 70, TWWFlag.TNGL_CT | TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 15
    ),
    "Dragon Roost Cavern - Big Key Chest": TWWLocationData(
        base_id + 71, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 12
    ),
    "Dragon Roost Cavern - Boss Stairs Right Chest": TWWLocationData(
        base_id + 72, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 11
    ),
    "Dragon Roost Cavern - Boss Stairs Left Chest": TWWLocationData(
        base_id + 73, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 10
    ),
    "Dragon Roost Cavern - Boss Stairs Right Pot": TWWLocationData(
        base_id + 74, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Dragon Roost Cavern", 0x3, TWWLocationType.PCKUP, 6
    ),
    "Dragon Roost Cavern - Gohma Heart Container": TWWLocationData(
        base_id + 75, TWWFlag.DUNGEON, "Gohma Boss Arena", 0x3, TWWLocationType.PCKUP, 21
    ),

    # Forest Haven
    "Forest Haven - On Tree Branch": TWWLocationData(
        base_id + 76, TWWFlag.ISLND_P, "The Great Sea", 0xB, TWWLocationType.PCKUP, 2
    ),
    "Forest Haven - Small Island Chest": TWWLocationData(
        base_id + 77, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.CHEST, 7
    ),

    # Forbidden Woods
    "Forbidden Woods - First Room": TWWLocationData(
        base_id + 78, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 0
    ),
    "Forbidden Woods - Inside Hollow Tree's Mouth": TWWLocationData(
        base_id + 79, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 1
    ),
    "Forbidden Woods - Climb to Top Using Boko Baba Bulbs": TWWLocationData(
        base_id + 80, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 2
    ),
    "Forbidden Woods - Pot High Above Hollow Tree": TWWLocationData(
        base_id + 81, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Forbidden Woods", 0x4, TWWLocationType.PCKUP, 1
    ),
    "Forbidden Woods - Hole in Tree": TWWLocationData(
        base_id + 82, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 6
    ),
    "Forbidden Woods - Morth Pit": TWWLocationData(
        base_id + 83, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 8
    ),
    "Forbidden Woods - Vine Maze Left Chest": TWWLocationData(
        base_id + 84, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 7
    ),
    "Forbidden Woods - Vine Maze Right Chest": TWWLocationData(
        base_id + 85, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 5
    ),
    "Forbidden Woods - Highest Pot in Vine Maze": TWWLocationData(
        base_id + 86, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Forbidden Woods", 0x4, TWWLocationType.PCKUP, 22
    ),
    "Forbidden Woods - Tall Room Before Miniboss": TWWLocationData(
        base_id + 87, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 12
    ),
    "Forbidden Woods - Mothula Miniboss Room": TWWLocationData(
        base_id + 88, TWWFlag.DUNGEON, "Forbidden Woods Miniboss Arena", 0x4, TWWLocationType.CHEST, 10
    ),
    "Forbidden Woods - Past Seeds Hanging by Vines": TWWLocationData(
        base_id + 89, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 3
    ),
    "Forbidden Woods - Chest Across Red Hanging Flower": TWWLocationData(
        base_id + 90, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 11
    ),
    "Forbidden Woods - Tingle Statue Chest": TWWLocationData(
        base_id + 91, TWWFlag.TNGL_CT | TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 15
    ),
    "Forbidden Woods - Chest in Locked Tree Trunk": TWWLocationData(
        base_id + 92, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 9
    ),
    "Forbidden Woods - Big Key Chest": TWWLocationData(
        base_id + 93, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 4
    ),
    "Forbidden Woods - Double Mothula Room": TWWLocationData(
        base_id + 94, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 14
    ),
    "Forbidden Woods - Kalle Demos Heart Container": TWWLocationData(
        base_id + 95, TWWFlag.DUNGEON, "Kalle Demos Boss Arena", 0x4, TWWLocationType.PCKUP, 21
    ),

    # Greatfish Isle
    "Greatfish Isle - Hidden Chest": TWWLocationData(
        base_id + 96, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.CHEST, 6
    ),

    # Tower of the Gods
    "Tower of the Gods - Chest Behind Bombable Walls": TWWLocationData(
        base_id + 97, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 2
    ),
    "Tower of the Gods - Pot Behind Bombable Walls": TWWLocationData(
        base_id + 98, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Tower of the Gods", 0x5, TWWLocationType.PCKUP, 0
    ),
    "Tower of the Gods - Hop Across Floating Boxes": TWWLocationData(
        base_id + 99, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 1
    ),
    "Tower of the Gods - Light Two Torches": TWWLocationData(
        base_id + 100, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 10
    ),
    "Tower of the Gods - Skulls Room Chest": TWWLocationData(
        base_id + 101, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 3
    ),
    "Tower of the Gods - Shoot Eye Above Skulls Room Chest": TWWLocationData(
        base_id + 102, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 9
    ),
    "Tower of the Gods - Tingle Statue Chest": TWWLocationData(
        base_id + 103, TWWFlag.TNGL_CT | TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 15
    ),
    "Tower of the Gods - First Chest Guarded by Armos Knights": TWWLocationData(
        base_id + 104, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 6
    ),
    "Tower of the Gods - Stone Tablet": TWWLocationData(
        base_id + 105, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.SWTCH, 25
    ),
    "Tower of the Gods - Darknut Miniboss Room": TWWLocationData(
        base_id + 106, TWWFlag.DUNGEON, "Tower of the Gods Miniboss Arena", 0x5, TWWLocationType.CHEST, 5
    ),
    "Tower of the Gods - Second Chest Guarded by Armos Knights": TWWLocationData(
        base_id + 107, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 8
    ),
    "Tower of the Gods - Floating Platforms Room": TWWLocationData(
        base_id + 108, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 4
    ),
    "Tower of the Gods - Top of Floating Platforms Room": TWWLocationData(
        base_id + 109, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 11
    ),
    "Tower of the Gods - Eastern Pot in Big Key Chest Room": TWWLocationData(
        base_id + 110, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Tower of the Gods", 0x5, TWWLocationType.PCKUP, 1
    ),
    "Tower of the Gods - Big Key Chest": TWWLocationData(
        base_id + 111, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 0
    ),
    "Tower of the Gods - Gohdan Heart Container": TWWLocationData(
        base_id + 112, TWWFlag.DUNGEON, "Gohdan Boss Arena", 0x5, TWWLocationType.PCKUP, 21
    ),

    # Hyrule
    "Hyrule - Master Sword Chamber": TWWLocationData(
        base_id + 113, TWWFlag.DUNGEON, "Master Sword Chamber", 0x9, TWWLocationType.CHEST, 0
    ),

    # Forsaken Fortress
    "Forsaken Fortress - Phantom Ganon": TWWLocationData(
        base_id + 114, TWWFlag.DUNGEON, "The Great Sea", 0x0, TWWLocationType.CHEST, 16
    ),
    "Forsaken Fortress - Chest Outside Upper Jail Cell": TWWLocationData(
        base_id + 115, TWWFlag.DUNGEON, "The Great Sea", 0x2, TWWLocationType.CHEST, 0
    ),
    "Forsaken Fortress - Chest Inside Lower Jail Cell": TWWLocationData(
        base_id + 116, TWWFlag.DUNGEON, "The Great Sea", 0x2, TWWLocationType.CHEST, 3
    ),
    "Forsaken Fortress - Chest Guarded By Bokoblin": TWWLocationData(
        base_id + 117, TWWFlag.DUNGEON, "The Great Sea", 0x2, TWWLocationType.CHEST, 2
    ),
    "Forsaken Fortress - Chest on Bed": TWWLocationData(
        base_id + 118, TWWFlag.DUNGEON, "The Great Sea", 0x2, TWWLocationType.CHEST, 1
    ),
    "Forsaken Fortress - Helmaroc King Heart Container": TWWLocationData(
        base_id + 119, TWWFlag.DUNGEON, "Helmaroc King Boss Arena", 0x2, TWWLocationType.PCKUP, 21
    ),

    # Mother and Child Isles
    "Mother and Child Isles - Inside Mother Isle": TWWLocationData(
        base_id + 120, TWWFlag.MISCELL, "The Great Sea", 0x0, TWWLocationType.CHEST, 28
    ),

    # Fire Mountain
    "Fire Mountain - Cave - Chest": TWWLocationData(
        base_id + 121, TWWFlag.PZL_CVE | TWWFlag.CBT_CVE, "Fire Mountain Secret Cave", 0xC, TWWLocationType.CHEST, 0
    ),
    "Fire Mountain - Lookout Platform Chest": TWWLocationData(
        base_id + 122, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 1
    ),
    "Fire Mountain - Lookout Platform - Destroy the Cannons": TWWLocationData(
        base_id + 123, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 0
    ),
    "Fire Mountain - Big Octo": TWWLocationData(
        base_id + 124, TWWFlag.BG_OCTO, "The Great Sea", 0x0, TWWLocationType.BOCTO, 0, 0x803C51F0
    ),

    # Ice Ring Isle
    "Ice Ring Isle - Frozen Chest": TWWLocationData(
        base_id + 125, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.CHEST, 18
    ),
    "Ice Ring Isle - Cave - Chest": TWWLocationData(
        base_id + 126, TWWFlag.PZL_CVE, "Ice Ring Isle Secret Cave", 0xC, TWWLocationType.CHEST, 1
    ),
    "Ice Ring Isle - Inner Cave - Chest": TWWLocationData(
        base_id + 127, TWWFlag.PZL_CVE | TWWFlag.CBT_CVE, "Ice Ring Isle Inner Cave", 0xC, TWWLocationType.CHEST, 21
    ),

    # Headstone Island
    "Headstone Island - Top of the Island": TWWLocationData(
        base_id + 128, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.PCKUP, 8
    ),
    "Headstone Island - Submarine": TWWLocationData(
        base_id + 129, TWWFlag.SUBMRIN, "The Great Sea", 0xA, TWWLocationType.CHEST, 4
    ),

    # Earth Temple
    "Earth Temple - Transparent Chest In Warp Pot Room": TWWLocationData(
        base_id + 130, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 0
    ),
    "Earth Temple - Behind Curtain In Warp Pot Room": TWWLocationData(
        base_id + 131, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Earth Temple", 0x6, TWWLocationType.PCKUP, 0
    ),
    "Earth Temple - Transparent Chest in First Crypt": TWWLocationData(
        base_id + 132, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 1
    ),
    "Earth Temple - Chest Behind Destructible Walls": TWWLocationData(
        base_id + 133, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 12
    ),
    "Earth Temple - Chest In Three Blocks Room": TWWLocationData(
        base_id + 134, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 2
    ),
    "Earth Temple - Chest Behind Statues": TWWLocationData(
        base_id + 135, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 3
    ),
    "Earth Temple - Casket in Second Crypt": TWWLocationData(
        base_id + 136, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.PCKUP, 14
    ),
    "Earth Temple - Stalfos Miniboss Room": TWWLocationData(
        base_id + 137, TWWFlag.DUNGEON, "Earth Temple Miniboss Arena", 0x6, TWWLocationType.CHEST, 7
    ),
    "Earth Temple - Tingle Statue Chest": TWWLocationData(
        base_id + 138, TWWFlag.TNGL_CT | TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 15
    ),
    "Earth Temple - End of Foggy Room With Floormasters": TWWLocationData(
        base_id + 139, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 4
    ),
    "Earth Temple - Kill All Floormasters in Foggy Room": TWWLocationData(
        base_id + 140, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 11
    ),
    "Earth Temple - Behind Curtain Next to Hammer Button": TWWLocationData(
        base_id + 141, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Earth Temple", 0x6, TWWLocationType.PCKUP, 1
    ),
    "Earth Temple - Chest in Third Crypt": TWWLocationData(
        base_id + 142, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 5
    ),
    "Earth Temple - Many Mirrors Room Right Chest": TWWLocationData(
        base_id + 143, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 10
    ),
    "Earth Temple - Many Mirrors Room Left Chest": TWWLocationData(
        base_id + 144, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 9
    ),
    "Earth Temple - Stalfos Crypt Room": TWWLocationData(
        base_id + 145, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 14
    ),
    "Earth Temple - Big Key Chest": TWWLocationData(
        base_id + 146, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 6
    ),
    "Earth Temple - Jalhalla Heart Container": TWWLocationData(
        base_id + 147, TWWFlag.DUNGEON, "Jalhalla Boss Arena", 0x6, TWWLocationType.PCKUP, 21
    ),

    # Wind Temple
    "Wind Temple - Chest Between Two Dirt Patches": TWWLocationData(
        base_id + 148, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 0
    ),
    "Wind Temple - Behind Stone Head in Hidden Upper Room": TWWLocationData(
        base_id + 149, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Wind Temple", 0x7, TWWLocationType.PCKUP, 0
    ),
    "Wind Temple - Tingle Statue Chest": TWWLocationData(
        base_id + 150, TWWFlag.TNGL_CT | TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 15
    ),
    "Wind Temple - Chest Behind Stone Head": TWWLocationData(
        base_id + 151, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 3
    ),
    "Wind Temple - Chest in Left Alcove": TWWLocationData(
        base_id + 152, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 7
    ),
    "Wind Temple - Big Key Chest": TWWLocationData(
        base_id + 153, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 8
    ),
    "Wind Temple - Chest In Many Cyclones Room": TWWLocationData(
        base_id + 154, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 11
    ),
    "Wind Temple - Behind Stone Head in Many Cyclones Room": TWWLocationData(
        base_id + 155, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Wind Temple", 0x7, TWWLocationType.PCKUP, 1
    ),
    "Wind Temple - Chest In Middle Of Hub Room": TWWLocationData(
        base_id + 156, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 13
    ),
    "Wind Temple - Spike Wall Room - First Chest": TWWLocationData(
        base_id + 157, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 9
    ),
    "Wind Temple - Spike Wall Room - Destroy All Cracked Floors": TWWLocationData(
        base_id + 158, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 10
    ),
    "Wind Temple - Wizzrobe Miniboss Room": TWWLocationData(
        base_id + 159, TWWFlag.DUNGEON, "Wind Temple Miniboss Arena", 0x7, TWWLocationType.CHEST, 5
    ),
    "Wind Temple - Chest at Top of Hub Room": TWWLocationData(
        base_id + 160, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 2
    ),
    "Wind Temple - Chest Behind Seven Armos": TWWLocationData(
        base_id + 161, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 4
    ),
    "Wind Temple - Kill All Enemies in Tall Basement Room": TWWLocationData(
        base_id + 162, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 12
    ),
    "Wind Temple - Molgera Heart Container": TWWLocationData(
        base_id + 163, TWWFlag.DUNGEON, "Molgera Boss Arena", 0x7, TWWLocationType.PCKUP, 21
    ),

    # Ganon's Tower
    "Ganon's Tower - Maze Chest": TWWLocationData(
        base_id + 164, TWWFlag.DUNGEON, "The Great Sea", 0x8, TWWLocationType.CHEST, 0
    ),

    # Mailbox
    # "Mailbox - Letter from Hoskit's Girlfriend": TWWLocationData(
    #     base_id + 165, TWWFlag.MAILBOX | TWWFlag.SPOILS, "The Great Sea"
    # ),
    # "Mailbox - Letter from Baito's Mother": TWWLocationData(
    #     base_id + 166, TWWFlag.MAILBOX, "The Great Sea"
    # ),
    # "Mailbox - Letter from Baito": TWWLocationData(
    #     base_id + 167, TWWFlag.MAILBOX | TWWFlag.DUNGEON, "The Great Sea"
    # ),
    # "Mailbox - Letter from Komali's Father": TWWLocationData(
    #     base_id + 168, TWWFlag.MAILBOX, "The Great Sea"
    # ),
    # "Mailbox - Letter Advertising Bombs in Beedle's Shop": TWWLocationData(
    #     base_id + 169, TWWFlag.MAILBOX, "The Great Sea"
    # ),
    # "Mailbox - Letter Advertising Rock Spire Shop Ship": TWWLocationData(
    #     base_id + 170, TWWFlag.MAILBOX, "The Great Sea"
    # ),
    # "Mailbox - Beedle's Silver Membership Reward": TWWLocationData(
    #     base_id + 171, TWWFlag.OTHER, "The Great Sea"
    # ),
    # "Mailbox - Beedle's Gold Membership Reward": TWWLocationData(
    #     base_id + 172, TWWFlag.OTHER, "The Great Sea"
    # ),
    # "Mailbox - Letter from Orca": TWWLocationData(
    #     base_id + 173, TWWFlag.MAILBOX | TWWFlag.DUNGEON, "The Great Sea"
    # ),
    # "Mailbox - Letter from Grandma": TWWLocationData(
    #     base_id + 174, TWWFlag.MAILBOX, "The Great Sea"
    # ),
    # "Mailbox - Letter from Aryll": TWWLocationData(
    #     base_id + 175, TWWFlag.MAILBOX | TWWFlag.DUNGEON, "The Great Sea"
    # ),
    # "Mailbox - Letter from Tingle": TWWLocationData(
    #     base_id + 176, TWWFlag.MAILBOX | TWWFlag.DUNGEON | TWWFlag.XPENSVE, "The Great Sea"
    # ),

    # The Great Sea
    # "The Great Sea - Beedle's Shop Ship - 20 Rupee Item": TWWLocationData(
    #     base_id + 177, TWWFlag.MISCELL, "The Great Sea"
    # ),
    "The Great Sea - Salvage Corp Gift": TWWLocationData(
        base_id + 178, TWWFlag.FREE_GF, "The Great Sea", 0x0, TWWLocationType.EVENT, 7, 0x803C5295
    ),
    "The Great Sea - Cyclos": TWWLocationData(
        base_id + 179, TWWFlag.MISCELL, "The Great Sea", 0x0, TWWLocationType.EVENT, 4, 0x803C5253
    ),
    # "The Great Sea - Goron Trading Reward": TWWLocationData(
    #     base_id + 180, TWWFlag.LONG_SQ | TWWFlag.XPENSVE, "The Great Sea"
    # ),
    "The Great Sea - Withered Trees": TWWLocationData(
        base_id + 181, TWWFlag.LONG_SQ, "The Great Sea", 0x0, TWWLocationType.EVENT, 5, 0x803C525A
    ),
    "The Great Sea - Ghost Ship": TWWLocationData(
        base_id + 182, TWWFlag.MISCELL, "The Great Sea", 0xA, TWWLocationType.CHEST, 23
    ),

    # Private Oasis
    "Private Oasis - Chest at Top of Waterfall": TWWLocationData(
        base_id + 183, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.CHEST, 19
    ),
    "Private Oasis - Cabana Labyrinth - Lower Floor Chest": TWWLocationData(
        base_id + 184, TWWFlag.PZL_CVE, "Cabana Labyrinth", 0xC, TWWLocationType.CHEST, 22
    ),
    "Private Oasis - Cabana Labyrinth - Upper Floor Chest": TWWLocationData(
        base_id + 185, TWWFlag.PZL_CVE, "Cabana Labyrinth", 0xC, TWWLocationType.CHEST, 17
    ),
    "Private Oasis - Big Octo": TWWLocationData(
        base_id + 186, TWWFlag.BG_OCTO, "The Great Sea", 0x0, TWWLocationType.BOCTO, 0, 0x803C520A
    ),

    # Spectacle Island
    # "Spectacle Island - Barrel Shooting - First Prize": TWWLocationData(
    #     base_id + 187, TWWFlag.MINIGME, "The Great Sea"
    # ),
    # "Spectacle Island - Barrel Shooting - Second Prize": TWWLocationData(
    #     base_id + 188, TWWFlag.MINIGME, "The Great Sea"
    # ),

    # Needle Rock Isle
    "Needle Rock Isle - Chest": TWWLocationData(
        base_id + 189, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.CHEST, 3
    ),
    "Needle Rock Isle - Cave": TWWLocationData(
        base_id + 190, TWWFlag.PZL_CVE, "Needle Rock Isle Secret Cave", 0xD, TWWLocationType.CHEST, 9
    ),
    "Needle Rock Isle - Golden Gunboat": TWWLocationData(
        base_id + 191, TWWFlag.BG_OCTO, "The Great Sea", 0x0, TWWLocationType.BOCTO, 2, 0x803C5202
    ),

    # Angular Isles
    "Angular Isles - Peak": TWWLocationData(
        base_id + 192, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.CHEST, 0
    ),
    "Angular Isles - Cave": TWWLocationData(
        base_id + 193, TWWFlag.PZL_CVE, "Angular Isles Secret Cave", 0xD, TWWLocationType.CHEST, 6
    ),

    # Boating Course
    "Boating Course - Raft": TWWLocationData(
        base_id + 194, TWWFlag.PLTFRMS, "The Great Sea", 0x0, TWWLocationType.CHEST, 21
    ),
    "Boating Course - Cave": TWWLocationData(
        base_id + 195, TWWFlag.PZL_CVE | TWWFlag.CBT_CVE, "Boating Course Secret Cave", 0xD, TWWLocationType.CHEST, 15
    ),

    # Stone Watcher Island
    "Stone Watcher Island - Cave": TWWLocationData(
        base_id + 196, TWWFlag.CBT_CVE, "Stone Watcher Island Secret Cave", 0xC, TWWLocationType.CHEST, 10
    ),
    "Stone Watcher Island - Lookout Platform Chest": TWWLocationData(
        base_id + 197, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 18
    ),
    "Stone Watcher Island - Lookout Platform - Destroy the Cannons": TWWLocationData(
        base_id + 198, TWWFlag.PLTFRMS, "The Great Sea", 0x0, TWWLocationType.CHEST, 20
    ),

    # Islet of Steel
    "Islet of Steel - Interior": TWWLocationData(
        base_id + 199, TWWFlag.MISCELL, "The Great Sea", 0xC, TWWLocationType.CHEST, 4
    ),
    "Islet of Steel - Lookout Platform - Defeat the Enemies": TWWLocationData(
        base_id + 200, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 16
    ),

    # Overlook Island
    "Overlook Island - Cave": TWWLocationData(
        base_id + 201, TWWFlag.CBT_CVE, "Overlook Island Secret Cave", 0xC, TWWLocationType.CHEST, 11
    ),

    # Bird's Peak Rock
    "Bird's Peak Rock - Cave": TWWLocationData(
        base_id + 202, TWWFlag.PZL_CVE, "Bird's Peak Rock Secret Cave", 0xC, TWWLocationType.CHEST, 16
    ),

    # Pawprint Isle
    "Pawprint Isle - Chuchu Cave - Chest": TWWLocationData(
        base_id + 203, TWWFlag.PZL_CVE, "Pawprint Isle Chuchu Cave", 0xC, TWWLocationType.CHEST, 26
    ),
    "Pawprint Isle - Chuchu Cave - Behind Left Boulder": TWWLocationData(
        base_id + 204, TWWFlag.PZL_CVE, "Pawprint Isle Chuchu Cave", 0xC, TWWLocationType.CHEST, 24
    ),
    "Pawprint Isle - Chuchu Cave - Behind Right Boulder": TWWLocationData(
        base_id + 205, TWWFlag.PZL_CVE, "Pawprint Isle Chuchu Cave", 0xC, TWWLocationType.CHEST, 25
    ),
    "Pawprint Isle - Chuchu Cave - Scale the Wall": TWWLocationData(
        base_id + 206, TWWFlag.PZL_CVE, "Pawprint Isle Chuchu Cave", 0xC, TWWLocationType.CHEST, 2
    ),
    "Pawprint Isle - Wizzrobe Cave": TWWLocationData(
        base_id + 207, TWWFlag.CBT_CVE, "Pawprint Isle Wizzrobe Cave", 0xD, TWWLocationType.CHEST, 2
    ),
    "Pawprint Isle - Lookout Platform - Defeat the Enemies": TWWLocationData(
        base_id + 208, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 5
    ),

    # Thorned Fairy Island
    # "Thorned Fairy Island - Great Fairy": TWWLocationData(
    #     base_id + 209, TWWFlag.GRT_FRY, "Thorned Fairy Fountain"
    # ),
    "Thorned Fairy Island - Northeastern Lookout Platform - Destroy the Cannons": TWWLocationData(
        base_id + 210, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 14
    ),
    "Thorned Fairy Island - Southwestern Lookout Platform - Defeat the Enemies": TWWLocationData(
        base_id + 211, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 15
    ),

    # Eastern Fairy Island
    # "Eastern Fairy Island - Great Fairy": TWWLocationData(
    #     base_id + 212, TWWFlag.GRT_FRY, "Eastern Fairy Fountain"
    # ),
    "Eastern Fairy Island - Lookout Platform - Defeat the Cannons and Enemies": TWWLocationData(
        base_id + 213, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 10
    ),

    # Western Fairy Island
    # "Western Fairy Island - Great Fairy": TWWLocationData(
    #     base_id + 214, TWWFlag.GRT_FRY, "Western Fairy Fountain"
    # ),
    "Western Fairy Island - Lookout Platform": TWWLocationData(
        base_id + 215, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 6
    ),

    # Southern Fairy Island
    # "Southern Fairy Island - Great Fairy": TWWLocationData(
    #     base_id + 216, TWWFlag.GRT_FRY, "Southern Fairy Fountain"
    # ),
    "Southern Fairy Island - Lookout Platform - Destroy the Northwest Cannons": TWWLocationData(
        base_id + 217, TWWFlag.PLTFRMS, "The Great Sea", 0x0, TWWLocationType.CHEST, 23
    ),
    "Southern Fairy Island - Lookout Platform - Destroy the Southeast Cannons": TWWLocationData(
        base_id + 218, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 17
    ),

    # Northern Fairy Island
    # "Northern Fairy Island - Great Fairy": TWWLocationData(
    #     base_id + 219, TWWFlag.GRT_FRY, "Northern Fairy Fountain"
    # ),
    "Northern Fairy Island - Submarine": TWWLocationData(
        base_id + 220, TWWFlag.SUBMRIN, "The Great Sea", 0xA, TWWLocationType.CHEST, 6
    ),

    # Tingle Island
    # "Tingle Island - Ankle - Reward for All Tingle Statues": TWWLocationData(
    #     base_id + 221, TWWFlag.MISCELL, "The Great Sea"
    # ),
    "Tingle Island - Big Octo": TWWLocationData(
        base_id + 222, TWWFlag.BG_OCTO, "The Great Sea", 0x0, TWWLocationType.BOCTO, 0, 0x803C51EA
    ),

    # Diamond Steppe Island
    "Diamond Steppe Island - Warp Maze Cave - First Chest": TWWLocationData(
        base_id + 223, TWWFlag.PZL_CVE, "Diamond Steppe Island Warp Maze Cave", 0xC, TWWLocationType.CHEST, 23
    ),
    "Diamond Steppe Island - Warp Maze Cave - Second Chest": TWWLocationData(
        base_id + 224, TWWFlag.PZL_CVE, "Diamond Steppe Island Warp Maze Cave", 0xC, TWWLocationType.CHEST, 3
    ),
    "Diamond Steppe Island - Big Octo": TWWLocationData(
        base_id + 225, TWWFlag.BG_OCTO, "The Great Sea", 0x0, TWWLocationType.BOCTO, 0, 0x803C5210
    ),

    # Bomb Island
    "Bomb Island - Cave": TWWLocationData(
        base_id + 226, TWWFlag.PZL_CVE, "Bomb Island Secret Cave", 0xC, TWWLocationType.CHEST, 5
    ),
    "Bomb Island - Lookout Platform - Defeat the Enemies": TWWLocationData(
        base_id + 227, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 3
    ),
    "Bomb Island - Submarine": TWWLocationData(
        base_id + 228, TWWFlag.SUBMRIN, "The Great Sea", 0xA, TWWLocationType.CHEST, 2
    ),

    # Rock Spire Isle
    "Rock Spire Isle - Cave": TWWLocationData(
        base_id + 229, TWWFlag.CBT_CVE, "Rock Spire Isle Secret Cave", 0xC, TWWLocationType.CHEST, 8
    ),
    "Rock Spire Isle - Beedle's Special Shop Ship - 500 Rupee Item": TWWLocationData(
        base_id + 230, TWWFlag.XPENSVE, "The Great Sea", 0xA, TWWLocationType.EVENT, 5, 0x803C524C
    ),
    "Rock Spire Isle - Beedle's Special Shop Ship - 950 Rupee Item": TWWLocationData(
        base_id + 231, TWWFlag.XPENSVE, "The Great Sea", 0xA, TWWLocationType.EVENT, 4, 0x803C524C
    ),
    "Rock Spire Isle - Beedle's Special Shop Ship - 900 Rupee Item": TWWLocationData(
        base_id + 232, TWWFlag.XPENSVE, "The Great Sea", 0xA, TWWLocationType.EVENT, 3, 0x803C524C
    ),
    "Rock Spire Isle - Western Lookout Platform - Destroy the Cannons": TWWLocationData(
        base_id + 233, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 23
    ),
    "Rock Spire Isle - Eastern Lookout Platform - Destroy the Cannons": TWWLocationData(
        base_id + 234, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 24
    ),
    "Rock Spire Isle - Center Lookout Platform": TWWLocationData(
        base_id + 235, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 25
    ),
    "Rock Spire Isle - Southeast Gunboat": TWWLocationData(
        base_id + 236, TWWFlag.BG_OCTO, "The Great Sea", 0x0, TWWLocationType.BOCTO, 0, 0x803C51E8
    ),

    # Shark Island
    "Shark Island - Cave": TWWLocationData(
        base_id + 237, TWWFlag.CBT_CVE, "Shark Island Secret Cave", 0xD, TWWLocationType.CHEST, 22
    ),

    # Cliff Plateau Isles
    "Cliff Plateau Isles - Cave": TWWLocationData(
        base_id + 238, TWWFlag.PZL_CVE, "Cliff Plateau Isles Secret Cave", 0xC, TWWLocationType.CHEST, 7
    ),
    "Cliff Plateau Isles - Highest Isle": TWWLocationData(
        base_id + 239, TWWFlag.PZL_CVE, "Cliff Plateau Isles Inner Cave", 0x0, TWWLocationType.CHEST, 1
    ),
    "Cliff Plateau Isles - Lookout Platform": TWWLocationData(
        base_id + 240, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 19
    ),

    # Crescent Moon Island
    "Crescent Moon Island - Chest": TWWLocationData(
        base_id + 241, TWWFlag.MISCELL, "The Great Sea", 0x0, TWWLocationType.CHEST, 4
    ),
    "Crescent Moon Island - Submarine": TWWLocationData(
        base_id + 242, TWWFlag.SUBMRIN, "The Great Sea", 0xA, TWWLocationType.CHEST, 7
    ),

    # Horseshoe Island
    "Horseshoe Island - Play Golf": TWWLocationData(
        base_id + 243, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.CHEST, 5
    ),
    "Horseshoe Island - Cave": TWWLocationData(
        base_id + 244, TWWFlag.CBT_CVE, "Horseshoe Island Secret Cave", 0xD, TWWLocationType.CHEST, 1
    ),
    "Horseshoe Island - Northwestern Lookout Platform": TWWLocationData(
        base_id + 245, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 26
    ),
    "Horseshoe Island - Southeastern Lookout Platform": TWWLocationData(
        base_id + 246, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 27
    ),

    # Flight Control Platform
    # "Flight Control Platform - Bird-Man Contest - First Prize": TWWLocationData(
    #     base_id + 247, TWWFlag.MINIGME, "The Great Sea"
    # ),
    "Flight Control Platform - Submarine": TWWLocationData(
        base_id + 248, TWWFlag.SUBMRIN, "The Great Sea", 0xA, TWWLocationType.CHEST, 3
    ),

    # Star Island
    "Star Island - Cave": TWWLocationData(
        base_id + 249, TWWFlag.CBT_CVE, "Star Island Secret Cave", 0xC, TWWLocationType.CHEST, 6
    ),
    "Star Island - Lookout Platform": TWWLocationData(
        base_id + 250, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 4
    ),

    # Star Belt Archipelago
    "Star Belt Archipelago - Lookout Platform": TWWLocationData(
        base_id + 251, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 11
    ),

    # Five-Star Isles
    "Five-Star Isles - Lookout Platform - Destroy the Cannons": TWWLocationData(
        base_id + 252, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 2
    ),
    "Five-Star Isles - Raft": TWWLocationData(
        base_id + 253, TWWFlag.PLTFRMS, "The Great Sea", 0x0, TWWLocationType.CHEST, 2
    ),
    "Five-Star Isles - Submarine": TWWLocationData(
        base_id + 254, TWWFlag.SUBMRIN, "The Great Sea", 0xA, TWWLocationType.CHEST, 1
    ),

    # Seven-Star Isles
    "Seven-Star Isles - Center Lookout Platform": TWWLocationData(
        base_id + 255, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 8
    ),
    "Seven-Star Isles - Northern Lookout Platform": TWWLocationData(
        base_id + 256, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 7
    ),
    "Seven-Star Isles - Southern Lookout Platform": TWWLocationData(
        base_id + 257, TWWFlag.PLTFRMS, "The Great Sea", 0x0, TWWLocationType.CHEST, 22
    ),
    "Seven-Star Isles - Big Octo": TWWLocationData(
        base_id + 258, TWWFlag.BG_OCTO, "The Great Sea", 0x0, TWWLocationType.BOCTO, 0, 0x803C51D4
    ),

    # Cyclops Reef
    "Cyclops Reef - Destroy the Cannons and Gunboats": TWWLocationData(
        base_id + 259, TWWFlag.EYE_RFS, "The Great Sea", 0x0, TWWLocationType.CHEST, 11
    ),
    "Cyclops Reef - Lookout Platform - Defeat the Enemies": TWWLocationData(
        base_id + 260, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 12
    ),

    # Two-Eye Reef
    "Two-Eye Reef - Destroy the Cannons and Gunboats": TWWLocationData(
        base_id + 261, TWWFlag.EYE_RFS, "The Great Sea", 0x0, TWWLocationType.CHEST, 13
    ),
    "Two-Eye Reef - Lookout Platform": TWWLocationData(
        base_id + 262, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 21
    ),
    "Two-Eye Reef - Big Octo Great Fairy": TWWLocationData(
        base_id + 263, TWWFlag.BG_OCTO | TWWFlag.GRT_FRY, "The Great Sea", 0x0, TWWLocationType.SWTCH, 52
    ),

    # Three-Eye Reef
    "Three-Eye Reef - Destroy the Cannons and Gunboats": TWWLocationData(
        base_id + 264, TWWFlag.EYE_RFS, "The Great Sea", 0x0, TWWLocationType.CHEST, 12
    ),

    # Four-Eye Reef
    "Four-Eye Reef - Destroy the Cannons and Gunboats": TWWLocationData(
        base_id + 265, TWWFlag.EYE_RFS, "The Great Sea", 0x0, TWWLocationType.CHEST, 14
    ),

    # Five-Eye Reef
    "Five-Eye Reef - Destroy the Cannons": TWWLocationData(
        base_id + 266, TWWFlag.EYE_RFS, "The Great Sea", 0x0, TWWLocationType.CHEST, 15
    ),
    "Five-Eye Reef - Lookout Platform": TWWLocationData(
        base_id + 267, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 20
    ),

    # Six-Eye Reef
    "Six-Eye Reef - Destroy the Cannons and Gunboats": TWWLocationData(
        base_id + 268, TWWFlag.EYE_RFS, "The Great Sea", 0x0, TWWLocationType.CHEST, 17
    ),
    "Six-Eye Reef - Lookout Platform - Destroy the Cannons": TWWLocationData(
        base_id + 269, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 13
    ),
    "Six-Eye Reef - Submarine": TWWLocationData(
        base_id + 270, TWWFlag.SUBMRIN, "The Great Sea", 0xA, TWWLocationType.CHEST, 0
    ),

    # Sunken Treasure
    "Forsaken Fortress Sector - Sunken Treasure": TWWLocationData(
        base_id + 271, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 8
    ),
    "Star Island - Sunken Treasure": TWWLocationData(
        base_id + 272, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 18
    ),
    "Northern Fairy Island - Sunken Treasure": TWWLocationData(
        base_id + 273, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 51
    ),
    "Gale Isle - Sunken Treasure": TWWLocationData(
        base_id + 274, TWWFlag.TRI_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 33
    ),
    "Crescent Moon Island - Sunken Treasure": TWWLocationData(
        base_id + 275, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 40
    ),
    "Seven-Star Isles - Sunken Treasure": TWWLocationData(
        base_id + 276, TWWFlag.TRI_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 38
    ),
    "Overlook Island - Sunken Treasure": TWWLocationData(
        base_id + 277, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 15
    ),
    "Four-Eye Reef - Sunken Treasure": TWWLocationData(
        base_id + 278, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 12
    ),
    "Mother and Child Isles - Sunken Treasure": TWWLocationData(
        base_id + 279, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 56
    ),
    "Spectacle Island - Sunken Treasure": TWWLocationData(
        base_id + 280, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 5
    ),
    "Windfall Island - Sunken Treasure": TWWLocationData(
        base_id + 281, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 58
    ),
    "Pawprint Isle - Sunken Treasure": TWWLocationData(
        base_id + 282, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 42
    ),
    "Dragon Roost Island - Sunken Treasure": TWWLocationData(
        base_id + 283, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 50
    ),
    "Flight Control Platform - Sunken Treasure": TWWLocationData(
        base_id + 284, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 13
    ),
    "Western Fairy Island - Sunken Treasure": TWWLocationData(
        base_id + 285, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 10
    ),
    "Rock Spire Isle - Sunken Treasure": TWWLocationData(
        base_id + 286, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 48
    ),
    "Tingle Island - Sunken Treasure": TWWLocationData(
        base_id + 287, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 0
    ),
    "Northern Triangle Island - Sunken Treasure": TWWLocationData(
        base_id + 288, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 11
    ),
    "Eastern Fairy Island - Sunken Treasure": TWWLocationData(
        base_id + 289, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 62
    ),
    "Fire Mountain - Sunken Treasure": TWWLocationData(
        base_id + 290, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 9
    ),
    "Star Belt Archipelago - Sunken Treasure": TWWLocationData(
        base_id + 291, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 17
    ),
    "Three-Eye Reef - Sunken Treasure": TWWLocationData(
        base_id + 292, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 49
    ),
    "Greatfish Isle - Sunken Treasure": TWWLocationData(
        base_id + 293, TWWFlag.TRI_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 32
    ),
    "Cyclops Reef - Sunken Treasure": TWWLocationData(
        base_id + 294, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 16
    ),
    "Six-Eye Reef - Sunken Treasure": TWWLocationData(
        base_id + 295, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 52
    ),
    "Tower of the Gods Sector - Sunken Treasure": TWWLocationData(
        base_id + 296, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 1
    ),
    "Eastern Triangle Island - Sunken Treasure": TWWLocationData(
        base_id + 297, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 57
    ),
    "Thorned Fairy Island - Sunken Treasure": TWWLocationData(
        base_id + 298, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 44
    ),
    "Needle Rock Isle - Sunken Treasure": TWWLocationData(
        base_id + 299, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 60
    ),
    "Islet of Steel - Sunken Treasure": TWWLocationData(
        base_id + 300, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 54
    ),
    "Stone Watcher Island - Sunken Treasure": TWWLocationData(
        base_id + 301, TWWFlag.TRI_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 34
    ),
    "Southern Triangle Island - Sunken Treasure": TWWLocationData(
        base_id + 302, TWWFlag.TRI_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 37
    ),
    "Private Oasis - Sunken Treasure": TWWLocationData(
        base_id + 303, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 55
    ),
    "Bomb Island - Sunken Treasure": TWWLocationData(
        base_id + 304, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 43
    ),
    "Bird's Peak Rock - Sunken Treasure": TWWLocationData(
        base_id + 305, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 6
    ),
    "Diamond Steppe Island - Sunken Treasure": TWWLocationData(
        base_id + 306, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 45
    ),
    "Five-Eye Reef - Sunken Treasure": TWWLocationData(
        base_id + 307, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 53
    ),
    "Shark Island - Sunken Treasure": TWWLocationData(
        base_id + 308, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 59
    ),
    "Southern Fairy Island - Sunken Treasure": TWWLocationData(
        base_id + 309, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 61
    ),
    "Ice Ring Isle - Sunken Treasure": TWWLocationData(
        base_id + 310, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 7
    ),
    "Forest Haven - Sunken Treasure": TWWLocationData(
        base_id + 311, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 46
    ),
    "Cliff Plateau Isles - Sunken Treasure": TWWLocationData(
        base_id + 312, TWWFlag.TRI_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 36
    ),
    "Horseshoe Island - Sunken Treasure": TWWLocationData(
        base_id + 313, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 4
    ),
    "Outset Island - Sunken Treasure": TWWLocationData(
        base_id + 314, TWWFlag.TRI_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 35
    ),
    "Headstone Island - Sunken Treasure": TWWLocationData(
        base_id + 315, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 63
    ),
    "Two-Eye Reef - Sunken Treasure": TWWLocationData(
        base_id + 316, TWWFlag.TRI_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 39
    ),
    "Angular Isles - Sunken Treasure": TWWLocationData(
        base_id + 317, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 41
    ),
    "Boating Course - Sunken Treasure": TWWLocationData(
        base_id + 318, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 14
    ),
    "Five-Star Isles - Sunken Treasure": TWWLocationData(
        base_id + 319, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 47
    ),

    # Defeat Ganondorf
    "Defeat Ganondorf": TWWLocationData(
        None, TWWFlag.ALWAYS, "The Great Sea", 0x8, TWWLocationType.SWTCH, 64
    ),
}

VANILLA_DUNGEON_ITEM_LOCATIONS: dict[str, list[str]] = {
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

    "DRC Big Key": ["Dragon Roost Cavern - Big Key Chest"],
    "FW Big Key": ["Forbidden Woods - Big Key Chest"],
    "TotG Big Key": ["Tower of the Gods - Big Key Chest"],
    "ET Big Key": ["Earth Temple - Big Key Chest"],
    "WT Big Key": ["Wind Temple - Big Key Chest"],

    "DRC Dungeon Map": ["Dragon Roost Cavern - Alcove With Water Jugs"],
    "FW Dungeon Map": ["Forbidden Woods - First Room"],
    "TotG Dungeon Map": ["Tower of the Gods - Chest Behind Bombable Walls"],
    "FF Dungeon Map": ["Forsaken Fortress - Chest Outside Upper Jail Cell"],
    "ET Dungeon Map": ["Earth Temple - Transparent Chest In Warp Pot Room"],
    "WT Dungeon Map": ["Wind Temple - Chest In Many Cyclones Room"],

    "DRC Compass": ["Dragon Roost Cavern - Rat Room"],
    "FW Compass": ["Forbidden Woods - Vine Maze Left Chest"],
    "TotG Compass": ["Tower of the Gods - Skulls Room Chest"],
    "FF Compass": ["Forsaken Fortress - Chest Guarded By Bokoblin"],
    "ET Compass": ["Earth Temple - Chest In Three Blocks Room"],
    "WT Compass": ["Wind Temple - Chest In Middle Of Hub Room"],
}

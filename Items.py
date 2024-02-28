from typing import NamedTuple

from BaseClasses import Item
from BaseClasses import ItemClassification as IC


class TWWItemData(NamedTuple):
    type: str
    classification: IC
    code: int | None
    quantity: int
    address: int | None
    value: int | None
    owned_bitfield: int | None
    bit_to_set: int | None


class TWWItem(Item):
    game: str = "The Wind Waker"

    def __init__(self, name: str, player: int, data: TWWItemData, force_nonprogress: bool):
        super(TWWItem, self).__init__(name, IC.useful if force_nonprogress else data.classification, data.code, player)
        self.type = data.type
        self.address = data.address
        self.value = data.value
        self.owned_bitfield = data.owned_bitfield
        self.bit_to_set = data.bit_to_set


base_id: int = 2322432

ITEM_TABLE: dict[str, TWWItemData] = {
    "Telescope":               TWWItemData("Item",   IC.useful,      base_id +   0, 1, 0x803C4C44, 0x20, 0x803C4C59, 0),
  # "Boat's Sail":             TWWItemData("Item",   IC.progression, base_id +   1, 1, 0x803C4C45, 0x78, 0x803C4C5A, 0),
    "Wind Waker":              TWWItemData("Item",   IC.progression, base_id +   2, 1, 0x803C4C46, 0x22, 0x803C4C5B, 0),
    "Grappling Hook":          TWWItemData("Item",   IC.progression, base_id +   3, 1, 0x803C4C47, 0x25, 0x803C4C5C, 0),
    "Spoils Bag":              TWWItemData("Item",   IC.progression, base_id +   4, 1, 0x803C4C48, 0x24, 0x803C4C5D, 0),
    "Boomerang":               TWWItemData("Item",   IC.progression, base_id +   5, 1, 0x803C4C49, 0x2D, 0x803C4C5E, 0),
    "Deku Leaf":               TWWItemData("Item",   IC.progression, base_id +   6, 1, 0x803C4C4A, 0x34, 0x803C4C5F, 0),
    "Tingle Tuner":            TWWItemData("Item",   IC.progression, base_id +   7, 1, 0x803C4C4B, 0x21, 0x803C4C60, 0),
    "Iron Boots":              TWWItemData("Item",   IC.progression, base_id +   8, 1, 0x803C4C4D, 0x29, 0x803C4C62, 0),
    "Magic Armor":             TWWItemData("Item",   IC.progression, base_id +   9, 1, 0x803C4C4E, 0x2A, 0x803C4C63, 0),
    "Bait Bag":                TWWItemData("Item",   IC.progression, base_id +  10, 1, 0x803C4C4F, 0x2C, 0x803C4C64, 0),
    "Bombs":                   TWWItemData("Item",   IC.progression, base_id +  11, 1, 0x803C4C51, 0x31, 0x803C4C66, 0),
    "Delivery Bag":            TWWItemData("Item",   IC.progression, base_id +  12, 1, 0x803C4C56, 0x30, 0x803C4C6B, 0),
    "Hookshot":                TWWItemData("Item",   IC.progression, base_id +  13, 1, 0x803C4C57, 0x2F, 0x803C4C6C, 0),
    "Skull Hammer":            TWWItemData("Item",   IC.progression, base_id +  14, 1, 0x803C4C58, 0x33, 0x803C4C6D, 0),
    "Power Bracelets":         TWWItemData("Item",   IC.progression, base_id +  15, 1, 0x803C4C18, 0x28, 0x803C4CBE, 0),

    "Hero's Charm":            TWWItemData("Item",   IC.useful,      base_id +  16, 1, None,       None, 0x803C4CC0, 0),
    "Hurricane Spin":          TWWItemData("Item",   IC.useful,      base_id +  17, 1, None,       None, 0x803C5295, 0),
    "Dragon Tingle Statue":    TWWItemData("Item",   IC.progression, base_id +  18, 1, None,       None, 0x803C5296, 2),
    "Forbidden Tingle Statue": TWWItemData("Item",   IC.progression, base_id +  19, 1, None,       None, 0x803C5296, 3),
    "Goddess Tingle Statue":   TWWItemData("Item",   IC.progression, base_id +  20, 1, None,       None, 0x803C5296, 4),
    "Earth Tingle Statue":     TWWItemData("Item",   IC.progression, base_id +  21, 1, None,       None, 0x803C5296, 5),
    "Wind Tingle Statue":      TWWItemData("Item",   IC.progression, base_id +  22, 1, None,       None, 0x803C5296, 6),

    "Wind's Requiem":          TWWItemData("Item",   IC.progression, base_id +  23, 1, None,       None, 0x803C4CC5, 0),
    "Ballad of Gales":         TWWItemData("Item",   IC.progression, base_id +  24, 1, None,       None, 0x803C4CC5, 1),
    "Command Melody":          TWWItemData("Item",   IC.progression, base_id +  25, 1, None,       None, 0x803C4CC5, 2),
    "Earth God's Lyric":       TWWItemData("Item",   IC.progression, base_id +  26, 1, None,       None, 0x803C4CC5, 3),
    "Wind God's Aria":         TWWItemData("Item",   IC.progression, base_id +  27, 1, None,       None, 0x803C4CC5, 4),
    "Song of Passing":         TWWItemData("Item",   IC.progression, base_id +  28, 1, None,       None, 0x803C4CC5, 5),

    "Triforce Shard 1":        TWWItemData("Item",   IC.progression, base_id +  29, 1, None,       None, 0x803C4CC6, 0),
    "Triforce Shard 2":        TWWItemData("Item",   IC.progression, base_id +  30, 1, None,       None, 0x803C4CC6, 1),
    "Triforce Shard 3":        TWWItemData("Item",   IC.progression, base_id +  31, 1, None,       None, 0x803C4CC6, 2),
    "Triforce Shard 4":        TWWItemData("Item",   IC.progression, base_id +  32, 1, None,       None, 0x803C4CC6, 3),
    "Triforce Shard 5":        TWWItemData("Item",   IC.progression, base_id +  33, 1, None,       None, 0x803C4CC6, 4),
    "Triforce Shard 6":        TWWItemData("Item",   IC.progression, base_id +  34, 1, None,       None, 0x803C4CC6, 5),
    "Triforce Shard 7":        TWWItemData("Item",   IC.progression, base_id +  35, 1, None,       None, 0x803C4CC6, 6),
    "Triforce Shard 8":        TWWItemData("Item",   IC.progression, base_id +  36, 1, None,       None, 0x803C4CC6, 7),

    "Skull Necklace":          TWWItemData("Spoil",  IC.filler,      base_id +  37, 9, 0x803C4CA4, 0x45, None,    None),
    "Boko Baba Seed":          TWWItemData("Spoil",  IC.filler,      base_id +  38, 1, 0x803C4CA5, 0x46, None,    None),
    "Golden Feather":          TWWItemData("Spoil",  IC.filler,      base_id +  39, 9, 0x803C4CA6, 0x47, None,    None),
    "Knight's Crest":          TWWItemData("Spoil",  IC.filler,      base_id +  40, 3, 0x803C4CA7, 0x48, None,    None),
    "Red Chu Jelly":           TWWItemData("Spoil",  IC.filler,      base_id +  41, 1, 0x803C4CA8, 0x49, None,    None),
    "Green Chu Jelly":         TWWItemData("Spoil",  IC.filler,      base_id +  42, 1, 0x803C4CA9, 0x4A, None,    None),
    "Joy Pendant":             TWWItemData("Spoil",  IC.filler,      base_id +  43, 9, 0x803C4CAB, 0x1F, None,    None),

    "All-Purpose Bait":        TWWItemData("Bait",   IC.filler,      base_id +  44, 1, None,       0x82, None,    None),
    "Hyoi Pear":               TWWItemData("Bait",   IC.useful,      base_id +  45, 4, None,       0x83, None,    None),

    "Note to Mom":             TWWItemData("Letter", IC.progression, base_id +  46, 1, None,       0x99, None,      13),
    "Maggie's Letter":         TWWItemData("Letter", IC.progression, base_id +  47, 1, None,       0x9A, None,      14),
    "Moblin's Letter":         TWWItemData("Letter", IC.progression, base_id +  48, 1, None,       0x9B, None,      15),
    "Cabana Deed":             TWWItemData("Letter", IC.progression, base_id +  49, 1, None,       0x9C, None,      16),
    "Fill-Up Coupon":          TWWItemData("Letter", IC.useful,      base_id +  50, 1, None,       0x9E, None,      18),

    "Nayru's Pearl":           TWWItemData("Pearl",  IC.progression, base_id +  51, 1, 0x803C5240, 0x10, 0x803C4CC7, 0),
    "Din's Pearl":             TWWItemData("Pearl",  IC.progression, base_id +  52, 1, 0x803C5240, 0x40, 0x803C4CC7, 1),
    "Farore's Pearl":          TWWItemData("Pearl",  IC.progression, base_id +  53, 1, 0x803C5240, 0x80, 0x803C4CC7, 2),

    "Progressive Sword":       TWWItemData("Prog", IC.progression, base_id + 54, 4, 0x803C4C16, None, 0x803C4CBC, None),
    "Progressive Shield":      TWWItemData("Prog", IC.progression, base_id + 55, 2, 0x803C4C17, None, 0x803C4CBD, None),
    "Progressive Picto Box":   TWWItemData("Prog", IC.progression, base_id + 56, 2, 0x803C4C4C, None, 0x803C4C61, None),
    "Progressive Bow":         TWWItemData("Prog", IC.progression, base_id + 57, 3, 0x803C4C50, None, 0x803C4C65, None),
    "Progressive Magic Meter": TWWItemData("Prog", IC.progression, base_id + 58, 2, 0x803C4C1B, None, 0x803C4C1C, None),
    "Progressive Quiver":      TWWItemData("Prog", IC.progression, base_id + 59, 2, 0x803C4C77, None, 0x803C4C71, None),
    "Progressive Bomb Bag":    TWWItemData("Prog", IC.progression, base_id + 60, 2, 0x803C4C78, None, 0x803C4C72, None),
    "Progressive Wallet":      TWWItemData("Prog", IC.progression, base_id + 61, 2, None,       None, None,       None),
    "Empty Bottle":            TWWItemData("Prog", IC.progression, base_id + 62, 4, None,       None, None,       None),

    "Triforce Chart 1": TWWItemData("Chart", IC.progression_skip_balancing, base_id +  63, 1, None,None,0x803C4CDC,  0),
    "Triforce Chart 2": TWWItemData("Chart", IC.progression_skip_balancing, base_id +  64, 1, None,None,0x803C4CDC,  1),
    "Triforce Chart 3": TWWItemData("Chart", IC.progression_skip_balancing, base_id +  65, 1, None,None,0x803C4CDC,  2),
    "Triforce Chart 4": TWWItemData("Chart", IC.progression_skip_balancing, base_id +  66, 1, None,None,0x803C4CDC,  3),
    "Triforce Chart 5": TWWItemData("Chart", IC.progression_skip_balancing, base_id +  67, 1, None,None,0x803C4CDC,  4),
    "Triforce Chart 6": TWWItemData("Chart", IC.progression_skip_balancing, base_id +  68, 1, None,None,0x803C4CDC,  5),
    "Triforce Chart 7": TWWItemData("Chart", IC.progression_skip_balancing, base_id +  69, 1, None,None,0x803C4CDC,  6),
    "Triforce Chart 8": TWWItemData("Chart", IC.progression_skip_balancing, base_id +  70, 1, None,None,0x803C4CDC,  7),
    "Treasure Chart 1": TWWItemData("Chart", IC.progression_skip_balancing, base_id +  71, 1, None,None,0x803C4CDC, 23),
    "Treasure Chart 2": TWWItemData("Chart", IC.progression_skip_balancing, base_id +  72, 1, None,None,0x803C4CDC, 16),
    "Treasure Chart 3": TWWItemData("Chart", IC.progression_skip_balancing, base_id +  73, 1, None,None,0x803C4CDC, 30),
    "Treasure Chart 4": TWWItemData("Chart", IC.progression_skip_balancing, base_id +  74, 1, None,None,0x803C4CDC, 29),
    "Treasure Chart 5": TWWItemData("Chart", IC.progression_skip_balancing, base_id +  75, 1, None,None,0x803C4CDC, 12),
    "Treasure Chart 6": TWWItemData("Chart", IC.progression_skip_balancing, base_id +  76, 1, None,None,0x803C4CDC, 20),
    "Treasure Chart 7": TWWItemData("Chart", IC.progression_skip_balancing, base_id +  77, 1, None,None,0x803C4CE0, 18),
    "Treasure Chart 8": TWWItemData("Chart", IC.progression_skip_balancing, base_id +  78, 1, None,None,0x803C4CE0, 10),
    "Treasure Chart 9": TWWItemData("Chart", IC.progression_skip_balancing, base_id +  79, 1, None,None,0x803C4CE0,  4),
    "Treasure Chart 10":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  80, 1, None,None,0x803C4CE0,  0),
    "Treasure Chart 11":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  81, 1, None,None,0x803C4CDC,  8),
    "Treasure Chart 12":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  82, 1, None,None,0x803C4CDC, 21),
    "Treasure Chart 13":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  83, 1, None,None,0x803C4CE0, 15),
    "Treasure Chart 14":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  84, 1, None,None,0x803C4CE0,  1),
    "Treasure Chart 15":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  85, 1, None,None,0x803C4CDC,  9),
    "Treasure Chart 16":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  86, 1, None,None,0x803C4CDC, 27),
    "Treasure Chart 17":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  87, 1, None,None,0x803C4CE0,  7),
    "Treasure Chart 18":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  88, 1, None,None,0x803C4CDC, 26),
    "Treasure Chart 19":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  89, 1, None,None,0x803C4CE0, 13),
    "Treasure Chart 20":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  90, 1, None,None,0x803C4CDC, 11),
    "Treasure Chart 21":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  91, 1, None,None,0x803C4CE0, 16),
    "Treasure Chart 22":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  92, 1, None,None,0x803C4CE0,  5),
    "Treasure Chart 23":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  93, 1, None,None,0x803C4CDC, 13),
    "Treasure Chart 24":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  94, 1, None,None,0x803C4CDC, 19),
    "Treasure Chart 25":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  95, 1, None,None,0x803C4CE0,  8),
    "Treasure Chart 26":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  96, 1, None,None,0x803C4CE0, 11),
    "Treasure Chart 27":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  97, 1, None,None,0x803C4CE0, 17),
    "Treasure Chart 28":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  98, 1, None,None,0x803C4CDC, 28),
    "Treasure Chart 29":TWWItemData("Chart", IC.progression_skip_balancing, base_id +  99, 1, None,None,0x803C4CDC, 24),
    "Treasure Chart 30":TWWItemData("Chart", IC.progression_skip_balancing, base_id + 100, 1, None,None,0x803C4CDC, 10),
    "Treasure Chart 31":TWWItemData("Chart", IC.progression_skip_balancing, base_id + 101, 1, None,None,0x803C4CDC, 14),
    "Treasure Chart 32":TWWItemData("Chart", IC.progression_skip_balancing, base_id + 102, 1, None,None,0x803C4CE0, 14),
    "Treasure Chart 33":TWWItemData("Chart", IC.progression_skip_balancing, base_id + 103, 1, None,None,0x803C4CDC, 15),
    "Treasure Chart 34":TWWItemData("Chart", IC.progression_skip_balancing, base_id + 104, 1, None,None,0x803C4CDC, 25),
    "Treasure Chart 35":TWWItemData("Chart", IC.progression_skip_balancing, base_id + 105, 1, None,None,0x803C4CDC, 22),
    "Treasure Chart 36":TWWItemData("Chart", IC.progression_skip_balancing, base_id + 106, 1, None,None,0x803C4CE0,  6),
    "Treasure Chart 37":TWWItemData("Chart", IC.progression_skip_balancing, base_id + 107, 1, None,None,0x803C4CE0,  9),
    "Treasure Chart 38":TWWItemData("Chart", IC.progression_skip_balancing, base_id + 108, 1, None,None,0x803C4CDC, 17),
    "Treasure Chart 39":TWWItemData("Chart", IC.progression_skip_balancing, base_id + 109, 1, None,None,0x803C4CDC, 18),
    "Treasure Chart 40":TWWItemData("Chart", IC.progression_skip_balancing, base_id + 110, 1, None,None,0x803C4CDC, 31),
    "Treasure Chart 41":TWWItemData("Chart", IC.progression_skip_balancing, base_id + 111, 1, None,None,0x803C4CE0, 12),

    "Tingle's Chart":          TWWItemData("Chart",  IC.useful,      base_id + 112, 1, None,       None, 0x803C4CE0, 2),
    "Ghost Ship Chart":        TWWItemData("Chart",  IC.progression, base_id + 113, 1, None,       None, 0x803C4CE0, 3),
    "Octo Chart":              TWWItemData("Chart",  IC.useful,      base_id + 114, 1, None,       None, 0x803C4CE0,20),
    "Great Fairy Chart":       TWWItemData("Chart",  IC.useful,      base_id + 115, 1, None,       None, 0x803C4CE0,21),
    "Secret Cave Chart":       TWWItemData("Chart",  IC.useful,      base_id + 116, 1, None,       None, 0x803C4CE0,24),
    "Light Ring Chart":        TWWItemData("Chart",  IC.useful,      base_id + 117, 1, None,       None, 0x803C4CE0,25),
    "Platform Chart":          TWWItemData("Chart",  IC.useful,      base_id + 118, 1, None,       None, 0x803C4CE0,26),
    "Beedle's Chart":          TWWItemData("Chart",  IC.useful,      base_id + 119, 1, None,       None, 0x803C4CE0,27),
    "Submarine Chart":         TWWItemData("Chart",  IC.useful,      base_id + 120, 1, None,       None, 0x803C4CE0,28),

    "Green Rupee":             TWWItemData("Rupee",  IC.filler,      base_id + 121,  1, None,         1, None,    None),
    "Blue Rupee":              TWWItemData("Rupee",  IC.filler,      base_id + 122,  2, None,         5, None,    None),
    "Yellow Rupee":            TWWItemData("Rupee",  IC.filler,      base_id + 123,  3, None,        10, None,    None),
    "Red Rupee":               TWWItemData("Rupee",  IC.filler,      base_id + 124,  5, None,        20, None,    None),
    "Purple Rupee":            TWWItemData("Rupee",  IC.filler,      base_id + 125, 10, None,        50, None,    None),
    "Orange Rupee":            TWWItemData("Rupee",  IC.filler,      base_id + 126, 15, None,       100, None,    None),
    "Silver Rupee":            TWWItemData("Rupee",  IC.filler,      base_id + 127, 15, None,       200, None,    None),
    "Rainbow Rupee":           TWWItemData("Rupee",  IC.filler,      base_id + 128,  1, None,       500, None,    None),

    "Piece of Heart":          TWWItemData("Heart",  IC.useful,      base_id + 129, 44, None,         1, None,    None),
    "Heart Container":         TWWItemData("Heart",  IC.useful,      base_id + 130,  6, None,         4, None,    None),

    "DRC Big Key":             TWWItemData("BKey",   IC.progression, base_id + 131,  1, None,       0x3, None,       2),
    "DRC Small Key":           TWWItemData("SKey",   IC.progression, base_id + 132,  4, None,       0x3, None,    None),
    "FW Big Key":              TWWItemData("BKey",   IC.progression, base_id + 133,  1, None,       0x4, None,       2),
    "FW Small Key":            TWWItemData("SKey",   IC.progression, base_id + 134,  1, None,       0x4, None,    None),
    "TotG Big Key":            TWWItemData("BKey",   IC.progression, base_id + 135,  1, None,       0x5, None,       2),
    "TotG Small Key":          TWWItemData("SKey",   IC.progression, base_id + 136,  2, None,       0x5, None,    None),
    "ET Big Key":              TWWItemData("BKey",   IC.progression, base_id + 138,  1, None,       0x6, None,       2),
    "ET Small Key":            TWWItemData("SKey",   IC.progression, base_id + 139,  3, None,       0x6, None,    None),
    "WT Big Key":              TWWItemData("BKey",   IC.progression, base_id + 140,  1, None,       0x7, None,    None),
    "WT Small Key":            TWWItemData("SKey",   IC.progression, base_id + 141,  2, None,       0x7, None,    None),
    "DRC Dungeon Map":         TWWItemData("Map",    IC.useful,      base_id + 142,  1, None,       0x3, None,       0),
    "DRC Compass":             TWWItemData("Compass",IC.useful,      base_id + 143,  1, None,       0x3, None,       1),
    "FW Dungeon Map":          TWWItemData("Map",    IC.useful,      base_id + 144,  1, None,       0x4, None,       0),
    "FW Compass":              TWWItemData("Compass",IC.useful,      base_id + 145,  1, None,       0x4, None,       1),
    "TotG Dungeon Map":        TWWItemData("Map",    IC.useful,      base_id + 146,  1, None,       0x5, None,       0),
    "TotG Compass":            TWWItemData("Compass",IC.useful,      base_id + 147,  1, None,       0x5, None,       1),
    "FF Dungeon Map":          TWWItemData("Map",    IC.useful,      base_id + 148,  1, None,       0x2, None,       0),
    "FF Compass":              TWWItemData("Compass",IC.useful,      base_id + 149,  1, None,       0x2, None,       1),
    "ET Dungeon Map":          TWWItemData("Map",    IC.useful,      base_id + 150,  1, None,       0x6, None,       0),
    "ET Compass":              TWWItemData("Compass",IC.useful,      base_id + 151,  1, None,       0x6, None,       1),
    "WT Dungeon Map":          TWWItemData("Map",    IC.useful,      base_id + 152,  1, None,       0x7, None,       0),
    "WT Compass":              TWWItemData("Compass",IC.useful,      base_id + 153,  1, None,       0x7, None,       1),

    "Victory":                 TWWItemData("Item",   IC.progression, None,           1, None,      None, None,    None),
}

LOOKUP_ID_TO_NAME: dict[int, str] = {data.code: item for item, data in ITEM_TABLE.items() if data.code}

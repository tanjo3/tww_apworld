from typing import NamedTuple

from BaseClasses import Item
from BaseClasses import ItemClassification as IC


class TWWItemData(NamedTuple):
    type: str
    classification: IC
    code: int | None
    quantity: int
    item_id: int | None


class TWWItem(Item):
    game: str = "The Wind Waker"

    def __init__(self, name: str, player: int, data: TWWItemData, force_nonprogress: bool):
        adjusted_classification = IC.filler if force_nonprogress else data.classification
        super(TWWItem, self).__init__(name, adjusted_classification, TWWItem.get_apid(data.code), player)

        self.type = data.type
        self.item_id = data.item_id

    @staticmethod
    def get_apid(code: int):
        base_id: int = 2322432
        return base_id + code if code is not None else None


ITEM_TABLE: dict[str, TWWItemData] = {
    "Telescope":               TWWItemData("Item",    IC.filler,                       0,  1, 0x20),
  # "Boat's Sail":             TWWItemData("Item",    IC.progression,                  1,  1, 0x78),
    "Wind Waker":              TWWItemData("Item",    IC.progression,                  2,  1, 0x22),
    "Grappling Hook":          TWWItemData("Item",    IC.progression,                  3,  1, 0x25),
    "Spoils Bag":              TWWItemData("Item",    IC.progression,                  4,  1, 0x24),
    "Boomerang":               TWWItemData("Item",    IC.progression,                  5,  1, 0x2D),
    "Deku Leaf":               TWWItemData("Item",    IC.progression,                  6,  1, 0x34),
    "Tingle Tuner":            TWWItemData("Item",    IC.progression,                  7,  1, 0x21),
    "Iron Boots":              TWWItemData("Item",    IC.progression,                  8,  1, 0x29),
    "Magic Armor":             TWWItemData("Item",    IC.progression,                  9,  1, 0x2A),
    "Bait Bag":                TWWItemData("Item",    IC.progression,                 10,  1, 0x2C),
    "Bombs":                   TWWItemData("Item",    IC.progression,                 11,  1, 0x31),
    "Delivery Bag":            TWWItemData("Item",    IC.progression,                 12,  1, 0x30),
    "Hookshot":                TWWItemData("Item",    IC.progression,                 13,  1, 0x2F),
    "Skull Hammer":            TWWItemData("Item",    IC.progression,                 14,  1, 0x33),
    "Power Bracelets":         TWWItemData("Item",    IC.progression,                 15,  1, 0x28),

    "Hero's Charm":            TWWItemData("Item",    IC.filler,                      16,  1, 0x43),
    "Hurricane Spin":          TWWItemData("Item",    IC.filler,                      17,  1, 0xAA),
    "Dragon Tingle Statue":    TWWItemData("Item",    IC.progression,                 18,  1, 0xA3),
    "Forbidden Tingle Statue": TWWItemData("Item",    IC.progression,                 19,  1, 0xA4),
    "Goddess Tingle Statue":   TWWItemData("Item",    IC.progression,                 20,  1, 0xA5),
    "Earth Tingle Statue":     TWWItemData("Item",    IC.progression,                 21,  1, 0xA6),
    "Wind Tingle Statue":      TWWItemData("Item",    IC.progression,                 22,  1, 0xA7),

    "Wind's Requiem":          TWWItemData("Item",    IC.progression,                 23,  1, 0x6D),
    "Ballad of Gales":         TWWItemData("Item",    IC.progression,                 24,  1, 0x6E),
    "Command Melody":          TWWItemData("Item",    IC.progression,                 25,  1, 0x6F),
    "Earth God's Lyric":       TWWItemData("Item",    IC.progression,                 26,  1, 0x70),
    "Wind God's Aria":         TWWItemData("Item",    IC.progression,                 27,  1, 0x71),
    "Song of Passing":         TWWItemData("Item",    IC.progression,                 28,  1, 0x72),

    "Triforce Shard 1":        TWWItemData("Item",    IC.progression,                 29,  1, 0x61),
    "Triforce Shard 2":        TWWItemData("Item",    IC.progression,                 30,  1, 0x62),
    "Triforce Shard 3":        TWWItemData("Item",    IC.progression,                 31,  1, 0x63),
    "Triforce Shard 4":        TWWItemData("Item",    IC.progression,                 32,  1, 0x64),
    "Triforce Shard 5":        TWWItemData("Item",    IC.progression,                 33,  1, 0x65),
    "Triforce Shard 6":        TWWItemData("Item",    IC.progression,                 34,  1, 0x66),
    "Triforce Shard 7":        TWWItemData("Item",    IC.progression,                 35,  1, 0x67),
    "Triforce Shard 8":        TWWItemData("Item",    IC.progression,                 36,  1, 0x68),

    "Skull Necklace":          TWWItemData("Spoil",   IC.filler,                      37,  9, 0x45),
    "Boko Baba Seed":          TWWItemData("Spoil",   IC.filler,                      38,  1, 0x46),
    "Golden Feather":          TWWItemData("Spoil",   IC.filler,                      39,  9, 0x47),
    "Knight's Crest":          TWWItemData("Spoil",   IC.filler,                      40,  3, 0x48),
    "Red Chu Jelly":           TWWItemData("Spoil",   IC.filler,                      41,  1, 0x49),
    "Green Chu Jelly":         TWWItemData("Spoil",   IC.filler,                      42,  1, 0x4A),
    "Joy Pendant":             TWWItemData("Spoil",   IC.filler,                      43,  9, 0x1F),

    "All-Purpose Bait":        TWWItemData("Bait",    IC.filler,                      44,  1, 0x82),
    "Hyoi Pear":               TWWItemData("Bait",    IC.filler,                      45,  4, 0x83),

    "Note to Mom":             TWWItemData("Letter",  IC.progression,                 46,  1, 0x99),
    "Maggie's Letter":         TWWItemData("Letter",  IC.progression,                 47,  1, 0x9A),
    "Moblin's Letter":         TWWItemData("Letter",  IC.progression,                 48,  1, 0x9B),
    "Cabana Deed":             TWWItemData("Letter",  IC.progression,                 49,  1, 0x9C),
    "Fill-Up Coupon":          TWWItemData("Letter",  IC.filler,                      50,  1, 0x9E),

    "Nayru's Pearl":           TWWItemData("Pearl",   IC.progression,                 51,  1, 0x69),
    "Din's Pearl":             TWWItemData("Pearl",   IC.progression,                 52,  1, 0x6A),
    "Farore's Pearl":          TWWItemData("Pearl",   IC.progression,                 53,  1, 0x6B),

    "Progressive Sword":       TWWItemData("Prog",    IC.progression,                 54,  4, 0x38),
    "Progressive Shield":      TWWItemData("Prog",    IC.progression,                 55,  2, 0x3B),
    "Progressive Picto Box":   TWWItemData("Prog",    IC.progression,                 56,  2, 0x23),
    "Progressive Bow":         TWWItemData("Prog",    IC.progression,                 57,  3, 0x27),
    "Progressive Magic Meter": TWWItemData("Prog",    IC.progression,                 58,  2, 0xB1),
    "Progressive Quiver":      TWWItemData("Prog",    IC.progression,                 59,  2, 0xAF),
    "Progressive Bomb Bag":    TWWItemData("Prog",    IC.useful,                      60,  2, 0xAD),
    "Progressive Wallet":      TWWItemData("Prog",    IC.progression,                 61,  2, 0xAB),
    "Empty Bottle":            TWWItemData("Prog",    IC.progression,                 62,  4, 0x50),

    "Triforce Chart 1":        TWWItemData("Chart",   IC.progression_skip_balancing,  63,  1, 0xFE),
    "Triforce Chart 2":        TWWItemData("Chart",   IC.progression_skip_balancing,  64,  1, 0xFD),
    "Triforce Chart 3":        TWWItemData("Chart",   IC.progression_skip_balancing,  65,  1, 0xFC),
    "Triforce Chart 4":        TWWItemData("Chart",   IC.progression_skip_balancing,  66,  1, 0xFB),
    "Triforce Chart 5":        TWWItemData("Chart",   IC.progression_skip_balancing,  67,  1, 0xFA),
    "Triforce Chart 6":        TWWItemData("Chart",   IC.progression_skip_balancing,  68,  1, 0xF9),
    "Triforce Chart 7":        TWWItemData("Chart",   IC.progression_skip_balancing,  69,  1, 0xF8),
    "Triforce Chart 8":        TWWItemData("Chart",   IC.progression_skip_balancing,  70,  1, 0xF7),
    "Treasure Chart 1":        TWWItemData("Chart",   IC.progression_skip_balancing,  71,  1, 0xE7),
    "Treasure Chart 2":        TWWItemData("Chart",   IC.progression_skip_balancing,  72,  1, 0xEE),
    "Treasure Chart 3":        TWWItemData("Chart",   IC.progression_skip_balancing,  73,  1, 0xE0),
    "Treasure Chart 4":        TWWItemData("Chart",   IC.progression_skip_balancing,  74,  1, 0xE1),
    "Treasure Chart 5":        TWWItemData("Chart",   IC.progression_skip_balancing,  75,  1, 0xF2),
    "Treasure Chart 6":        TWWItemData("Chart",   IC.progression_skip_balancing,  76,  1, 0xEA),
    "Treasure Chart 7":        TWWItemData("Chart",   IC.progression_skip_balancing,  77,  1, 0xCC),
    "Treasure Chart 8":        TWWItemData("Chart",   IC.progression_skip_balancing,  78,  1, 0xD4),
    "Treasure Chart 9":        TWWItemData("Chart",   IC.progression_skip_balancing,  79,  1, 0xDA),
    "Treasure Chart 10":       TWWItemData("Chart",   IC.progression_skip_balancing,  80,  1, 0xDE),
    "Treasure Chart 11":       TWWItemData("Chart",   IC.progression_skip_balancing,  81,  1, 0xF6),
    "Treasure Chart 12":       TWWItemData("Chart",   IC.progression_skip_balancing,  82,  1, 0xE9),
    "Treasure Chart 13":       TWWItemData("Chart",   IC.progression_skip_balancing,  83,  1, 0xCF),
    "Treasure Chart 14":       TWWItemData("Chart",   IC.progression_skip_balancing,  84,  1, 0xDD),
    "Treasure Chart 15":       TWWItemData("Chart",   IC.progression_skip_balancing,  85,  1, 0xF5),
    "Treasure Chart 16":       TWWItemData("Chart",   IC.progression_skip_balancing,  86,  1, 0xE3),
    "Treasure Chart 17":       TWWItemData("Chart",   IC.progression_skip_balancing,  87,  1, 0xD7),
    "Treasure Chart 18":       TWWItemData("Chart",   IC.progression_skip_balancing,  88,  1, 0xE4),
    "Treasure Chart 19":       TWWItemData("Chart",   IC.progression_skip_balancing,  89,  1, 0xD1),
    "Treasure Chart 20":       TWWItemData("Chart",   IC.progression_skip_balancing,  90,  1, 0xF3),
    "Treasure Chart 21":       TWWItemData("Chart",   IC.progression_skip_balancing,  91,  1, 0xCE),
    "Treasure Chart 22":       TWWItemData("Chart",   IC.progression_skip_balancing,  92,  1, 0xD9),
    "Treasure Chart 23":       TWWItemData("Chart",   IC.progression_skip_balancing,  93,  1, 0xF1),
    "Treasure Chart 24":       TWWItemData("Chart",   IC.progression_skip_balancing,  94,  1, 0xEB),
    "Treasure Chart 25":       TWWItemData("Chart",   IC.progression_skip_balancing,  95,  1, 0xD6),
    "Treasure Chart 26":       TWWItemData("Chart",   IC.progression_skip_balancing,  96,  1, 0xD3),
    "Treasure Chart 27":       TWWItemData("Chart",   IC.progression_skip_balancing,  97,  1, 0xCD),
    "Treasure Chart 28":       TWWItemData("Chart",   IC.progression_skip_balancing,  98,  1, 0xE2),
    "Treasure Chart 29":       TWWItemData("Chart",   IC.progression_skip_balancing,  99,  1, 0xE6),
    "Treasure Chart 30":       TWWItemData("Chart",   IC.progression_skip_balancing, 100,  1, 0xF4),
    "Treasure Chart 31":       TWWItemData("Chart",   IC.progression_skip_balancing, 101,  1, 0xF0),
    "Treasure Chart 32":       TWWItemData("Chart",   IC.progression_skip_balancing, 102,  1, 0xD0),
    "Treasure Chart 33":       TWWItemData("Chart",   IC.progression_skip_balancing, 103,  1, 0xEF),
    "Treasure Chart 34":       TWWItemData("Chart",   IC.progression_skip_balancing, 104,  1, 0xE5),
    "Treasure Chart 35":       TWWItemData("Chart",   IC.progression_skip_balancing, 105,  1, 0xE8),
    "Treasure Chart 36":       TWWItemData("Chart",   IC.progression_skip_balancing, 106,  1, 0xD8),
    "Treasure Chart 37":       TWWItemData("Chart",   IC.progression_skip_balancing, 107,  1, 0xD5),
    "Treasure Chart 38":       TWWItemData("Chart",   IC.progression_skip_balancing, 108,  1, 0xED),
    "Treasure Chart 39":       TWWItemData("Chart",   IC.progression_skip_balancing, 109,  1, 0xEC),
    "Treasure Chart 40":       TWWItemData("Chart",   IC.progression_skip_balancing, 110,  1, 0xDF),
    "Treasure Chart 41":       TWWItemData("Chart",   IC.progression_skip_balancing, 111,  1, 0xD2),
 
    "Tingle's Chart":          TWWItemData("Chart",   IC.filler,                     112,  1, 0xDC),
    "Ghost Ship Chart":        TWWItemData("Chart",   IC.progression,                113,  1, 0xDB),
    "Octo Chart":              TWWItemData("Chart",   IC.filler,                     114,  1, 0xCA),
    "Great Fairy Chart":       TWWItemData("Chart",   IC.filler,                     115,  1, 0xC9),
    "Secret Cave Chart":       TWWItemData("Chart",   IC.filler,                     116,  1, 0xC6),
    "Light Ring Chart":        TWWItemData("Chart",   IC.filler,                     117,  1, 0xC5),
    "Platform Chart":          TWWItemData("Chart",   IC.filler,                     118,  1, 0xC4),
    "Beedle's Chart":          TWWItemData("Chart",   IC.filler,                     119,  1, 0xC3),
    "Submarine Chart":         TWWItemData("Chart",   IC.filler,                     120,  1, 0xC2),

    "Green Rupee":             TWWItemData("Rupee",   IC.filler,                     121,  1, 0x01),
    "Blue Rupee":              TWWItemData("Rupee",   IC.filler,                     122,  2, 0x02),
    "Yellow Rupee":            TWWItemData("Rupee",   IC.filler,                     123,  3, 0x03),
    "Red Rupee":               TWWItemData("Rupee",   IC.filler,                     124,  5, 0x04),
    "Purple Rupee":            TWWItemData("Rupee",   IC.filler,                     125, 10, 0x05),
    "Orange Rupee":            TWWItemData("Rupee",   IC.filler,                     126, 15, 0x06),
    "Silver Rupee":            TWWItemData("Rupee",   IC.filler,                     127, 15, 0x0F),
    "Rainbow Rupee":           TWWItemData("Rupee",   IC.filler,                     128,  1, 0xB8),

    "Piece of Heart":          TWWItemData("Heart",   IC.filler,                     129, 44, 0x07),
    "Heart Container":         TWWItemData("Heart",   IC.filler,                     130,  6, 0x08),

    "DRC Big Key":             TWWItemData("BKey",    IC.progression,                131,  1, 0x14),
    "DRC Small Key":           TWWItemData("SKey",    IC.progression,                132,  4, 0x13),
    "FW Big Key":              TWWItemData("BKey",    IC.progression,                133,  1, 0x40),
    "FW Small Key":            TWWItemData("SKey",    IC.progression,                134,  1, 0x1D),
    "TotG Big Key":            TWWItemData("BKey",    IC.progression,                135,  1, 0x5C),
    "TotG Small Key":          TWWItemData("SKey",    IC.progression,                136,  2, 0x5B),
    "ET Big Key":              TWWItemData("BKey",    IC.progression,                138,  1, 0x74),
    "ET Small Key":            TWWItemData("SKey",    IC.progression,                139,  3, 0x73),
    "WT Big Key":              TWWItemData("BKey",    IC.progression,                140,  1, 0x81),
    "WT Small Key":            TWWItemData("SKey",    IC.progression,                141,  2, 0x77),
    "DRC Dungeon Map":         TWWItemData("Map",     IC.filler,                     142,  1, 0x1B),
    "DRC Compass":             TWWItemData("Compass", IC.filler,                     143,  1, 0x1C),
    "FW Dungeon Map":          TWWItemData("Map",     IC.filler,                     144,  1, 0x41),
    "FW Compass":              TWWItemData("Compass", IC.filler,                     145,  1, 0x5A),
    "TotG Dungeon Map":        TWWItemData("Map",     IC.filler,                     146,  1, 0x5D),
    "TotG Compass":            TWWItemData("Compass", IC.filler,                     147,  1, 0x5E),
    "FF Dungeon Map":          TWWItemData("Map",     IC.filler,                     148,  1, 0x5F),
    "FF Compass":              TWWItemData("Compass", IC.filler,                     149,  1, 0x60),
    "ET Dungeon Map":          TWWItemData("Map",     IC.filler,                     150,  1, 0x75),
    "ET Compass":              TWWItemData("Compass", IC.filler,                     151,  1, 0x76),
    "WT Dungeon Map":          TWWItemData("Map",     IC.filler,                     152,  1, 0x84),
    "WT Compass":              TWWItemData("Compass", IC.filler,                     153,  1, 0x85),

    "Victory":                 TWWItemData("Item",    IC.progression,               None,  1, None),
}

LOOKUP_ID_TO_NAME: dict[int, str] = {
    TWWItem.get_apid(data.code): item for item, data in ITEM_TABLE.items() if data.code is not None
}

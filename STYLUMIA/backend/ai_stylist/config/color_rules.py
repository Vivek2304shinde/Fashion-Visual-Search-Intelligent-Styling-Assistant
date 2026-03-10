"""
Color combination rules based on color theory and fashion expertise.
This drives the validator agent's decisions.
"""

from typing import Dict, List, Tuple, Optional
from ai_stylist.schemas import Color, Occasion, Style

# Color family groupings - matching your actual Color enum EXACTLY
COLOR_FAMILIES = {
    "reds": [
        Color.RED, Color.BRIGHT_RED, Color.DARK_RED, Color.MAROON, Color.BURGUNDY, 
        Color.WINE, Color.CRIMSON, Color.SCARLET, Color.BRICK_RED, Color.RUST, 
        Color.TERRA_COTTA, Color.MAHOGANY, Color.RED_ORANGE
    ],
    "pinks": [
        Color.PINK, Color.HOT_PINK, Color.BABY_PINK, Color.BLUSH, Color.ROSE, 
        Color.ROSE_GOLD, Color.MAGENTA, Color.FUCHSIA, Color.CORAL, Color.PEACH, 
        Color.SALMON
    ],
    "oranges": [
        Color.ORANGE, Color.TANGERINE, Color.MANDARIN, Color.PUMPKIN, 
        Color.APRICOT, Color.PEACH_ORANGE, Color.BURNT_ORANGE
    ],
    "yellows": [
        Color.YELLOW, Color.MUSTARD, Color.GOLD, Color.GOLDEN, Color.LEMON, 
        Color.CANARY, Color.OCHRE, Color.SAFFRON, Color.TURMERIC, Color.SUNFLOWER
    ],
    "greens": [
        Color.GREEN, Color.LIME, Color.MINT, Color.PISTACHIO, Color.OLIVE, 
        Color.FOREST, Color.EMERALD, Color.JADE, Color.TEAL, Color.SEA_GREEN, 
        Color.MOSS, Color.SAGE, Color.PINE, Color.KHAKI, Color.ARMY_GREEN
    ],
    "blues": [
        Color.BLUE, Color.SKY_BLUE, Color.BABY_BLUE, Color.POWDER_BLUE, Color.LIGHT_BLUE,
        Color.NAVY, Color.ROYAL_BLUE, Color.MIDNIGHT_BLUE, Color.COBALT, Color.DENIM, 
        Color.TURQUOISE, Color.AQUA, Color.CYAN, Color.CERULEAN, Color.SAPPHIRE, 
        Color.CORNFLOWER
    ],
    "purples": [
        Color.PURPLE, Color.LAVENDER, Color.LILAC, Color.VIOLET, Color.PLUM, 
        Color.MAUVE, Color.EGGPLANT, Color.GRAPE, Color.INDIGO, Color.AMETHYST
    ],
    "browns": [
        Color.BROWN, Color.LIGHT_BROWN, Color.DARK_BROWN, Color.TAN, Color.BEIGE, 
        Color.CREAM, Color.ECRU, Color.TAUPE, Color.CAMEL, Color.KHAKI_BROWN, 
        Color.COFFEE, Color.MOCHA, Color.CHOCOLATE, Color.CARAMEL, Color.HONEY, 
        Color.TOFFEE, Color.CINNAMON
    ],
    "neutrals": [
        Color.WHITE, Color.OFF_WHITE, Color.IVORY, Color.CREAM_WHITE, Color.PEARL, 
        Color.BLACK, Color.JET_BLACK, Color.CHARCOAL, Color.GREY, Color.LIGHT_GREY, 
        Color.MEDIUM_GREY, Color.DARK_GREY, Color.SILVER, Color.GUNMETAL
    ],
    "metallics": [
        Color.METALLIC, Color.GOLD_METALLIC, Color.SILVER_METALLIC, 
        Color.COPPER, Color.BRONZE
    ],
    "multicolor": [
        Color.MULTICOLOR, Color.PRINTED, Color.PATTERNED, Color.TIE_DYE, 
        Color.OMBRE, Color.FLORAL_PRINT, Color.ABSTRACT_PRINT, Color.ETHNIC_PRINT, 
        Color.BANDHANI, Color.IKAT, Color.PAISLEY
    ],
}

# Color temperature classification
WARM_COLORS = [
    Color.RED, Color.BRIGHT_RED, Color.DARK_RED, Color.MAROON, Color.BURGUNDY, 
    Color.WINE, Color.CRIMSON, Color.SCARLET, Color.BRICK_RED, Color.RUST, 
    Color.TERRA_COTTA, Color.MAHOGANY, Color.RED_ORANGE,
    Color.ORANGE, Color.TANGERINE, Color.MANDARIN, Color.PUMPKIN, Color.APRICOT,
    Color.PEACH_ORANGE, Color.BURNT_ORANGE,
    Color.YELLOW, Color.MUSTARD, Color.GOLD, Color.GOLDEN, Color.LEMON,
    Color.CANARY, Color.OCHRE, Color.SAFFRON, Color.TURMERIC, Color.SUNFLOWER,
    Color.PINK, Color.HOT_PINK, Color.BABY_PINK, Color.BLUSH, Color.ROSE, 
    Color.CORAL, Color.PEACH, Color.SALMON,
    Color.BROWN, Color.LIGHT_BROWN, Color.DARK_BROWN, Color.TAN, Color.BEIGE, 
    Color.CAMEL, Color.KHAKI_BROWN, Color.COFFEE, Color.MOCHA, Color.CHOCOLATE, 
    Color.CARAMEL, Color.HONEY, Color.TOFFEE, Color.CINNAMON
]

COOL_COLORS = [
    Color.BLUE, Color.SKY_BLUE, Color.BABY_BLUE, Color.POWDER_BLUE, Color.LIGHT_BLUE,
    Color.NAVY, Color.ROYAL_BLUE, Color.MIDNIGHT_BLUE, Color.COBALT, Color.DENIM,
    Color.TURQUOISE, Color.AQUA, Color.CYAN, Color.CERULEAN, Color.SAPPHIRE,
    Color.CORNFLOWER,
    Color.GREEN, Color.LIME, Color.MINT, Color.PISTACHIO, Color.OLIVE,
    Color.FOREST, Color.EMERALD, Color.JADE, Color.TEAL, Color.SEA_GREEN,
    Color.MOSS, Color.SAGE, Color.PINE, Color.KHAKI, Color.ARMY_GREEN,
    Color.PURPLE, Color.LAVENDER, Color.LILAC, Color.VIOLET, Color.PLUM,
    Color.MAUVE, Color.EGGPLANT, Color.GRAPE, Color.INDIGO, Color.AMETHYST,
    Color.SILVER, Color.GUNMETAL
]

NEUTRAL_COLORS = [
    Color.WHITE, Color.OFF_WHITE, Color.IVORY, Color.CREAM_WHITE, Color.PEARL,
    Color.BLACK, Color.JET_BLACK, Color.CHARCOAL, Color.GREY, Color.LIGHT_GREY,
    Color.MEDIUM_GREY, Color.DARK_GREY,
    Color.BEIGE, Color.CREAM, Color.ECRU, Color.TAUPE
]

# Classic color combinations - using only valid color strings
CLASSIC_COMBINATIONS = [
    # Neutrals with anything
    (["white", "off_white", "ivory", "cream", "black", "jet_black", "charcoal", "grey", "light_grey", "dark_grey", "beige"], "any"),
    
    # Blue-based combinations
    (["navy"], ["white", "beige", "grey", "brown", "burgundy", "coral", "cream"]),
    (["sky_blue"], ["white", "beige", "navy", "grey", "cream"]),
    (["royal_blue"], ["white", "black", "silver", "gold"]),
    (["baby_blue"], ["white", "grey", "navy", "pink"]),
    (["light_blue"], ["white", "grey", "navy", "pink", "beige"]),
    
    # Green-based combinations
    (["olive"], ["beige", "navy", "white", "brown", "black", "cream", "burgundy"]),
    (["forest"], ["cream", "tan", "burgundy", "gold", "beige"]),
    (["sage"], ["white", "beige", "brown", "navy", "lavender"]),
    (["mint"], ["white", "grey", "navy", "pink", "coral"]),
    (["emerald"], ["black", "white", "gold", "navy", "burgundy"]),
    (["khaki"], ["white", "navy", "brown", "olive", "black"]),
    
    # Red-based combinations
    (["burgundy"], ["beige", "navy", "grey", "black", "cream", "gold", "white"]),
    (["maroon"], ["cream", "gold", "beige", "navy", "white"]),
    (["red"], ["black", "white", "navy", "grey", "gold"]),
    (["coral"], ["navy", "teal", "white", "grey", "cream", "mint"]),
    (["wine"], ["cream", "grey", "navy", "gold"]),
    (["rust"], ["cream", "navy", "olive", "brown", "beige"]),
    
    # Earth tones
    (["brown"], ["blue", "cream", "green", "beige", "orange", "turquoise", "camel"]),
    (["beige"], ["navy", "burgundy", "olive", "brown", "black", "maroon", "camel"]),
    (["tan"], ["navy", "white", "olive", "burgundy", "brown"]),
    (["camel"], ["navy", "white", "burgundy", "olive", "cream", "brown"]),
    (["caramel"], ["navy", "white", "cream", "burgundy"]),
    (["taupe"], ["white", "black", "navy", "burgundy", "olive"]),
    
    # Purple-based
    (["purple"], ["grey", "white", "black", "silver", "pink", "gold"]),
    (["lavender"], ["white", "grey", "navy", "silver", "cream", "pink"]),
    (["plum"], ["grey", "cream", "gold", "navy"]),
    (["indigo"], ["white", "cream", "grey", "gold"]),
    
    # Pink-based
    (["pink"], ["grey", "white", "navy", "black", "gold", "mint"]),
    (["hot_pink"], ["black", "white", "silver", "grey"]),
    (["magenta"], ["black", "white", "silver", "purple", "grey"]),
    (["rose_gold"], ["navy", "white", "grey", "blush"]),
    (["blush"], ["navy", "grey", "cream", "taupe", "gold"]),
    
    # Yellow-based
    (["mustard"], ["navy", "grey", "brown", "white", "olive", "burgundy"]),
    (["gold"], ["navy", "burgundy", "black", "white", "emerald", "maroon", "purple"]),
    (["yellow"], ["grey", "navy", "white", "black"]),
    (["lemon"], ["white", "grey", "navy", "pink"]),
    
    # Teal/Turquoise
    (["teal"], ["coral", "cream", "navy", "white", "gold", "brown", "burgundy"]),
    (["turquoise"], ["white", "navy", "coral", "gold", "brown", "purple"]),
    
    # Metallics
    (["gold_metallic"], ["navy", "black", "white", "burgundy", "emerald"]),
    (["silver_metallic"], ["navy", "black", "white", "purple", "blue"]),
    (["copper"], ["teal", "navy", "cream", "brown"]),
    (["bronze"], ["olive", "cream", "navy", "burgundy"]),
]

# Occasion-specific color recommendations
OCCASION_COLORS = {
    Occasion.WEDDING: {
        "primary": [
            Color.GOLD, Color.GOLD_METALLIC, Color.MAROON, Color.BURGUNDY, 
            Color.ROSE_GOLD, Color.NAVY, Color.FOREST, Color.EMERALD, 
            Color.WINE, Color.PEACH, Color.BLUSH, Color.CREAM, Color.LAVENDER,
            Color.ROSE, Color.SILVER_METALLIC
        ],
        "accent": [
            Color.CREAM, Color.IVORY, Color.BEIGE, Color.GOLD, Color.SILVER, 
            Color.ROSE_GOLD, Color.PEACH
        ],
        "avoid": [Color.BLACK, Color.WHITE]
    },
    Occasion.RECEPTION: {
        "primary": [
            Color.BLACK, Color.NAVY, Color.BURGUNDY, Color.EMERALD, 
            Color.SAPPHIRE, Color.PURPLE, Color.GOLD, Color.CHARCOAL,
            Color.SILVER_METALLIC, Color.RED
        ],
        "accent": [Color.GOLD, Color.SILVER, Color.ROSE_GOLD, Color.WHITE],
        "avoid": []
    },
    Occasion.ENGAGEMENT: {
        "primary": [
            Color.ROSE_GOLD, Color.BLUSH, Color.LAVENDER, Color.PEACH, 
            Color.MINT, Color.CORAL, Color.PINK, Color.BABY_PINK,
            Color.CREAM, Color.SKY_BLUE
        ],
        "accent": [Color.WHITE, Color.CREAM, Color.GOLD, Color.SILVER],
        "avoid": [Color.BLACK, Color.DARK_BROWN, Color.CHARCOAL]
    },
    Occasion.MEHENDI: {
        "primary": [
            Color.YELLOW, Color.MUSTARD, Color.ORANGE, Color.GREEN, 
            Color.PINK, Color.TURMERIC, Color.SAFFRON, Color.CORAL,
            Color.GOLD, Color.PEACH, Color.LIME, Color.HOT_PINK
        ],
        "accent": [Color.GOLD, Color.BROWN, Color.RED, Color.ORANGE],
        "avoid": [Color.BLACK, Color.WHITE, Color.GREY, Color.CHARCOAL]
    },
    Occasion.SANGEET: {
        "primary": [
            Color.PURPLE, Color.PINK, Color.BLUE, Color.GREEN, 
            Color.FUCHSIA, Color.TEAL, Color.GOLD, Color.MAGENTA,
            Color.ORANGE, Color.YELLOW, Color.SILVER
        ],
        "accent": [Color.SILVER, Color.GOLD, Color.ROSE_GOLD],
        "avoid": [Color.BROWN, Color.BEIGE, Color.TAUPE, Color.KHAKI]
    },
    Occasion.PARTY: {
        "primary": [
            Color.BLACK, Color.RED, Color.EMERALD, Color.SAPPHIRE, 
            Color.PURPLE, Color.FUCHSIA, Color.GOLD, Color.SILVER,
            Color.HOT_PINK, Color.BLUE, Color.MAGENTA
        ],
        "accent": [Color.GOLD, Color.SILVER, Color.ROSE_GOLD],
        "avoid": [Color.BEIGE, Color.KHAKI, Color.CREAM, Color.TAUPE]
    },
    Occasion.CLUB: {
        "primary": [
            Color.BLACK, Color.RED, Color.PURPLE, Color.HOT_PINK,
            Color.SILVER, Color.GOLD, Color.WHITE, Color.FUCHSIA,
            Color.MAGENTA
        ],
        "accent": [Color.SILVER, Color.GOLD, Color.WHITE],
        "avoid": [Color.BROWN, Color.BEIGE, Color.TAN, Color.OLIVE, Color.KHAKI]
    },
    Occasion.OFFICE: {
        "primary": [
            Color.NAVY, Color.CHARCOAL, Color.BLACK, Color.BROWN, 
            Color.DARK_GREY, Color.MAROON, Color.GREY, Color.BEIGE,
            Color.OLIVE, Color.BABY_BLUE
        ],
        "accent": [
            Color.WHITE, Color.OFF_WHITE, Color.BEIGE, Color.CREAM, 
            Color.SKY_BLUE, Color.SAGE, Color.LIGHT_GREY
        ],
        "avoid": [Color.HOT_PINK, Color.MAGENTA, Color.FUCHSIA, Color.BRIGHT_RED,
                  Color.ORANGE, Color.YELLOW]
    },
    Occasion.INTERVIEW: {
        "primary": [
            Color.NAVY, Color.CHARCOAL, Color.BLACK, Color.DARK_GREY, 
            Color.BROWN, Color.DARK_BROWN, Color.GREY
        ],
        "accent": [
            Color.WHITE, Color.OFF_WHITE, Color.LIGHT_BLUE, Color.BEIGE, 
            Color.CREAM, Color.LIGHT_GREY
        ],
        "avoid": [Color.RED, Color.PURPLE, Color.GREEN, Color.PATTERNED, 
                  Color.PRINTED]
    },
    Occasion.CASUAL: {
        "primary": "any",
        "accent": "any",
        "avoid": []
    },
    Occasion.DATE: {
        "primary": [
            Color.RED, Color.BLACK, Color.NAVY, Color.BURGUNDY, 
            Color.PURPLE, Color.EMERALD, Color.ROSE_GOLD, Color.MAROON,
            Color.BLUSH, Color.CORAL, Color.PEACH
        ],
        "accent": [
            Color.WHITE, Color.ROSE_GOLD, Color.SILVER, Color.BLUSH, 
            Color.PEACH, Color.CREAM
        ],
        "avoid": [Color.ORANGE, Color.YELLOW]
    },
    Occasion.DINNER: {
        "primary": [
            Color.BLACK, Color.NAVY, Color.BURGUNDY, Color.EMERALD,
            Color.PURPLE, Color.CHARCOAL, Color.RED
        ],
        "accent": [Color.GOLD, Color.SILVER, Color.WHITE],
        "avoid": []
    },
    Occasion.BEACH: {
        "primary": [
            Color.WHITE, Color.OFF_WHITE, Color.BEIGE, Color.TAN, 
            Color.SKY_BLUE, Color.TURQUOISE, Color.CORAL, Color.MINT, 
            Color.YELLOW, Color.PEACH, Color.AQUA, Color.LIGHT_BLUE
        ],
        "accent": [Color.YELLOW, Color.ORANGE, Color.PINK, Color.CORAL],
        "avoid": [Color.BLACK, Color.CHARCOAL, Color.DARK_BROWN, Color.NAVY]
    },
    Occasion.FESTIVAL: {
        "primary": [
            Color.RED, Color.YELLOW, Color.GREEN, Color.BLUE,
            Color.PURPLE, Color.PINK, Color.ORANGE, Color.GOLD,
            Color.MAGENTA, Color.TURMERIC, Color.SAFFRON
        ],
        "accent": [Color.GOLD, Color.SILVER, Color.COPPER],
        "avoid": [Color.BLACK, Color.GREY, Color.CHARCOAL]
    },
    Occasion.DIWALI: {
        "primary": [
            Color.GOLD, Color.RED, Color.YELLOW, Color.ORANGE,
            Color.GREEN, Color.PURPLE, Color.PINK, Color.MAROON,
            Color.ROSE_GOLD
        ],
        "accent": [Color.GOLD, Color.SILVER, Color.COPPER],
        "avoid": [Color.BLACK, Color.WHITE, Color.GREY]
    },
    Occasion.HOLI: {
        "primary": [
            Color.RED, Color.YELLOW, Color.GREEN, Color.PINK,
            Color.PURPLE, Color.ORANGE, Color.BLUE, Color.MAGENTA,
            Color.CORAL, Color.TURQUOISE
        ],
        "accent": [Color.WHITE],
        "avoid": [Color.BLACK, Color.DARK_BROWN, Color.CHARCOAL]
    }
}

# Season-based color recommendations
# SEASONAL_COLORS = {
#     Season.SUMMER: {
#         "primary": [
#             Color.WHITE, Color.OFF_WHITE, Color.BEIGE, Color.CREAM, 
#             Color.SKY_BLUE, Color.MINT, Color.CORAL, Color.PEACH, 
#             Color.YELLOW, Color.TURQUOISE, Color.LAVENDER, Color.BABY_BLUE,
#             Color.PINK, Color.LIGHT_GREY, Color.TAN, Color.LIGHT_BLUE
#         ],
#         "accent": [Color.PINK, Color.LAVENDER, Color.LIGHT_GREY, Color.YELLOW],
#         "avoid": [Color.BLACK, Color.CHARCOAL, Color.DARK_BROWN, Color.NAVY,
#                   Color.DARK_GREEN, Color.PURPLE]
#     },
#     Season.WINTER: {
#         "primary": [
#             Color.BLACK, Color.JET_BLACK, Color.CHARCOAL, Color.BURGUNDY, 
#             Color.FOREST, Color.NAVY, Color.MAROON, Color.EMERALD, 
#             Color.PLUM, Color.DARK_GREY, Color.CAMEL, Color.WINE,
#             Color.DARK_BROWN, Color.GREY
#         ],
#         "accent": [Color.RED, Color.GOLD, Color.WHITE, Color.SILVER, 
#                    Color.COPPER, Color.BURGUNDY],
#         "avoid": [Color.PASTEL, Color.LIGHT, Color.BRIGHT]
#     },
#     Season.SPRING: {
#         "primary": [
#             Color.LAVENDER, Color.BLUSH, Color.MINT, Color.CORAL,
#             Color.PEACH, Color.ROSE, Color.SKY_BLUE, Color.CREAM,
#             Color.YELLOW, Color.BABY_PINK, Color.LILAC, Color.PISTACHIO,
#             Color.SAGE, Color.LIGHT_GREEN, Color.LIGHT_BLUE
#         ],
#         "accent": [Color.YELLOW, Color.GREEN, Color.PINK, Color.CORAL],
#         "avoid": [Color.DARK, Color.HEAVY, Color.BLACK, Color.CHARCOAL,
#                   Color.DARK_BROWN]
#     },
#     Season.FALL: {
#         "primary": [
#             Color.MAROON, Color.BURGUNDY, Color.MUSTARD, Color.OLIVE,
#             Color.BROWN, Color.RUST, Color.TERRA_COTTA, Color.CARAMEL,
#             Color.ORANGE, Color.TAN, Color.CAMEL, Color.TAUPE,
#             Color.COPPER, Color.FOREST
#         ],
#         "accent": [Color.ORANGE, Color.RED, Color.GOLD, Color.COPPER,
#                    Color.MAROON],
#         "avoid": [Color.BRIGHT, Color.NEON, Color.PASTEL, Color.LIGHT,
#                   Color.WHITE]
#     },
#     Season.AUTUMN: {
#         "primary": [
#             Color.MAROON, Color.BURGUNDY, Color.MUSTARD, Color.OLIVE,
#             Color.BROWN, Color.RUST, Color.TERRA_COTTA, Color.CARAMEL,
#             Color.ORANGE, Color.TAN, Color.CAMEL, Color.COPPER,
#             Color.FOREST, Color.CHOCOLATE
#         ],
#         "accent": [Color.ORANGE, Color.RED, Color.GOLD, Color.COPPER],
#         "avoid": [Color.BRIGHT, Color.NEON, Color.PASTEL, Color.LIGHT]
#     },
#     Season.MONSOON: {
#         "primary": [
#             Color.BLUE, Color.SKY_BLUE, Color.GREEN, Color.TEAL, 
#             Color.PURPLE, Color.BURGUNDY, Color.BROWN, Color.EMERALD,
#             Color.CHARCOAL, Color.GREY, Color.OLIVE, Color.DENIM
#         ],
#         "accent": [Color.YELLOW, Color.ORANGE, Color.PINK, Color.CORAL],
#         "avoid": [Color.WHITE, Color.OFF_WHITE, Color.BEIGE, Color.CREAM,
#                   Color.LIGHT, Color.PASTEL]
#     },
#     Season.ALL_SEASON: {
#         "primary": "any",
#         "accent": "any",
#         "avoid": []
#     }
# }

# Style-based color recommendations
STYLE_COLORS = {
    Style.FORMAL: {
        "primary": [
            Color.BLACK, Color.NAVY, Color.CHARCOAL, Color.DARK_GREY,
            Color.BROWN, Color.MAROON, Color.DARK_BROWN, Color.GREY
        ],
        "accent": [
            Color.WHITE, Color.OFF_WHITE, Color.BEIGE, Color.CREAM, 
            Color.LIGHT_BLUE, Color.SILVER
        ],
        "avoid": [Color.HOT_PINK, Color.MAGENTA, Color.FUCHSIA,
                  Color.ORANGE, Color.YELLOW, Color.BRIGHT_RED]
    },
    Style.BUSINESS: {
        "primary": [
            Color.NAVY, Color.CHARCOAL, Color.BLACK, Color.DARK_GREY,
            Color.BROWN, Color.GREY, Color.DARK_BROWN, Color.MAROON
        ],
        "accent": [
            Color.WHITE, Color.OFF_WHITE, Color.LIGHT_BLUE, Color.BEIGE, 
            Color.CREAM, Color.SAGE, Color.LIGHT_GREY
        ],
        "avoid": [Color.RED, Color.PURPLE, Color.GREEN, Color.FUCHSIA,
                  Color.ORANGE, Color.HOT_PINK]
    },
    Style.CASUAL: {
        "primary": "any",
        "accent": "any",
        "avoid": []
    },
    Style.STREETWEAR: {
        "primary": [
            Color.BLACK, Color.WHITE, Color.GREY, Color.OLIVE,
            Color.KHAKI, Color.ARMY_GREEN, Color.BURGUNDY, Color.NAVY,
            Color.CHARCOAL, Color.RED
        ],
        "accent": [Color.RED, Color.YELLOW, Color.ORANGE, Color.HOT_PINK,
                   Color.MAGENTA, Color.BLUE],
        "avoid": [Color.BABY_PINK, Color.BLUSH,
                  Color.CREAM, Color.BEIGE]
    },
    Style.URBAN: {
        "primary": [
            Color.BLACK, Color.GREY, Color.CHARCOAL, Color.NAVY,
            Color.OLIVE, Color.KHAKI, Color.WHITE
        ],
        "accent": [Color.RED, Color.YELLOW, Color.ORANGE, Color.BLUE],
        "avoid": []
    },
    Style.TRADITIONAL: {
        "primary": [
            Color.MAROON, Color.BURGUNDY, Color.GOLD, Color.GOLD_METALLIC,
            Color.RED, Color.GREEN, Color.PURPLE, Color.ROYAL_BLUE,
            Color.MAGENTA, Color.SILVER, Color.PINK, Color.YELLOW,
            Color.ORANGE, Color.EMERALD
        ],
        "accent": [Color.CREAM, Color.BEIGE, Color.GOLD, Color.SILVER],
        "avoid": [Color.BLACK, Color.WHITE, Color.GREY, Color.CHARCOAL]
    },
    Style.ETHNIC: {
        "primary": [
            Color.MAROON, Color.BURGUNDY, Color.GOLD, Color.RED,
            Color.GREEN, Color.PURPLE, Color.BLUE, Color.PINK,
            Color.YELLOW, Color.ORANGE, Color.MAGENTA, Color.SILVER
        ],
        "accent": [Color.GOLD, Color.SILVER, Color.COPPER],
        "avoid": [Color.BLACK, Color.WHITE, Color.GREY]
    },
    Style.INDO_WESTERN: {
        "primary": [
            Color.MAROON, Color.BURGUNDY, Color.NAVY, Color.EMERALD,
            Color.GOLD, Color.PURPLE, Color.TEAL, Color.ROYAL_BLUE,
            Color.BLACK, Color.WHITE, Color.SILVER
        ],
        "accent": [Color.CREAM, Color.BEIGE, Color.GOLD, Color.SILVER],
        "avoid": []
    },
    Style.MINIMALIST: {
        "primary": [
            Color.BLACK, Color.WHITE, Color.GREY, Color.LIGHT_GREY,
            Color.BEIGE, Color.NAVY, Color.CHARCOAL, Color.CREAM,
            Color.OFF_WHITE, Color.TAUPE
        ],
        "accent": [Color.ANY],
        "avoid": [ Color.PATTERNED, 
                  Color.MULTICOLOR]
    },
    Style.CONTEMPORARY: {
        "primary": [
            Color.BLACK, Color.WHITE, Color.NAVY, Color.GREY,
            Color.OLIVE, Color.BURGUNDY, Color.TEAL, Color.MUSTARD
        ],
        "accent": [Color.GOLD, Color.SILVER, Color.COPPER, Color.CORAL],
        "avoid": []
    },
    Style.BOHEMIAN: {
        "primary": [
            Color.BROWN, Color.TAN, Color.CREAM, Color.RUST,
            Color.MUSTARD, Color.OLIVE, Color.TEAL, Color.TERRA_COTTA,
            Color.SAGE, Color.BURGUNDY, Color.TURQUOISE, Color.CORAL,
            Color.PEACH, Color.LAVENDER
        ],
        "accent": [
            Color.TURQUOISE, Color.CORAL, Color.GOLD, Color.PURPLE,
            Color.MAGENTA, Color.PEACH, Color.PINK
        ],
        "avoid": []
    },
    Style.BOHO: {
        "primary": [
            Color.BROWN, Color.CREAM, Color.RUST, Color.MUSTARD,
            Color.OLIVE, Color.TURQUOISE, Color.CORAL, Color.TERRA_COTTA
        ],
        "accent": [Color.TURQUOISE, Color.GOLD, Color.PURPLE, Color.PINK],
        "avoid": [Color.BLACK, Color.WHITE]
    },
    Style.ROCK: {
        "primary": [
            Color.BLACK, Color.JET_BLACK, Color.CHARCOAL, Color.DARK_GREY,
            Color.BURGUNDY, Color.DARK_RED, Color.GREY
        ],
        "accent": [Color.RED, Color.WHITE, Color.SILVER, Color.GUNMETAL],
        "avoid": [ Color.PINK, Color.BABY_PINK,
                  Color.CREAM, Color.BEIGE]
    },
    Style.PUNK: {
        "primary": [
            Color.BLACK, Color.JET_BLACK, Color.CHARCOAL, Color.RED,
            Color.DARK_RED, Color.DARK_GREY
        ],
        "accent": [Color.RED, Color.WHITE, Color.SILVER, Color.GUNMETAL],
        "avoid": []
    },
    Style.GRUNGE: {
        "primary": [
            Color.BLACK, Color.GREY, Color.OLIVE, Color.BROWN,
            Color.RUST,  Color.NAVY
        ],
        "accent": [Color.RED, Color.ORANGE, Color.BURGUNDY],
        "avoid": []
    },
    Style.CLASSIC: {
        "primary": [
            Color.NAVY, Color.BLACK, Color.BEIGE, Color.WHITE,
            Color.BROWN, Color.MAROON, Color.CHARCOAL, Color.GREY
        ],
        "accent": [Color.WHITE, Color.CREAM, Color.GOLD, Color.SILVER],
        "avoid": []
    },
    Style.PREPPY: {
        "primary": [
            Color.NAVY, Color.BURGUNDY, Color.GREEN, Color.PINK,
            Color.YELLOW, Color.WHITE, Color.CREAM, Color.BEIGE,
            Color.LIGHT_BLUE, Color.RED
        ],
        "accent": [Color.GOLD, Color.SILVER, Color.CORAL, Color.PINK],
        "avoid": [ Color.BLACK]
    },
    Style.VINTAGE: {
        "primary": [
            Color.CREAM, Color.BEIGE, Color.MUSTARD, Color.OLIVE,
            Color.BROWN, Color.RUST, Color.MAROON, Color.NAVY,
            Color.BURGUNDY, Color.TAUPE
        ],
        "accent": [Color.GOLD, Color.COPPER, Color.CREAM],
        "avoid": []
    },
    Style.RETRO: {
        "primary": [
            Color.MUSTARD, Color.ORANGE, Color.BROWN, Color.GREEN,
            Color.CORAL, Color.TEAL, Color.PINK, Color.YELLOW
        ],
        "accent": [Color.COPPER, Color.GOLD, Color.BROWN],
        "avoid": []
    },
    Style.ATHLEISURE: {
        "primary": [
            Color.BLACK, Color.GREY, Color.NAVY, Color.OLIVE,
            Color.BURGUNDY, Color.CHARCOAL, Color.WHITE, Color.BLUE
        ],
        "accent": [Color.WHITE, Color.RED, Color.BLUE,
                   Color.YELLOW, Color.ORANGE],
        "avoid": []
    },
    Style.SPORTS: {
        "primary": [
            Color.BLACK, Color.NAVY, Color.RED, Color.BLUE,
            Color.WHITE, Color.GREY, Color.GREEN
        ],
        "accent": [Color.WHITE, Color.YELLOW, Color.ORANGE],
        "avoid": []
    },
    Style.SMART_CASUAL: {
        "primary": [
            Color.NAVY, Color.CHARCOAL, Color.BEIGE, Color.OLIVE,
            Color.BURGUNDY, Color.GREY, Color.BROWN, Color.WHITE
        ],
        "accent": [
            Color.WHITE, Color.CREAM, Color.LIGHT_BLUE, Color.SAGE,
            Color.PINK, Color.CORAL
        ],
        "avoid": []
    },
    Style.ROMANTIC: {
        "primary": [
            Color.BLUSH, Color.PINK, Color.LAVENDER, Color.PEACH,
            Color.CREAM, Color.ROSE, Color.MINT, Color.LILAC,
            Color.BABY_BLUE, Color.CORAL
        ],
        "accent": [Color.GOLD, Color.ROSE_GOLD, Color.SILVER, Color.WHITE],
        "avoid": [Color.BLACK]
    },
    Style.LUXURY: {
        "primary": [
            Color.BLACK, Color.NAVY, Color.BURGUNDY, Color.EMERALD,
            Color.GOLD, Color.SILVER, Color.WHITE, Color.CHARCOAL,
            Color.PURPLE, Color.MAROON
        ],
        "accent": [Color.GOLD, Color.SILVER, Color.ROSE_GOLD],
        "avoid": []
    },
    Style.FESTIVE: {
        "primary": [
            Color.RED, Color.GOLD, Color.GREEN, Color.BLUE,
            Color.PURPLE, Color.PINK, Color.YELLOW, Color.ORANGE,
            Color.MAGENTA, Color.TURQUOISE
        ],
        "accent": [Color.GOLD, Color.SILVER, Color.COPPER],
        "avoid": [Color.BLACK, Color.GREY]
    },
    Style.WEDDING: {
        "primary": [
            Color.WHITE, Color.CREAM, Color.IVORY, Color.BLUSH,
            Color.PEACH, Color.LAVENDER, Color.GOLD, Color.SILVER,
            Color.ROSE_GOLD
        ],
        "accent": [Color.GOLD, Color.SILVER, Color.ROSE_GOLD],
        "avoid": [Color.BLACK, Color.RED
                  ]
    },
    Style.PARTY: {
        "primary": [
            Color.BLACK, Color.RED, Color.GOLD, Color.SILVER,
            Color.PURPLE, Color.HOT_PINK, Color.BLUE, Color.EMERALD
        ],
        "accent": [Color.GOLD, Color.SILVER, Color.ROSE_GOLD],
        "avoid": [Color.BEIGE, Color.KHAKI]
    },
    Style.SUMMER: {
        "primary": [
            Color.WHITE, Color.YELLOW, Color.PINK, Color.LIGHT_BLUE,
            Color.CORAL, Color.MINT, Color.LAVENDER, Color.PEACH
        ],
        "accent": [Color.GOLD, Color.COPPER, Color.WHITE],
        "avoid": [Color.BLACK]
    },
    Style.WINTER: {
        "primary": [
            Color.BLACK, Color.NAVY, Color.BURGUNDY, Color.FOREST,
            Color.CHARCOAL, Color.MAROON, Color.CAMEL
        ],
        "accent": [Color.WHITE, Color.RED, Color.GOLD, Color.SILVER],
        "avoid": []
    },
    Style.SPORTY: {
        "primary": [
            Color.BLACK, Color.NAVY, Color.RED, Color.BLUE,
            Color.WHITE, Color.GREY, Color.GREEN, Color.ORANGE
        ],
        "accent": [Color.WHITE, Color.YELLOW],
        "avoid": []
    },
    Style.RESORT: {
        "primary": [
            Color.WHITE, Color.BEIGE, Color.TAN, Color.SKY_BLUE,
            Color.TURQUOISE, Color.CORAL, Color.MINT, Color.YELLOW,
            Color.PEACH, Color.LIGHT_BLUE
        ],
        "accent": [Color.YELLOW, Color.ORANGE, Color.PINK, Color.CORAL],
        "avoid": [Color.BLACK]
    },
    Style.COCKTAIL: {
        "primary": [
            Color.BLACK, Color.RED, Color.NAVY, Color.BURGUNDY,
            Color.EMERALD, Color.PURPLE, Color.GOLD, Color.SILVER
        ],
        "accent": [Color.GOLD, Color.SILVER, Color.ROSE_GOLD],
        "avoid": [ Color.BEIGE, Color.KHAKI]
    },
    Style.BLACK_TIE: {
        "primary": [
            Color.BLACK, Color.NAVY, Color.CHARCOAL, Color.WHITE
        ],
        "accent": [Color.WHITE, Color.SILVER, Color.GOLD],
        "avoid": [Color.PATTERNED]
    },
    Style.WHITE_TIE: {
        "primary": [
            Color.BLACK, Color.WHITE, Color.NAVY
        ],
        "accent": [Color.WHITE, Color.SILVER, Color.GOLD],
        "avoid": [ Color.PATTERNED]
    },
    Style.ELEGANT: {
        "primary": [
            Color.BLACK, Color.NAVY, Color.WHITE, Color.CREAM,
            Color.BURGUNDY, Color.EMERALD, Color.CHARCOAL
        ],
        "accent": [Color.GOLD, Color.SILVER, Color.PEARL],
        "avoid": []
    }
}

# Add this to your existing color_rules.py

SEASONAL_COLORS = {
    "summer": {
        "primary": [
            Color.WHITE, Color.OFF_WHITE, Color.BEIGE, Color.CREAM, 
            Color.SKY_BLUE, Color.MINT, Color.CORAL, Color.PEACH, 
            Color.YELLOW, Color.TURQUOISE, Color.LAVENDER, Color.BABY_BLUE,
            Color.PINK, Color.LIGHT_GREY, Color.TAN, Color.LIGHT_BLUE
        ],
        "accent": [Color.PINK, Color.LAVENDER, Color.LIGHT_GREY, Color.YELLOW],
        "avoid": [Color.BLACK, Color.CHARCOAL, Color.DARK_BROWN, Color.NAVY]
    },
    "winter": {
        "primary": [
            Color.BLACK, Color.JET_BLACK, Color.CHARCOAL, Color.BURGUNDY, 
            Color.FOREST, Color.NAVY, Color.MAROON, Color.EMERALD, 
            Color.PLUM, Color.DARK_GREY, Color.CAMEL, Color.WINE,
            Color.DARK_BROWN, Color.GREY
        ],
        "accent": [Color.RED, Color.GOLD, Color.WHITE, Color.SILVER, Color.COPPER],
        "avoid": []
    },
    "spring": {
        "primary": [
            Color.LAVENDER, Color.BLUSH, Color.MINT, Color.CORAL,
            Color.PEACH, Color.ROSE, Color.SKY_BLUE, Color.CREAM,
            Color.YELLOW, Color.BABY_PINK, Color.LILAC, Color.PISTACHIO,
            Color.SAGE, Color.LIGHT_BLUE
        ],
        "accent": [Color.YELLOW, Color.GREEN, Color.PINK, Color.CORAL],
        "avoid": [ Color.BLACK, Color.CHARCOAL]
    },
    "fall": {
        "primary": [
            Color.MAROON, Color.BURGUNDY, Color.MUSTARD, Color.OLIVE,
            Color.BROWN, Color.RUST, Color.TERRA_COTTA, Color.CARAMEL,
            Color.ORANGE, Color.TAN, Color.CAMEL, Color.TAUPE,
            Color.COPPER, Color.FOREST
        ],
        "accent": [Color.ORANGE, Color.RED, Color.GOLD, Color.COPPER],
        "avoid": []
    },
    "autumn": {
        "primary": [
            Color.MAROON, Color.BURGUNDY, Color.MUSTARD, Color.OLIVE,
            Color.BROWN, Color.RUST, Color.TERRA_COTTA, Color.CARAMEL,
            Color.ORANGE, Color.TAN, Color.CAMEL, Color.COPPER,
            Color.FOREST, Color.CHOCOLATE
        ],
        "accent": [Color.ORANGE, Color.RED, Color.GOLD, Color.COPPER],
        "avoid": []
    },
    "monsoon": {
        "primary": [
            Color.BLUE, Color.SKY_BLUE, Color.GREEN, Color.TEAL, 
            Color.PURPLE, Color.BURGUNDY, Color.BROWN, Color.EMERALD,
            Color.CHARCOAL, Color.GREY, Color.OLIVE, Color.DENIM
        ],
        "accent": [Color.YELLOW, Color.ORANGE, Color.PINK, Color.CORAL],
        "avoid": [Color.WHITE, Color.OFF_WHITE, Color.BEIGE, Color.CREAM]
    },
    "all_season": {
        "primary": "any",
        "accent": "any",
        "avoid": []
    }
}

# Helper functions
def get_complementary_colors(color: Color, count: int = 5) -> List[Color]:
    """Get colors that complement a given color"""
    color_str = color.value.lower()
    complements = []
    
    for primary, secondary in CLASSIC_COMBINATIONS:
        if color_str in primary:
            if secondary == "any":
                neutrals = [Color.WHITE, Color.BLACK, Color.GREY, Color.BEIGE, 
                           Color.NAVY, Color.CREAM, Color.CHARCOAL]
                return neutrals[:count]
            for sec in secondary:
                try:
                    for color_enum in Color:
                        if color_enum.value == sec:
                            complements.append(color_enum)
                            break
                except:
                    pass
    
    # Add neutrals if we don't have enough
    neutrals = [Color.WHITE, Color.BLACK, Color.GREY, Color.BEIGE, Color.CREAM,
                Color.NAVY, Color.CHARCOAL]
    for neutral in neutrals:
        if neutral not in complements:
            complements.append(neutral)
    
    # Remove duplicates and limit
    seen = set()
    unique_complements = []
    for c in complements:
        if c.value not in seen:
            seen.add(c.value)
            unique_complements.append(c)
    
    return unique_complements[:count]

def get_analogous_colors(color: Color, count: int = 3) -> List[Color]:
    """Get analogous colors (from same color family)"""
    color_family = get_color_family(color)
    if color_family in COLOR_FAMILIES:
        family_colors = COLOR_FAMILIES[color_family]
        others = [c for c in family_colors if c != color]
        return others[:count]
    return []

def get_monochromatic_colors(color: Color, count: int = 3) -> List[Color]:
    """Get different shades of the same color (from same family)"""
    return get_analogous_colors(color, count)

def validate_color_combination(colors: List[Color], occasion: Optional[Occasion] = None, 
                              style: Optional[Style] = None, season: Optional[Season] = None) -> Tuple[bool, str, float]:
    """Validate if a set of colors work well together."""
    if len(colors) < 2:
        return True, "Single color is always valid", 1.0
    
    color_strs = [c.value.lower() for c in colors]
    
    # Check if all are neutrals
    all_neutrals = all(c in NEUTRAL_COLORS for c in colors)
    if all_neutrals:
        return True, "Neutral colors always work well together", 1.0
    
    # Check classic combinations
    for primary, secondary in CLASSIC_COMBINATIONS:
        primary_set = set(primary)
        if any(c in primary_set for c in color_strs):
            if secondary == "any":
                return True, "Colors work well with neutrals", 0.95
            if any(c in secondary for c in color_strs):
                return True, "Classic, timeless combination", 0.95
    
    # Check warm/cool balance
    warm_count = sum(1 for c in colors if c in WARM_COLORS)
    cool_count = sum(1 for c in colors if c in COOL_COLORS)
    neutral_count = sum(1 for c in colors if c in NEUTRAL_COLORS)
    
    if warm_count > 0 and cool_count > 0:
        if neutral_count > 0:
            return True, "Warm and cool colors balanced with neutrals", 0.8
        else:
            return True, "Mixing warm and cool can work with careful styling", 0.6
    
    # Check if from same color family
    color_families = []
    for color in colors:
        for family, family_colors in COLOR_FAMILIES.items():
            if color in family_colors:
                color_families.append(family)
                break
    
    if len(set(color_families)) == 1 and len(colors) > 1:
        return True, f"Monochromatic {color_families[0]} scheme - elegant and cohesive", 0.95
    
    # Check occasion appropriateness
    if occasion and occasion in OCCASION_COLORS:
        occasion_info = OCCASION_COLORS[occasion]
        if occasion_info.get("primary") != "any":
            avoid = [c.value.lower() for c in occasion_info.get("avoid", [])]
            for color in color_strs:
                if color in avoid:
                    return False, f"{color} is not appropriate for {occasion.value}", 0.3
    
    return True, "Acceptable color combination", 0.7

def suggest_colors_for_occasion(occasion: Occasion, style: Optional[Style] = None, 
                               season: Optional[Season] = None, count: int = 3) -> List[Color]:
    """Suggest appropriate colors for an occasion"""
    suggested = []
    
    if occasion in OCCASION_COLORS:
        occasion_colors = OCCASION_COLORS[occasion].get("primary", [])
        if occasion_colors != "any":
            suggested.extend(occasion_colors)
    
    if style and style in STYLE_COLORS:
        style_colors = STYLE_COLORS[style].get("primary", [])
        if style_colors != "any":
            suggested.extend(style_colors)
    
    # if season and season in SEASONAL_COLORS:
    #     suggested.extend(SEASONAL_COLORS[season].get("primary", []))
    
    # Remove duplicates
    unique = []
    seen = set()
    for color in suggested:
        if color.value not in seen:
            seen.add(color.value)
            unique.append(color)
    
    return unique[:count]

def get_color_family(color: Color) -> str:
    """Get the family a color belongs to"""
    for family, colors in COLOR_FAMILIES.items():
        if color in colors:
            return family
    return "other"

def get_color_temperature(color: Color) -> str:
    """Get whether a color is warm, cool, or neutral"""
    if color in WARM_COLORS:
        return "warm"
    elif color in COOL_COLORS:
        return "cool"
    else:
        return "neutral"

def calculate_color_harmony_score(colors: List[Color]) -> float:
    """Calculate a harmony score for a set of colors (0-1)"""
    if len(colors) < 2:
        return 1.0
    
    score = 0.0
    checks = 0
    
    for i in range(len(colors)):
        for j in range(i+1, len(colors)):
            if get_color_family(colors[i]) == get_color_family(colors[j]):
                score += 0.9
            elif colors[i] in NEUTRAL_COLORS or colors[j] in NEUTRAL_COLORS:
                score += 0.85
            else:
                score += 0.6
            checks += 1
    
    return score / checks if checks > 0 else 1.0
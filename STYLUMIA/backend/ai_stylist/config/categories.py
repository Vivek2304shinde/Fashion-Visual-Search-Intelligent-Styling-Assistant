"""
Dynamic category configuration - This is the SINGLE source of truth for all categories.
Adding a new category here automatically makes it available to all agents.
"""

from typing import Dict, List, Any, Optional
from ai_stylist.schemas import CategoryGroup, Gender, Fit, Fabric, Season

# ==================== CATEGORY CONFIGURATION ====================

# Main category configuration - Add new categories HERE only
OUTFIT_CATEGORIES = {
    # Upper Body
    "shirt": {
        "group": CategoryGroup.UPPER_BODY,
        "display_name": "Shirt",
        "search_terms": ["shirt", "formal shirt", "casual shirt"],
        "priority": 1,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.COTTON, Fabric.LINEN, Fabric.POLYESTER, Fabric.SILK],
        "common_fits": [Fit.SLIM, Fit.REGULAR, Fit.RELAXED],
        "seasonal": [Season.SUMMER, Season.SPRING, Season.FALL],
        "alternatives": ["t_shirt", "blouse", "kurta"]
    },
    "t_shirt": {
        "group": CategoryGroup.UPPER_BODY,
        "display_name": "T-Shirt",
        "search_terms": ["t-shirt", "tee", "casual tshirt"],
        "priority": 1,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.COTTON, Fabric.POLYESTER, Fabric.BLEND, Fabric.JERSEY],
        "common_fits": [Fit.REGULAR, Fit.SLIM, Fit.OVERSIZED],
        "seasonal": [Season.SUMMER, Season.SPRING],
        "alternatives": ["shirt", "polo", "vest"]
    },
    "polo": {
        "group": CategoryGroup.UPPER_BODY,
        "display_name": "Polo Shirt",
        "search_terms": ["polo", "polo shirt", "golf shirt"],
        "priority": 2,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.COTTON, Fabric.PIQUE, Fabric.BLEND],
        "common_fits": [Fit.REGULAR, Fit.SLIM],
        "seasonal": [Season.SUMMER, Season.SPRING, Season.FALL],
        "alternatives": ["t_shirt", "shirt"]
    },
    "blouse": {
        "group": CategoryGroup.UPPER_BODY,
        "display_name": "Blouse",
        "search_terms": ["blouse", "women top", "formal blouse"],
        "priority": 1,
        "gender": [Gender.FEMALE],
        "common_fabrics": [Fabric.SILK, Fabric.COTTON, Fabric.CHIFFON, Fabric.GEORGETTE, Fabric.SATIN],
        "common_fits": [Fit.SLIM, Fit.REGULAR],
        "seasonal": [Season.SUMMER, Season.SPRING, Season.FALL],
        "alternatives": ["shirt", "top", "kurti"]
    },
    "sweater": {
        "group": CategoryGroup.UPPER_BODY,
        "display_name": "Sweater",
        "search_terms": ["sweater", "pullover", "knitwear"],
        "priority": 2,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.WOOL, Fabric.CASHMERE, Fabric.ACRYLIC, Fabric.COTTON, Fabric.SWEATER_KNIT],
        "common_fits": [Fit.REGULAR, Fit.RELAXED, Fit.OVERSIZED],
        "seasonal": [Season.WINTER, Season.FALL],
        "alternatives": ["cardigan", "hoodie", "jacket"]
    },
    "hoodie": {
        "group": CategoryGroup.UPPER_BODY,
        "display_name": "Hoodie",
        "search_terms": ["hoodie", "hooded sweatshirt"],
        "priority": 2,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.COTTON, Fabric.FLEECE, Fabric.POLAR_FLEECE, Fabric.POLYESTER],
        "common_fits": [Fit.REGULAR, Fit.OVERSIZED],
        "seasonal": [Season.WINTER, Season.FALL, Season.SPRING],
        "alternatives": ["sweater", "jacket", "sweatshirt"]
    },
    "crop_top": {
        "group": CategoryGroup.UPPER_BODY,
        "display_name": "Crop Top",
        "search_terms": ["crop top", "cropped top"],
        "priority": 2,
        "gender": [Gender.FEMALE],
        "common_fabrics": [Fabric.COTTON, Fabric.POLYESTER, Fabric.BLEND, Fabric.JERSEY],
        "common_fits": [Fit.SLIM, Fit.CROPPED],
        "seasonal": [Season.SUMMER, Season.SPRING],
        "alternatives": ["top", "blouse", "t_shirt"]
    },
    "tank_top": {
        "group": CategoryGroup.UPPER_BODY,
        "display_name": "Tank Top",
        "search_terms": ["tank top", "vest top", "sleeveless"],
        "priority": 2,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.COTTON, Fabric.POLYESTER, Fabric.BLEND, Fabric.RIBBED],
        "common_fits": [Fit.SLIM, Fit.REGULAR],
        "seasonal": [Season.SUMMER, Season.SPRING],
        "alternatives": ["t_shirt", "crop_top"]
    },
    "kurti": {
        "group": CategoryGroup.ETHNIC,
        "display_name": "Kurti",
        "search_terms": ["kurti", "ethnic top", "long kurta"],
        "priority": 1,
        "gender": [Gender.FEMALE],
        "common_fabrics": [Fabric.COTTON, Fabric.SILK, Fabric.CHIFFON, Fabric.GEORGETTE, Fabric.BANARASI_SILK],
        "common_fits": [Fit.REGULAR, Fit.RELAXED],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["kurta", "blouse", "ethnic_top"]
    },
    
    # Lower Body
    "pants": {
        "group": CategoryGroup.LOWER_BODY,
        "display_name": "Pants",
        "search_terms": ["pants", "trousers", "formal pants"],
        "priority": 1,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.COTTON, Fabric.POLYESTER, Fabric.WOOL, Fabric.LINEN, Fabric.TWILL],
        "common_fits": [Fit.SLIM, Fit.REGULAR, Fit.RELAXED, Fit.STRAIGHT],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["jeans", "chinos", "shorts"]
    },
    "jeans": {
        "group": CategoryGroup.LOWER_BODY,
        "display_name": "Jeans",
        "search_terms": ["jeans", "denim"],
        "priority": 1,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.DENIM, Fabric.COTTON],
        "common_fits": [Fit.SKINNY, Fit.SLIM, Fit.REGULAR, Fit.RELAXED, Fit.BOOTCUT],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["pants", "chinos", "shorts"]
    },
    "chinos": {
        "group": CategoryGroup.LOWER_BODY,
        "display_name": "Chinos",
        "search_terms": ["chinos", "khaki pants", "casual pants"],
        "priority": 2,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.COTTON, Fabric.CHINO, Fabric.TWILL],
        "common_fits": [Fit.SLIM, Fit.REGULAR],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["pants", "jeans"]
    },
    "shorts": {
        "group": CategoryGroup.LOWER_BODY,
        "display_name": "Shorts",
        "search_terms": ["shorts", "bermuda", "cargo shorts"],
        "priority": 2,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.COTTON, Fabric.DENIM, Fabric.POLYESTER, Fabric.LINEN],
        "common_fits": [Fit.REGULAR, Fit.RELAXED],
        "seasonal": [Season.SUMMER, Season.SPRING],
        "alternatives": ["pants", "jeans"]
    },
    "skirt": {
        "group": CategoryGroup.LOWER_BODY,
        "display_name": "Skirt",
        "search_terms": ["skirt", "mini skirt", "midi skirt", "maxi skirt"],
        "priority": 2,
        "gender": [Gender.FEMALE],
        "common_fabrics": [Fabric.COTTON, Fabric.DENIM, Fabric.SILK, Fabric.POLYESTER, Fabric.CHIFFON],
        "common_fits": [Fit.REGULAR, Fit.A_LINE, Fit.FLARED],
        "seasonal": [Season.SUMMER, Season.SPRING, Season.FALL],
        "alternatives": ["dress", "shorts"]
    },
    "leggings": {
        "group": CategoryGroup.LOWER_BODY,
        "display_name": "Leggings",
        "search_terms": ["leggings", "tights"],
        "priority": 3,
        "gender": [Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.COTTON, Fabric.SPANDEX, Fabric.POLYESTER, Fabric.LYCRA],
        "common_fits": [Fit.SLIM, Fit.SKINNY, Fit.COMPRESSION],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["pants", "jeans"]
    },
    "churidar": {
        "group": CategoryGroup.LOWER_BODY,
        "display_name": "Churidar",
        "search_terms": ["churidar", "churidar pants", "fitted pants"],
        "priority": 2,
        "gender": [Gender.FEMALE, Gender.MALE],
        "common_fabrics": [Fabric.COTTON, Fabric.SILK, Fabric.LYCRA, Fabric.BLEND],
        "common_fits": [Fit.SLIM, Fit.SKINNY],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["leggings", "pants"]
    },
    "palazzo": {
        "group": CategoryGroup.LOWER_BODY,
        "display_name": "Palazzo",
        "search_terms": ["palazzo", "palazzo pants", "wide leg pants"],
        "priority": 2,
        "gender": [Gender.FEMALE],
        "common_fabrics": [Fabric.COTTON, Fabric.SILK, Fabric.VISCOSE, Fabric.GEORGETTE],
        "common_fits": [Fit.WIDE_LEG, Fit.FLARED, Fit.PALAZZO],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["pants", "skirt"]
    },
    "dhoti": {
        "group": CategoryGroup.LOWER_BODY,
        "display_name": "Dhoti",
        "search_terms": ["dhoti", "dhoti pants", "ethnic dhoti"],
        "priority": 3,
        "gender": [Gender.MALE, Gender.FEMALE],
        "common_fabrics": [Fabric.COTTON, Fabric.SILK, Fabric.LINEN],
        "common_fits": [Fit.REGULAR, Fit.RELAXED],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["pants", "lungi"]
    },
    
    # One-Piece
    "dress": {
        "group": CategoryGroup.ONE_PIECE,
        "display_name": "Dress",
        "search_terms": ["dress", "gown", "frock"],
        "priority": 1,
        "gender": [Gender.FEMALE],
        "common_fabrics": [Fabric.COTTON, Fabric.SILK, Fabric.POLYESTER, Fabric.CHIFFON, Fabric.SATIN],
        "common_fits": [Fit.REGULAR, Fit.A_LINE, Fit.WRAP, Fit.EMPIRE],
        "seasonal": [Season.SUMMER, Season.SPRING, Season.FALL],
        "alternatives": ["jumpsuit", "skirt_set"]
    },
    "jumpsuit": {
        "group": CategoryGroup.ONE_PIECE,
        "display_name": "Jumpsuit",
        "search_terms": ["jumpsuit", "playsuit", "romper"],
        "priority": 2,
        "gender": [Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.COTTON, Fabric.POLYESTER, Fabric.LINEN, Fabric.CREPE],
        "common_fits": [Fit.REGULAR, Fit.SLIM, Fit.RELAXED],
        "seasonal": [Season.SUMMER, Season.SPRING],
        "alternatives": ["dress", "pants_set"]
    },
    "suit": {
        "group": CategoryGroup.ONE_PIECE,
        "display_name": "Suit",
        "search_terms": ["suit", "blazer suit", "formal suit"],
        "priority": 1,
        "gender": [Gender.MALE, Gender.FEMALE],
        "common_fabrics": [Fabric.WOOL, Fabric.POLYESTER, Fabric.LINEN, Fabric.COTTON, Fabric.BLEND],
        "common_fits": [Fit.SLIM, Fit.REGULAR, Fit.TAILORED],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["blazer", "jacket"]
    },
    "gown": {
        "group": CategoryGroup.ONE_PIECE,
        "display_name": "Gown",
        "search_terms": ["gown", "evening gown", "ball gown"],
        "priority": 2,
        "gender": [Gender.FEMALE],
        "common_fabrics": [Fabric.SILK, Fabric.SATIN, Fabric.VELVET, Fabric.NET, Fabric.TULLE],
        "common_fits": [Fit.REGULAR, Fit.FLARED, Fit.EMPIRE, Fit.A_LINE],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["dress", "lehenga"]
    },
    "saree": {
        "group": CategoryGroup.ETHNIC,
        "display_name": "Saree",
        "search_terms": ["saree", "sari", "ethnic saree"],
        "priority": 1,
        "gender": [Gender.FEMALE],
        "common_fabrics": [Fabric.SILK, Fabric.COTTON, Fabric.CHIFFON, Fabric.GEORGETTE, 
                          Fabric.BANARASI_SILK, Fabric.KANCHIPURAM_SILK],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["lehenga", "anarkali"]
    },
    "lehenga": {
        "group": CategoryGroup.ETHNIC,
        "display_name": "Lehenga",
        "search_terms": ["lehenga", "lehenga choli"],
        "priority": 1,
        "gender": [Gender.FEMALE],
        "common_fabrics": [Fabric.SILK, Fabric.VELVET, Fabric.NET, Fabric.GEORGETTE, Fabric.BROCADE],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["saree", "ghagra"]
    },
    "anarkali": {
        "group": CategoryGroup.ETHNIC,
        "display_name": "Anarkali",
        "search_terms": ["anarkali", "anarkali suit", "frock style"],
        "priority": 2,
        "gender": [Gender.FEMALE],
        "common_fabrics": [Fabric.SILK, Fabric.GEORGETTE, Fabric.CHIFFON, Fabric.COTTON],
        "common_fits": [Fit.FLARED, Fit.A_LINE, Fit.REGULAR],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["kurta", "dress"]
    },
    "sherwani": {
        "group": CategoryGroup.ETHNIC,
        "display_name": "Sherwani",
        "search_terms": ["sherwani", "wedding sherwani"],
        "priority": 1,
        "gender": [Gender.MALE],
        "common_fabrics": [Fabric.SILK, Fabric.VELVET, Fabric.BROCADE, Fabric.JACQUARD],
        "common_fits": [Fit.REGULAR, Fit.TAILORED],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["achkan", "bandhgala"]
    },
    "kurta": {
        "group": CategoryGroup.ETHNIC,
        "display_name": "Kurta",
        "search_terms": ["kurta", "ethnic kurta", "kurti"],
        "priority": 1,
        "gender": [Gender.MALE, Gender.FEMALE],
        "common_fabrics": [Fabric.COTTON, Fabric.SILK, Fabric.LINEN],
        "common_fits": [Fit.REGULAR, Fit.RELAXED],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["shirt", "sherwani"]
    },
    
    # Layering
    "jacket": {
        "group": CategoryGroup.LAYERING,
        "display_name": "Jacket",
        "search_terms": ["jacket", "bomber jacket", "denim jacket"],
        "priority": 2,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.DENIM, Fabric.LEATHER, Fabric.COTTON, Fabric.POLYESTER, Fabric.FAUX_LEATHER],
        "common_fits": [Fit.REGULAR, Fit.RELAXED, Fit.OVERSIZED],
        "seasonal": [Season.WINTER, Season.FALL, Season.SPRING],
        "alternatives": ["blazer", "coat", "hoodie"]
    },
    "blazer": {
        "group": CategoryGroup.LAYERING,
        "display_name": "Blazer",
        "search_terms": ["blazer", "sport coat"],
        "priority": 2,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.WOOL, Fabric.POLYESTER, Fabric.LINEN, Fabric.COTTON, Fabric.BLEND],
        "common_fits": [Fit.SLIM, Fit.REGULAR, Fit.TAILORED],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["jacket", "suit_jacket"]
    },
    "coat": {
        "group": CategoryGroup.LAYERING,
        "display_name": "Coat",
        "search_terms": ["coat", "overcoat", "trench coat"],
        "priority": 2,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.WOOL, Fabric.CASHMERE, Fabric.POLYESTER, Fabric.GABARDINE],
        "common_fits": [Fit.REGULAR, Fit.RELAXED],
        "seasonal": [Season.WINTER],
        "alternatives": ["jacket", "blazer"]
    },
    "trench_coat": {
        "group": CategoryGroup.LAYERING,
        "display_name": "Trench Coat",
        "search_terms": ["trench coat", "trench"],
        "priority": 3,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.COTTON, Fabric.GABARDINE, Fabric.POLYESTER],
        "common_fits": [Fit.REGULAR, Fit.RELAXED],
        "seasonal": [Season.FALL, Season.SPRING, Season.MONSOON],
        "alternatives": ["coat", "raincoat"]
    },
    "cardigan": {
        "group": CategoryGroup.LAYERING,
        "display_name": "Cardigan",
        "search_terms": ["cardigan", "knit cardigan"],
        "priority": 3,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.WOOL, Fabric.COTTON, Fabric.ACRYLIC, Fabric.SWEATER_KNIT],
        "common_fits": [Fit.REGULAR, Fit.RELAXED, Fit.OVERSIZED],
        "seasonal": [Season.WINTER, Season.FALL, Season.SPRING],
        "alternatives": ["sweater", "jacket"]
    },
    "vest": {
        "group": CategoryGroup.LAYERING,
        "display_name": "Vest",
        "search_terms": ["vest", "waistcoat", "suit vest"],
        "priority": 3,
        "gender": [Gender.MALE, Gender.FEMALE],
        "common_fabrics": [Fabric.WOOL, Fabric.COTTON, Fabric.POLYESTER, Fabric.SILK],
        "common_fits": [Fit.SLIM, Fit.REGULAR, Fit.TAILORED],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["jacket", "blazer"]
    },
    "waistcoat": {
        "group": CategoryGroup.LAYERING,
        "display_name": "Waistcoat",
        "search_terms": ["waistcoat", "vest"],
        "priority": 3,
        "gender": [Gender.MALE, Gender.FEMALE],
        "common_fabrics": [Fabric.WOOL, Fabric.COTTON, Fabric.SILK, Fabric.BROCADE],
        "common_fits": [Fit.SLIM, Fit.REGULAR, Fit.TAILORED],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["vest", "jacket"]
    },
    "overshirt": {
        "group": CategoryGroup.LAYERING,
        "display_name": "Overshirt",
        "search_terms": ["overshirt", "shirt jacket", "shacket"],
        "priority": 3,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.COTTON, Fabric.FLANNEL, Fabric.DENIM, Fabric.TWILL],
        "common_fits": [Fit.REGULAR, Fit.RELAXED, Fit.OVERSIZED],
        "seasonal": [Season.FALL, Season.SPRING],
        "alternatives": ["shirt", "jacket"]
    },
    "shawl": {
        "group": CategoryGroup.LAYERING,
        "display_name": "Shawl",
        "search_terms": ["shawl", "wrap", "stole"],
        "priority": 4,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.WOOL, Fabric.CASHMERE, Fabric.SILK],
        "seasonal": [Season.WINTER, Season.FALL],
        "alternatives": ["dupatta", "scarf"]
    },
    "dupatta": {
        "group": CategoryGroup.ETHNIC,
        "display_name": "Dupatta",
        "search_terms": ["dupatta", "chunni", "ethnic stole"],
        "priority": 3,
        "gender": [Gender.FEMALE],
        "common_fabrics": [Fabric.SILK, Fabric.COTTON, Fabric.CHIFFON, Fabric.NET],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["stole", "shawl"]
    },
    
    # Footwear
    "sneakers": {
        "group": CategoryGroup.FOOTWEAR,
        "display_name": "Sneakers",
        "search_terms": ["sneakers", "sports shoes", "running shoes"],
        "priority": 1,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_materials": [Fabric.LEATHER, Fabric.CANVAS,  Fabric.MESH],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["casual_shoes", "sports_shoes"]
    },
    "formal_shoes": {
        "group": CategoryGroup.FOOTWEAR,
        "display_name": "Formal Shoes",
        "search_terms": ["formal shoes", "oxford shoes", "derby shoes"],
        "priority": 1,
        "gender": [Gender.MALE, Gender.FEMALE],
        "common_materials": [Fabric.LEATHER],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["loafers", "brogues"]
    },
    "boots": {
        "group": CategoryGroup.FOOTWEAR,
        "display_name": "Boots",
        "search_terms": ["boots", "ankle boots", "chelsea boots"],
        "priority": 2,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_materials": [Fabric.LEATHER, Fabric.SUEDE],
        "seasonal": [Season.WINTER, Season.FALL],
        "alternatives": ["shoes", "sneakers"]
    },
    "heels": {
        "group": CategoryGroup.FOOTWEAR,
        "display_name": "Heels",
        "search_terms": ["heels", "pumps", "stilettos"],
        "priority": 2,
        "gender": [Gender.FEMALE],
        "common_materials": [Fabric.LEATHER, Fabric.SATIN, ],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["wedges", "platforms"]
    },
    "sandals": {
        "group": CategoryGroup.FOOTWEAR,
        "display_name": "Sandals",
        "search_terms": ["sandals", "slides", "flip flops"],
        "priority": 3,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_materials": [Fabric.LEATHER, Fabric.RIBBED],
        "seasonal": [Season.SUMMER],
        "alternatives": ["slippers", "flats"]
    },
    "loafers": {
        "group": CategoryGroup.FOOTWEAR,
        "display_name": "Loafers",
        "search_terms": ["loafers", "slip ons", "moccasins"],
        "priority": 2,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_materials": [Fabric.LEATHER, Fabric.SUEDE],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["formal_shoes", "sneakers"]
    },
    "ethnic_footwear": {
        "group": CategoryGroup.FOOTWEAR,
        "display_name": "Ethnic Footwear",
        "search_terms": ["mojari", "jutti", "ethnic shoes"],
        "priority": 2,
        "gender": [Gender.MALE, Gender.FEMALE],
        "common_materials": [Fabric.LEATHER, Fabric.VELVET, Fabric.SILK],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["sandals", "loafers"]
    },
    "mojari": {
        "group": CategoryGroup.FOOTWEAR,
        "display_name": "Mojari",
        "search_terms": ["mojari", "ethnic mojari"],
        "priority": 3,
        "gender": [Gender.MALE, Gender.FEMALE],
        "common_materials": [Fabric.LEATHER, Fabric.VELVET, Fabric.SILK],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["jutti", "ethnic_footwear"]
    },
    "jutti": {
        "group": CategoryGroup.FOOTWEAR,
        "display_name": "Jutti",
        "search_terms": ["jutti", "punjabi jutti"],
        "priority": 3,
        "gender": [Gender.MALE, Gender.FEMALE],
        "common_materials": [Fabric.LEATHER, Fabric.VELVET, Fabric.SILK],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["mojari", "ethnic_footwear"]
    },
    
    # Jewelry
    "earrings": {
        "group": CategoryGroup.JEWELRY,
        "display_name": "Earrings",
        "search_terms": ["earrings", "jhumkas", "studs"],
        "priority": 2,
        "gender": [Gender.FEMALE, Gender.UNISEX],
        "common_materials": ["gold", "silver", "fashion_jewelry"],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["ear_cuffs", "clip_ons"]
    },
    "necklace": {
        "group": CategoryGroup.JEWELRY,
        "display_name": "Necklace",
        "search_terms": ["necklace", "chain", "pendant set"],
        "priority": 2,
        "gender": [Gender.FEMALE, Gender.MALE],
        "common_materials": ["gold", "silver", "diamond", "fashion"],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["pendant", "choker"]
    },
    "rings": {
        "group": CategoryGroup.JEWELRY,
        "display_name": "Rings",
        "search_terms": ["rings", "signet ring", "wedding band"],
        "priority": 3,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_materials": ["gold", "silver", "platinum", "steel"],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["band", "statement_ring"]
    },
    "bracelet": {
        "group": CategoryGroup.JEWELRY,
        "display_name": "Bracelet",
        "search_terms": ["bracelet", "chain bracelet"],
        "priority": 3,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_materials": ["gold", "silver", "leather", "beaded"],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["bangles", "cuff"]
    },
    "bangles": {
        "group": CategoryGroup.JEWELRY,
        "display_name": "Bangles",
        "search_terms": ["bangles", "kada", "glass bangles"],
        "priority": 3,
        "gender": [Gender.FEMALE],
        "common_materials": ["gold", "glass", "metal", "acrylic"],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["bracelet", "kada"]
    },
    "anklet": {
        "group": CategoryGroup.JEWELRY,
        "display_name": "Anklet",
        "search_terms": ["anklet", "payal", "foot chain"],
        "priority": 4,
        "gender": [Gender.FEMALE],
        "common_materials": ["silver", "gold", "fashion"],
        "seasonal": [Season.SUMMER],
        "alternatives": ["bracelet", "chain"]
    },
    
    # Watches
    "watch": {
        "group": CategoryGroup.WATCHES,
        "display_name": "Watch",
        "search_terms": ["watch", "analog watch", "digital watch"],
        "priority": 2,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_materials": ["leather", "metal", "silicone"],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["smartwatch", "fitness_tracker"]
    },
    "smartwatch": {
        "group": CategoryGroup.WATCHES,
        "display_name": "Smartwatch",
        "search_terms": ["smartwatch", "fitness watch", "smart band"],
        "priority": 3,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_materials": ["silicone", "metal", "plastic"],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["watch", "fitness_tracker"]
    },
    
    # Accessories
    "sunglasses": {
        "group": CategoryGroup.ACCESSORIES,
        "display_name": "Sunglasses",
        "search_terms": ["sunglasses", "sun glasses", "aviators"],
        "priority": 2,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_materials": ["acetate", "metal", "plastic"],
        "seasonal": [Season.SUMMER, Season.SPRING],
        "alternatives": ["eyewear", "glasses"]
    },
    "belt": {
        "group": CategoryGroup.ACCESSORIES,
        "display_name": "Belt",
        "search_terms": ["belt", "leather belt", "dress belt"],
        "priority": 3,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_materials": [Fabric.LEATHER, "metal"],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["waist_chain", "sash"]
    },
    "bag": {
        "group": CategoryGroup.BAGS,
        "display_name": "Bag",
        "search_terms": ["bag", "handbag", "backpack"],
        "priority": 2,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_materials": [Fabric.LEATHER, Fabric.CANVAS, Fabric.NYLON, Fabric.POLYESTER],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["backpack", "tote", "clutch"]
    },
    "wallet": {
        "group": CategoryGroup.BAGS,
        "display_name": "Wallet",
        "search_terms": ["wallet", "card holder", "money clip"],
        "priority": 4,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_materials": [Fabric.LEATHER, "metal"],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["card_holder", "purse"]
    },
    "backpack": {
        "group": CategoryGroup.BAGS,
        "display_name": "Backpack",
        "search_terms": ["backpack", "rucksack", "school bag"],
        "priority": 3,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_materials": [Fabric.NYLON, Fabric.CANVAS, Fabric.POLYESTER, Fabric.LEATHER],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["bag", "messenger_bag"]
    },
    
    # Headwear
    "hat": {
        "group": CategoryGroup.HEADWEAR,
        "display_name": "Hat",
        "search_terms": ["hat", "fedora", "sun hat"],
        "priority": 3,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_materials": [Fabric.COTTON, Fabric.WOOL, "straw", "felt"],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["cap", "beanie"]
    },
    "cap": {
        "group": CategoryGroup.HEADWEAR,
        "display_name": "Cap",
        "search_terms": ["cap", "baseball cap", "snapback"],
        "priority": 3,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_materials": [Fabric.COTTON, Fabric.POLYESTER, Fabric.WOOL],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["hat", "visor"]
    },
    "beanie": {
        "group": CategoryGroup.HEADWEAR,
        "display_name": "Beanie",
        "search_terms": ["beanie", "knit cap", "winter hat"],
        "priority": 3,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_materials": [Fabric.WOOL, Fabric.ACRYLIC, Fabric.COTTON],
        "seasonal": [Season.WINTER],
        "alternatives": ["hat", "ear_muffs"]
    },
    "pagdi": {
        "group": CategoryGroup.HEADWEAR,
        "display_name": "Pagdi",
        "search_terms": ["pagdi", "turban", "safa"],
        "priority": 3,
        "gender": [Gender.MALE],
        "common_fabrics": [Fabric.SILK, Fabric.COTTON, Fabric.VELVET],
        "seasonal": [Season.ALL_SEASON],
        "alternatives": ["hat", "cap"]
    },
    
    # Seasonal
    "scarf": {
        "group": CategoryGroup.SEASONAL,
        "display_name": "Scarf",
        "search_terms": ["scarf", "muffler", "winter scarf"],
        "priority": 3,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.WOOL, Fabric.CASHMERE, Fabric.ACRYLIC, Fabric.SILK],
        "seasonal": [Season.WINTER, Season.FALL],
        "alternatives": ["stole", "muffler"]
    },
    "gloves": {
        "group": CategoryGroup.SEASONAL,
        "display_name": "Gloves",
        "search_terms": ["gloves", "winter gloves", "hand gloves"],
        "priority": 4,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_materials": [Fabric.WOOL, Fabric.LEATHER, Fabric.FLEECE],
        "seasonal": [Season.WINTER],
        "alternatives": ["hand_warmers", "mittens"]
    },
    "muffler": {
        "group": CategoryGroup.SEASONAL,
        "display_name": "Muffler",
        "search_terms": ["muffler", "winter scarf", "neck warmer"],
        "priority": 4,
        "gender": [Gender.MALE, Gender.FEMALE, Gender.UNISEX],
        "common_fabrics": [Fabric.WOOL, Fabric.ACRYLIC, Fabric.FLEECE],
        "seasonal": [Season.WINTER],
        "alternatives": ["scarf", "stole"]
    }
}

# Helper functions to work with categories
def get_all_categories() -> List[str]:
    """Get all category names"""
    return list(OUTFIT_CATEGORIES.keys())

def get_categories_by_group(group: CategoryGroup) -> List[str]:
    """Get all categories in a specific group"""
    return [cat for cat, config in OUTFIT_CATEGORIES.items() 
            if config["group"] == group]

def get_category_config(category: str) -> dict:
    """Get configuration for a specific category"""
    return OUTFIT_CATEGORIES.get(category, {})

def get_category_display_name(category: str) -> str:
    """Get display name for a category"""
    return OUTFIT_CATEGORIES.get(category, {}).get("display_name", category)

def get_category_search_terms(category: str) -> List[str]:
    """Get search terms for a category"""
    return OUTFIT_CATEGORIES.get(category, {}).get("search_terms", [category])

def is_category_valid(category: str) -> bool:
    """Check if a category exists"""
    return category in OUTFIT_CATEGORIES

def get_priority_categories(limit: int = 5) -> List[str]:
    """Get highest priority categories"""
    sorted_cats = sorted(OUTFIT_CATEGORIES.items(), 
                        key=lambda x: x[1].get("priority", 5))
    return [cat[0] for cat in sorted_cats[:limit]]
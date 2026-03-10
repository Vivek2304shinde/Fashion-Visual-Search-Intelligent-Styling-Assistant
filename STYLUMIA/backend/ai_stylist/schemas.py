from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

# ==================== ENUMS FOR ALL CATEGORIES ====================

class UpperBodyCategory(str, Enum):
    SHIRT = "shirt"
    T_SHIRT = "t_shirt"
    POLO = "polo"
    BLOUSE = "blouse"
    SWEATER = "sweater"
    HOODIE = "hoodie"
    CROP_TOP = "crop_top"
    TANK_TOP = "tank_top"
    KURTA = "kurta"
    ETHNIC_TOP = "ethnic_top"

class LowerBodyCategory(str, Enum):
    PANTS = "pants"
    JEANS = "jeans"
    TROUSERS = "trousers"
    SHORTS = "shorts"
    SKIRT = "skirt"
    LEGGINGS = "leggings"
    CHURIDAR = "churidar"
    PALAZZO = "palazzo"
    DHOTI = "dhoti"

class OnePieceCategory(str, Enum):
    DRESS = "dress"
    JUMPSUIT = "jumpsuit"
    SUIT = "suit"
    SAREE = "saree"
    LEHENGA = "lehenga"
    GOWN = "gown"
    ANARKALI = "anarkali"
    SHERWANI = "sherwani"

class LayeringCategory(str, Enum):
    JACKET = "jacket"
    BLAZER = "blazer"
    COAT = "coat"
    TRENCH_COAT = "trench_coat"
    CARDIGAN = "cardigan"
    VEST = "vest"
    WAISTCOAT = "waistcoat"
    OVERSHIRT = "overshirt"
    NEHRU_JACKET = "nehru_jacket"
    SHAWL = "shawl"
    DUPATTA = "dupatta"

class FootwearCategory(str, Enum):
    SNEAKERS = "sneakers"
    FORMAL_SHOES = "formal_shoes"
    BOOTS = "boots"
    HEELS = "heels"
    SANDALS = "sandals"
    LOAFERS = "loafers"
    MOJARI = "mojari"
    JUTTI = "jutti"
    ESPADRILLES = "espadrilles"
    FLIP_FLOPS = "flip_flops"
    ETHNIC_FOOTWEAR = "ethnic_footwear"

class JewelryCategory(str, Enum):
    EARRINGS = "earrings"
    JHUMPKA = "jhumka"
    NECKLACE = "necklace"
    PENDANT = "pendant"
    CHAIN = "chain"
    RINGS = "rings"
    BRACELET = "bracelet"
    BANGLES = "bangles"
    ANKLET = "anklet"
    NOSE_RING = "nose_ring"
    NOSE_PIN = "nose_pin"
    MAANG_TIKA = "maang_tika"
    KAMARBANDH = "kamarbandh"

class WatchCategory(str, Enum):
    ANALOG_WATCH = "analog_watch"
    DIGITAL_WATCH = "digital_watch"
    SMARTWATCH = "smartwatch"
    CHRONOGRAPH = "chronograph"
    DRESS_WATCH = "dress_watch"
    SPORTS_WATCH = "sports_watch"
    LUXURY_WATCH = "luxury_watch"
    CASUAL_WATCH = "casual_watch"

class BagCategory(str, Enum):
    HANDBAG = "handbag"
    SHOULDER_BAG = "shoulder_bag"
    TOTE_BAG = "tote_bag"
    BACKPACK = "backpack"
    CLUTCH = "clutch"
    WALLET = "wallet"
    CARD_HOLDER = "card_holder"
    BRIEFCASE = "briefcase"
    DUFFLE_BAG = "duffle_bag"
    MESSENGER_BAG = "messenger_bag"
    SLING_BAG = "sling_bag"
    POTLI = "potli"

class HairAccessoryCategory(str, Enum):
    HAT = "hat"
    CAP = "cap"
    BEANIE = "beanie"
    HAIRBAND = "hairband"
    HEADBAND = "headband"
    HAIR_CLIP = "hair_clip"
    HAIR_PIN = "hair_pin"
    SCRUNCHIE = "scrunchie"
    TURBAN = "turban"
    PAGDI = "pagdi"
    SAFA = "safa"
    DUPATTA_HEAD_COVER = "dupatta_head_cover"
    HIJAB = "hijab"

class BeltCategory(str, Enum):
    BELT = "belt"
    LEATHER_BELT = "leather_belt"
    FABRIC_BELT = "fabric_belt"
    CHAIN_BELT = "chain_belt"
    WAIST_CHAIN = "waist_chain"
    KAMARBANDH_BELT = "kamarbandh_belt"

class SeasonalItemCategory(str, Enum):
    SCARF = "scarf"
    MUFFLER = "muffler"
    GLOVES = "gloves"
    WOOLEN_CAP = "woolen_cap"
    EAR_MUFFS = "ear_muffs"
    RAINCOAT = "raincoat"
    UMBRELLA = "umbrella"
    HAND_WARMER = "hand_warmer"

class EthnicCategory(str, Enum):
    SAREE = "saree"
    LEHENGA = "lehenga"
    KURTA = "kurta"
    SHERWANI = "sherwani"
    DUPATTA = "dupatta"
    ANARKALI = "anarkali"
    INDO_WESTERN = "indo_western"
    BANDHGALA = "bandhgala"
    JODHPURI = "jodhpuri"
    PATHANI = "pathani"
    DHOTI = "dhoti"
    LUNGI = "lungi"
    VESHTI = "veshti"
    MUNDU = "mundu"

# ==================== COLOR ENUM ====================

class Color(str, Enum):
    # Reds
    RED = "red"
    BRIGHT_RED = "bright_red"
    DARK_RED = "dark_red"
    MAROON = "maroon"
    BURGUNDY = "burgundy"
    WINE = "wine"
    CRIMSON = "crimson"
    SCARLET = "scarlet"
    BRICK_RED = "brick_red"
    RUST = "rust"
    TERRA_COTTA = "terra_cotta"
    MAHOGANY = "mahogany"
    RED_ORANGE = "red_orange"
    
    # Pinks
    PINK = "pink"
    HOT_PINK = "hot_pink"
    BABY_PINK = "baby_pink"
    BLUSH = "blush"
    ROSE = "rose"
    ROSE_GOLD = "rose_gold"
    MAGENTA = "magenta"
    FUCHSIA = "fuchsia"
    CORAL = "coral"
    PEACH = "peach"
    SALMON = "salmon"
    
    # Oranges
    ORANGE = "orange"
    TANGERINE = "tangerine"
    MANDARIN = "mandarin"
    PUMPKIN = "pumpkin"
    APRICOT = "apricot"
    PEACH_ORANGE = "peach_orange"
    BURNT_ORANGE = "burnt_orange"
    
    # Yellows
    YELLOW = "yellow"
    MUSTARD = "mustard"
    GOLD = "gold"
    GOLDEN = "golden"
    LEMON = "lemon"
    CANARY = "canary"
    OCHRE = "ochre"
    SAFFRON = "saffron"
    TURMERIC = "turmeric"
    SUNFLOWER = "sunflower"
    
    # Greens
    GREEN = "green"
    LIME = "lime"
    MINT = "mint"
    PISTACHIO = "pistachio"
    OLIVE = "olive"
    FOREST = "forest"
    EMERALD = "emerald"
    JADE = "jade"
    TEAL = "teal"
    SEA_GREEN = "sea_green"
    MOSS = "moss"
    SAGE = "sage"
    PINE = "pine"
    KHAKI = "khaki"
    ARMY_GREEN = "army_green"
    
    # Blues
    BLUE = "blue"
    SKY_BLUE = "sky_blue"
    BABY_BLUE = "baby_blue"
    POWDER_BLUE = "powder_blue"
    LIGHT_BLUE = "light_blue"
    NAVY = "navy"
    ROYAL_BLUE = "royal_blue"
    MIDNIGHT_BLUE = "midnight_blue"
    COBALT = "cobalt"
    DENIM = "denim"
    TURQUOISE = "turquoise"
    AQUA = "aqua"
    CYAN = "cyan"
    CERULEAN = "cerulean"
    SAPPHIRE = "sapphire"
    CORNFLOWER = "cornflower"
    
    # Purples
    PURPLE = "purple"
    LAVENDER = "lavender"
    LILAC = "lilac"
    VIOLET = "violet"
    PLUM = "plum"
    MAUVE = "mauve"
    EGGPLANT = "eggplant"
    GRAPE = "grape"
    INDIGO = "indigo"
    AMETHYST = "amethyst"
    
    # Browns
    BROWN = "brown"
    LIGHT_BROWN = "light_brown"
    DARK_BROWN = "dark_brown"
    TAN = "tan"
    BEIGE = "beige"
    CREAM = "cream"
    ECRU = "ecru"
    TAUPE = "taupe"
    CAMEL = "camel"
    KHAKI_BROWN = "khaki_brown"
    COFFEE = "coffee"
    MOCHA = "mocha"
    CHOCOLATE = "chocolate"
    CARAMEL = "caramel"
    HONEY = "honey"
    TOFFEE = "toffee"
    CINNAMON = "cinnamon"
    
    # Neutrals
    WHITE = "white"
    OFF_WHITE = "off_white"
    IVORY = "ivory"
    CREAM_WHITE = "cream_white"
    PEARL = "pearl"
    BLACK = "black"
    JET_BLACK = "jet_black"
    CHARCOAL = "charcoal"
    GREY = "grey"
    LIGHT_GREY = "light_grey"
    MEDIUM_GREY = "medium_grey"
    DARK_GREY = "dark_grey"
    SILVER = "silver"
    GUNMETAL = "gunmetal"
    
    # Metallics
    METALLIC = "metallic"
    GOLD_METALLIC = "gold_metallic"
    SILVER_METALLIC = "silver_metallic"
    COPPER = "copper"
    BRONZE = "bronze"
    
    # Multicolor/Patterns
    MULTICOLOR = "multicolor"
    PRINTED = "printed"
    PATTERNED = "patterned"
    TIE_DYE = "tie_dye"
    OMBRE = "ombre"
    FLORAL_PRINT = "floral_print"
    ABSTRACT_PRINT = "abstract_print"
    ETHNIC_PRINT = "ethnic_print"
    BANDHANI = "bandhani"
    IKAT = "ikat"
    PAISLEY = "paisley"
    
    ANY = "any"

# ==================== STYLE ENUM ====================

class Style(str, Enum):
    FORMAL = "formal"
    SEMI_FORMAL = "semi_formal"
    BUSINESS = "business"
    BUSINESS_CASUAL = "business_casual"
    SMART_CASUAL = "smart_casual"
    CASUAL = "casual"
    SPORTS = "sports"
    ATHLEISURE = "athleisure"
    STREETWEAR = "streetwear"
    URBAN = "urban"
    GRUNGE = "grunge"
    PUNK = "punk"
    ROCK = "rock"
    GOTHIC = "gothic"
    CLASSIC = "classic"
    PREPPY = "preppy"
    IVY_LEAGUE = "ivy_league"
    VINTAGE = "vintage"
    RETRO = "retro"
    RUSTIC = "rustic"
    COUNTRY = "country"
    WESTERN = "western"
    MINIMALIST = "minimalist"
    CONTEMPORARY = "contemporary"
    AVANT_GARDE = "avant_garde"
    EXPERIMENTAL = "experimental"
    ECLECTIC = "eclectic"
    TRADITIONAL = "traditional"
    ETHNIC = "ethnic"
    INDO_WESTERN = "indo_western"
    FUSION = "fusion"
    BOHEMIAN = "bohemian"
    BOHO = "boho"
    TRIBAL = "tribal"
    NORTH_INDIAN = "north_indian"
    SOUTH_INDIAN = "south_indian"
    EAST_INDIAN = "east_indian"
    WEST_INDIAN = "west_indian"
    PUNJABI = "punjabi"
    GUJARATI = "gujarati"
    RAJASTHANI = "rajasthani"
    MAHARASHTRIAN = "maharashtrian"
    BENGALI = "bengali"
    TAMILIAN = "tamilian"
    TELUGU = "telugu"
    KANNADIGA = "kannadiga"
    MALAYALI = "malayali"
    WEDDING = "wedding"
    PARTY = "party"
    CLUB = "club"
    DATE_NIGHT = "date_night"
    VACATION = "vacation"
    BEACH = "beach"
    FESTIVAL_WEAR = "festival_wear"
    PUJA_WEAR = "puja_wear"
    SUMMER = "summer"
    WINTER = "winter"
    MONSOON = "monsoon"
    SPRING = "spring"
    FALL = "fall"
    AUTUMN = "autumn"
    MILITARY = "military"
    SAFARI = "safari"
    NAVAL = "naval"
    AVIATOR = "aviator"
    RACING = "racing"
    MOTORCYCLE = "motorcycle"
    TWENTIES = "twenties"
    THIRTIES = "thirties"
    FORTIES = "forties"
    FIFTIES = "fifties"
    SIXTIES = "sixties"
    SEVENTIES = "seventies"
    EIGHTIES = "eighties"
    NINETIES = "nineties"
    Y2K = "y2k"
    ROMANTIC = "romantic"
    LUXURY = "luxury"
    FESTIVE = "festive"
    SPORTY = "sporty"
    ELEGANT = "elegant"
    RESORT = "resort"
    COCKTAIL = "cocktail"
    BLACK_TIE = "black_tie"
    WHITE_TIE = "white_tie"

# ==================== OCCASION ENUM ====================

class Occasion(str, Enum):
    CASUAL = "casual"
    OFFICE = "office"
    BUSINESS_MEETING = "business_meeting"
    INTERVIEW = "interview"
    DAILY_WEAR = "daily_wear"
    PARTY = "party"
    CLUB = "club"
    DATE = "date"
    DINNER = "dinner"
    BRUNCH = "brunch"
    COCKTAIL = "cocktail"
    FORMAL = "formal"
    SEMI_FORMAL = "semi_formal"
    BLACK_TIE = "black_tie"
    WHITE_TIE = "white_tie"
    RED_CARPET = "red_carpet"
    WEDDING = "wedding"
    RECEPTION = "reception"
    ENGAGEMENT = "engagement"
    MEHENDI = "mehendi"
    SANGEET = "sangeet"
    HALDI = "haldi"
    WEDDING_GUEST = "wedding_guest"
    BRIDAL = "bridal"
    GROOM = "groom"
    BRIDESMAID = "bridesmaid"
    GROOMSMAN = "groomsman"
    FESTIVAL = "festival"
    DIWALI = "diwali"
    HOLI = "holi"
    EID = "eid"
    CHRISTMAS = "christmas"
    NEW_YEAR = "new_year"
    DUSSEHRA = "dussehra"
    NAVRATRI = "navratri"
    GANESH_CHATURTHI = "ganesh_chaturthi"
    PONGAL = "pongal"
    BIHU = "bihu"
    LOHRI = "lohri"
    VACATION = "vacation"
    BEACH = "beach"
    CONCERT = "concert"
    SPORTS_EVENT = "sports_event"
    GRADUATION = "graduation"
    ANNIVERSARY = "anniversary"
    BIRTHDAY = "birthday"
    BABY_SHOWER = "baby_shower"
    POOJA = "pooja"
    TEMPLE_VISIT = "temple_visit"
    RELIGIOUS = "religious"
    CULTURAL = "cultural"

# ==================== OTHER ENUMS ====================

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNISEX = "unisex"
    BOYS = "boys"
    GIRLS = "girls"
    MEN = "men"
    WOMEN = "women"
    KIDS = "kids"

class AgeGroup(str, Enum):
    INFANT = "infant"
    TODDLER = "toddler"
    KIDS = "kids"
    TEEN = "teen"
    YOUNG_ADULT = "young_adult"
    ADULT = "adult"
    MATURE = "mature"

class Fit(str, Enum):
    XS = "xs"
    S = "s"
    M = "m"
    L = "l"
    XL = "xl"
    XXL = "xxl"
    XXXL = "xxxl"
    SLIM = "slim"
    REGULAR = "regular"
    RELAXED = "relaxed"
    LOOSE = "loose"
    OVERSIZED = "oversized"
    TAILORED = "tailored"
    CUSTOM = "custom"
    COMPRESSION = "compression"
    SKINNY = "skinny"
    BOOTCUT = "bootcut"
    FLARED = "flared"
    STRAIGHT = "straight"
    WIDE_LEG = "wide_leg"
    PALAZZO = "palazzo"
    CIGARETTE = "cigarette"
    CROPPED = "cropped"
    HIGH_WAIST = "high_waist"
    MID_WAIST = "mid_waist"
    LOW_WAIST = "low_waist"
    A_LINE = "a_line"
    WRAP = "wrap"
    EMPIRE = "empire"
    BOXY = "boxy"
    PEPLUM = "peplum"
    BELTED = "belted"

class Fabric(str, Enum):
    COTTON = "cotton"
    ORGANIC_COTTON = "organic_cotton"
    LINEN = "linen"
    SILK = "silk"
    WOOL = "wool"
    CASHMERE = "cashmere"
    HEMP = "hemp"
    JUTE = "jute"
    RAMIE = "ramie"
    BANARASI_SILK = "banarasi_silk"
    KANCHIPURAM_SILK = "kanchipuram_silk"
    MYSORE_SILK = "mysore_silk"
    TUSSAR_SILK = "tussar_silk"
    MULBERRY_SILK = "mulberry_silk"
    POLYESTER = "polyester"
    NYLON = "nylon"
    ACRYLIC = "acrylic"
    SPANDEX = "spandex"
    ELASTANE = "elastane"
    LYCRA = "lycra"
    RAYON = "rayon"
    VISCOSE = "viscose"
    MODAL = "modal"
    TENCEL = "tencel"
    ACETATE = "acetate"
    TRIACETATE = "triacetate"
    BLEND = "blend"
    COTTON_POLYESTER = "cotton_polyester"
    POLYESTER_SPANDEX = "polyester_spandex"
    COTTON_SPANDEX = "cotton_spandex"
    WOOL_BLEND = "wool_blend"
    DENIM = "denim"
    LEATHER = "leather"
    SUEDE = "suede"
    VELVET = "velvet"
    VELOUR = "velour"
    CORDS = "cords"
    CORDUROY = "corduroy"
    TWILL = "twill"
    CHINO = "chino"
    GABARDINE = "gabardine"
    FLANNEL = "flannel"
    FLEECE = "fleece"
    POLAR_FLEECE = "polar_fleece"
    SHERPA = "sherpa"
    FAUX_LEATHER = "faux_leather"
    FAUX_FUR = "faux_fur"
    FAUX_SUEDE = "faux_suede"
    CHIFFON = "chiffon"
    GEORGETTE = "georgette"
    SATIN = "satin"
    CHARMEUSE = "charmeuse"
    CREPE = "crepe"
    ORGANZA = "organza"
    ORGANDY = "organdy"
    NET = "net"
    TULLE = "tulle"
    LACE = "lace"
    MESH = "mesh"
    SEQUIN = "sequin"
    EMBROIDERED = "embroidered"
    BROCADE = "brocade"
    JACQUARD = "jacquard"
    DAMASK = "damask"
    JERSEY = "jersey"
    INTERLOCK = "interlock"
    RIBBED = "ribbed"
    PIQUE = "pique"
    SWEATER_KNIT = "sweater_knit"
    WATERPROOF = "waterproof"
    WINDPROOF = "windproof"
    BREATHABLE = "breathable"
    QUILTED = "quilted"
    INSULATED = "insulated"
    CANVAS = "canvas"
    MUSLIN = "muslin"
    CALICO = "calico"
    OXFORD = "oxford"
    POPLIN = "poplin"
    BROADCLOTH = "broadcloth"
    VOILE = "voile"
    SEERSUCKER = "seersucker"
    MADRAS = "madras"
    KHADI = "khadi"
    HANDLOOM = "handloom"

class Pattern(str, Enum):
    SOLID = "solid"
    PRINTED = "printed"
    STRIPED = "striped"
    CHECKED = "checked"
    PLAID = "plaid"
    POLKA_DOT = "polka_dot"
    FLORAL = "floral"
    PAISLEY = "paisley"
    ABSTRACT = "abstract"
    GEOMETRIC = "geometric"
    TIE_DYE = "tie_dye"
    OMBRE = "ombre"
    EMBROIDERED = "embroidered"
    PINSTRIPE = "pinstripe"
    CAMO = "camo"
    GRAPHIC = "graphic"
    COLOR_BLOCK = "color_block"
    ETHNIC = "ethnic"
    IKAT = "ikat"
    BANDHANI = "bandhani"
    LEOPARD = "leopard"
    ZEBRA = "zebra"
    ANIMAL = "animal"
    TRIBAL = "tribal"
    MADRAS = "madras"
    GINGHAM = "gingham"
    HOUNDSTOOTH = "houndstooth"
    HERRINGBONE = "herringbone"
    CHEVRON = "chevron"
    ARGYLE = "argyle"
    FAIR_ISLE = "fair_isle"
    JACQUARD = "jacquard"
    BROCADE = "brocade"
    DAMASK = "damask"
    TIE_AND_DYE = "tie_and_dye"
    SHIBORI = "shibori"
    BATIK = "batik"

class Season(str, Enum):
    SUMMER = "summer"
    WINTER = "winter"
    SPRING = "spring"
    FALL = "fall"
    AUTUMN = "autumn"
    MONSOON = "monsoon"
    ALL_SEASON = "all_season"

class PriceRange(str, Enum):
    BUDGET = "budget"
    ECONOMY = "economy"
    MID_RANGE = "mid_range"
    PREMIUM = "premium"
    LUXURY = "luxury"
    ULTRA_LUXURY = "ultra_luxury"

class CategoryGroup(str, Enum):
    UPPER_BODY = "upper_body"
    LOWER_BODY = "lower_body"
    ONE_PIECE = "one_piece"
    LAYERING = "layering"
    FOOTWEAR = "footwear"
    JEWELRY = "jewelry"
    WATCHES = "watches"
    ACCESSORIES = "accessories"
    HEADWEAR = "headwear"
    BAGS = "bags"
    SEASONAL = "seasonal"
    ETHNIC = "ethnic"


# ==================== MAIN SCHEMAS ====================

class CategorySpec(BaseModel):
    """Specific requirements for any category"""
    color: Optional[str] = None  # Using string to avoid enum validation issues
    style: Optional[str] = None
    fit: Optional[str] = None
    fabric: Optional[str] = None
    pattern: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    price_range: Optional[str] = None
    preferred_brands: List[str] = Field(default_factory=list)
    excluded_brands: List[str] = Field(default_factory=list)
    must_have: List[str] = Field(default_factory=list)
    nice_to_have: List[str] = Field(default_factory=list)
    avoid: List[str] = Field(default_factory=list)
    custom_requirements: Optional[str] = None


class UserContext(BaseModel):
    """User's personal context for personalized styling"""
    gender: str = "unisex"
    age_group: str = "adult"
    body_type: Optional[str] = None
    skin_tone: Optional[str] = None
    preferred_colors: List[str] = Field(default_factory=list)
    avoided_colors: List[str] = Field(default_factory=list)
    preferred_styles: List[str] = Field(default_factory=list)
    preferred_brands: List[str] = Field(default_factory=list)
    avoided_brands: List[str] = Field(default_factory=list)
    typical_budget: str = "mid_range"
    max_budget_per_item: Optional[int] = None
    user_id: Optional[str] = None


class UserQuery(BaseModel):
    """Complete user query with context"""
    message: str
    context: Optional[UserContext] = None
    occasion: Optional[str] = None
    season: Optional[str] = None
    budget_total: Optional[int] = None
    need_by_date: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "message": "I need an outfit for a wedding",
                "occasion": "wedding",
                "budget_total": 25000
            }
        }


class Product(BaseModel):
    """Product scraped from e-commerce site"""
    product_id: str
    brand: str
    product_name: str
    price: int
    original_price: Optional[int] = 0
    discount: Optional[str] = ""
    image_url: str
    additional_images: List[str] = Field(default_factory=list)
    product_url: str
    source: str
    category: str
    category_type: Optional[str] = None
    color: Optional[str] = None
    style: Optional[str] = None
    fit: Optional[str] = None
    fabric: Optional[str] = None
    pattern: Optional[str] = None
    in_stock: bool = True
    sizes_available: List[str] = Field(default_factory=list)
    scraped_at: int
    match_score: float = 0.0
    match_reasons: List[str] = Field(default_factory=list)


class ScrapingTask(BaseModel):
    """Task for a scraping agent"""
    category: str
    category_type: str = "default"  # Add default value
    search_query: str
    max_results: int = 10
    priority: int = 1
    spec: Optional[CategorySpec] = None
    depends_on: List[str] = Field(default_factory=list)


class StylistResponse(BaseModel):
    """Complete response from AI stylist"""
    user_query: str
    user_context: Optional[UserContext] = None
    outfit_spec: Dict[str, Any]
    products: Dict[str, List[Product]]
    total_outfit_price: int
    budget_status: str
    styling_advice: str
    color_advice: str
    fit_advice: Optional[str] = None
    layering_advice: Optional[str] = None
    missing_categories: List[str] = Field(default_factory=list)
    alternative_suggestions: Dict[str, List[Product]] = Field(default_factory=dict)
    processing_time: float
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
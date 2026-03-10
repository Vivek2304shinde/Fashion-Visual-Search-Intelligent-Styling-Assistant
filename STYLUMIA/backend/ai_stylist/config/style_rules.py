"""
Style combination rules based on fashion expertise and style compatibility.
This drives the validator agent's decisions for style coordination.
"""

from typing import Dict, List, Tuple, Optional, Set, Any
from ai_stylist.schemas import Style, Occasion, Fit, AgeGroup, Gender

# Style compatibility matrix
STYLE_COMPATIBILITY = {
    # Formal with other styles
    Style.FORMAL: {
        "compatible": [Style.FORMAL, Style.BUSINESS, Style.MINIMALIST, Style.BLACK_TIE, Style.WHITE_TIE],
        "incompatible": [Style.STREETWEAR, Style.ROCK, Style.BOHEMIAN, Style.PUNK, Style.GRUNGE],
        "fusion_possible": [Style.CASUAL, Style.PREPPY, Style.SMART_CASUAL, Style.CONTEMPORARY],
        "notes": "Formal works best with clean, structured styles"
    },
    
    # Business with other styles
    Style.BUSINESS: {
        "compatible": [Style.FORMAL, Style.BUSINESS, Style.MINIMALIST, Style.PREPPY, Style.SMART_CASUAL],
        "incompatible": [Style.STREETWEAR, Style.ROCK, Style.BOHEMIAN, Style.PUNK],
        "fusion_possible": [Style.CASUAL, Style.CONTEMPORARY],
        "notes": "Business attire can be softened with smart casual elements"
    },
    
    # Casual with other styles
    Style.CASUAL: {
        "compatible": [Style.CASUAL, Style.STREETWEAR, Style.ATHLEISURE, Style.BOHEMIAN, 
                      Style.PREPPY, Style.SPORTY, Style.VINTAGE, Style.RETRO],
        "incompatible": [Style.FORMAL, Style.BLACK_TIE, Style.WHITE_TIE],
        "fusion_possible": [Style.SMART_CASUAL, Style.MINIMALIST, Style.CONTEMPORARY],
        "notes": "Casual is versatile but avoid over-formalizing"
    },
    
    # Streetwear with other styles
    Style.STREETWEAR: {
        "compatible": [Style.STREETWEAR, Style.CASUAL, Style.ATHLEISURE, Style.ROCK, 
                      Style.URBAN, Style.GRUNGE],
        "incompatible": [Style.FORMAL, Style.BUSINESS, Style.MINIMALIST, Style.BLACK_TIE],
        "fusion_possible": [Style.PREPPY, Style.LUXURY, Style.CONTEMPORARY],
        "notes": "Streetwear can be elevated with luxury elements"
    },
    
    # Traditional with other styles
    Style.TRADITIONAL: {
        "compatible": [Style.TRADITIONAL, Style.ETHNIC, Style.FORMAL, Style.CASUAL, 
                      Style.FESTIVE, Style.WEDDING],
        "incompatible": [Style.STREETWEAR, Style.ROCK, Style.PUNK, Style.GRUNGE],
        "fusion_possible": [Style.CONTEMPORARY, Style.MINIMALIST, Style.BOHEMIAN, Style.INDO_WESTERN],
        "notes": "Traditional can be modernized with contemporary pieces"
    },
    
    # Ethnic with other styles
    Style.ETHNIC: {
        "compatible": [Style.ETHNIC, Style.TRADITIONAL, Style.FESTIVE, Style.WEDDING],
        "incompatible": [Style.STREETWEAR, Style.ROCK, Style.ATHLEISURE],
        "fusion_possible": [Style.CONTEMPORARY, Style.INDO_WESTERN, Style.BOHEMIAN],
        "notes": "Ethnic wear can be styled with contemporary accessories"
    },
    
    # Minimalist with other styles
    Style.MINIMALIST: {
        "compatible": [Style.MINIMALIST, Style.FORMAL, Style.BUSINESS, Style.CASUAL, 
                      Style.CONTEMPORARY, Style.SMART_CASUAL],
        "incompatible": [Style.BOHEMIAN, Style.ROCK, Style.STREETWEAR, Style.PUNK, 
                        Style.GRUNGE, Style.FESTIVE],
        "fusion_possible": [Style.PREPPY, Style.CLASSIC],
        "notes": "Minimalism pairs well with clean, simple aesthetics"
    },
    
    # Contemporary with other styles
    Style.CONTEMPORARY: {
        "compatible": [Style.CONTEMPORARY, Style.MINIMALIST, Style.CASUAL, Style.SMART_CASUAL,
                      Style.PREPPY, Style.CLASSIC],
        "incompatible": [Style.TRADITIONAL, Style.ROCK, Style.PUNK],
        "fusion_possible": [Style.BOHEMIAN, Style.STREETWEAR, Style.INDO_WESTERN],
        "notes": "Contemporary works with most modern styles"
    },
    
    # Bohemian with other styles
    Style.BOHEMIAN: {
        "compatible": [Style.BOHEMIAN, Style.BOHO, Style.CASUAL, Style.TRADITIONAL, 
                      Style.VINTAGE, Style.RETRO],
        "incompatible": [Style.FORMAL, Style.BUSINESS, Style.MINIMALIST, Style.BLACK_TIE],
        "fusion_possible": [Style.CONTEMPORARY, Style.STREETWEAR, Style.INDO_WESTERN],
        "notes": "Boho can be grounded with contemporary elements"
    },
    
    # Boho with other styles
    Style.BOHO: {
        "compatible": [Style.BOHO, Style.BOHEMIAN, Style.CASUAL, Style.VINTAGE],
        "incompatible": [Style.FORMAL, Style.BUSINESS, Style.MINIMALIST],
        "fusion_possible": [Style.CONTEMPORARY, Style.STREETWEAR],
        "notes": "Similar to bohemian but more casual"
    },
    
    # Rock with other styles
    Style.ROCK: {
        "compatible": [Style.ROCK, Style.PUNK, Style.GRUNGE, Style.STREETWEAR, Style.CASUAL],
        "incompatible": [Style.FORMAL, Style.BUSINESS, Style.PREPPY, Style.MINIMALIST,
                        Style.TRADITIONAL, Style.CLASSIC],
        "fusion_possible": [Style.LUXURY, Style.CONTEMPORARY, Style.ATHLEISURE],
        "notes": "Rock elements can add edge to luxury pieces"
    },
    
    # Punk with other styles
    Style.PUNK: {
        "compatible": [Style.PUNK, Style.ROCK, Style.GRUNGE, Style.STREETWEAR],
        "incompatible": [Style.FORMAL, Style.BUSINESS, Style.PREPPY, Style.MINIMALIST,
                        Style.TRADITIONAL, Style.CLASSIC],
        "fusion_possible": [Style.CONTEMPORARY, Style.LUXURY],
        "notes": "Punk is very specific and hard to mix"
    },
    
    # Grunge with other styles
    Style.GRUNGE: {
        "compatible": [Style.GRUNGE, Style.ROCK, Style.PUNK, Style.STREETWEAR, Style.CASUAL],
        "incompatible": [Style.FORMAL, Style.BUSINESS, Style.PREPPY, Style.MINIMALIST],
        "fusion_possible": [Style.CONTEMPORARY, Style.VINTAGE],
        "notes": "Grunge works with casual and vintage pieces"
    },
    
    # Preppy with other styles
    Style.PREPPY: {
        "compatible": [Style.PREPPY, Style.CASUAL, Style.BUSINESS, Style.SMART_CASUAL,
                      Style.CLASSIC, Style.IVY_LEAGUE],
        "incompatible": [Style.ROCK, Style.STREETWEAR, Style.PUNK, Style.GRUNGE],
        "fusion_possible": [Style.CONTEMPORARY, Style.MINIMALIST, Style.SPORTY],
        "notes": "Preppy can be updated with contemporary cuts"
    },
    
    # Classic with other styles
    Style.CLASSIC: {
        "compatible": [Style.CLASSIC, Style.FORMAL, Style.BUSINESS, Style.PREPPY,
                      Style.MINIMALIST, Style.SMART_CASUAL],
        "incompatible": [Style.STREETWEAR, Style.ROCK, Style.PUNK, Style.GRUNGE],
        "fusion_possible": [Style.CONTEMPORARY, Style.VINTAGE],
        "notes": "Classic is timeless and works with most refined styles"
    },
    
    # Vintage with other styles
    Style.VINTAGE: {
        "compatible": [Style.VINTAGE, Style.RETRO, Style.CASUAL, Style.BOHEMIAN,
                      Style.CLASSIC, Style.ROCK],
        "incompatible": [Style.STREETWEAR, Style.ATHLEISURE, Style.MINIMALIST],
        "fusion_possible": [Style.CONTEMPORARY, Style.INDO_WESTERN],
        "notes": "Vintage can be mixed with contemporary pieces"
    },
    
    # Retro with other styles
    Style.RETRO: {
        "compatible": [Style.RETRO, Style.VINTAGE, Style.CASUAL, Style.BOHEMIAN,
                      Style.ROCK, Style.PREPPY],
        "incompatible": [Style.MINIMALIST, Style.FORMAL, Style.BUSINESS],
        "fusion_possible": [Style.CONTEMPORARY, Style.STREETWEAR],
        "notes": "Retro patterns work with modern silhouettes"
    },
    
    # Athleisure with other styles
    Style.ATHLEISURE: {
        "compatible": [Style.ATHLEISURE, Style.CASUAL, Style.STREETWEAR, Style.SPORTY],
        "incompatible": [Style.FORMAL, Style.BUSINESS, Style.TRADITIONAL, Style.BLACK_TIE],
        "fusion_possible": [Style.LUXURY, Style.CONTEMPORARY, Style.MINIMALIST],
        "notes": "Athleisure works best with relaxed styles"
    },
    
    # Sporty with other styles
    Style.SPORTY: {
        "compatible": [Style.SPORTY, Style.ATHLEISURE, Style.CASUAL, Style.STREETWEAR],
        "incompatible": [Style.FORMAL, Style.BUSINESS, Style.TRADITIONAL],
        "fusion_possible": [Style.CONTEMPORARY, Style.PREPPY],
        "notes": "Sporty elements can add energy to casual looks"
    },
    
    # Smart Casual with other styles
    Style.SMART_CASUAL: {
        "compatible": [Style.SMART_CASUAL, Style.BUSINESS, Style.CASUAL, Style.PREPPY, 
                      Style.MINIMALIST, Style.CONTEMPORARY, Style.CLASSIC],
        "incompatible": [Style.ROCK, Style.STREETWEAR, Style.PUNK, Style.GRUNGE],
        "fusion_possible": [Style.FORMAL, Style.INDO_WESTERN, Style.VINTAGE],
        "notes": "Smart casual bridges formal and casual perfectly"
    },
    
    # Indo-Western with other styles
    Style.INDO_WESTERN: {
        "compatible": [Style.INDO_WESTERN, Style.CONTEMPORARY, Style.TRADITIONAL, 
                      Style.ETHNIC, Style.FUSION, Style.CASUAL],
        "incompatible": [Style.ROCK, Style.PUNK, Style.STREETWEAR],
        "fusion_possible": [Style.FORMAL, Style.MINIMALIST, Style.BOHEMIAN],
        "notes": "Indo-Western is inherently fusion-friendly"
    },
    
    # Fusion with other styles
    Style.FUSION: {
        "compatible": [Style.FUSION, Style.CONTEMPORARY, Style.INDO_WESTERN, 
                      Style.BOHEMIAN, Style.TRADITIONAL],
        "incompatible": [Style.PUNK, Style.ROCK, Style.STREETWEAR],
        "fusion_possible": [Style.CASUAL, Style.FORMAL],
        "notes": "Fusion is designed to mix different elements"
    },
    
    # Wedding with other styles
    Style.WEDDING: {
        "compatible": [Style.WEDDING, Style.FORMAL, Style.TRADITIONAL, Style.ETHNIC,
                      Style.LUXURY, Style.ROMANTIC],
        "incompatible": [Style.CASUAL, Style.STREETWEAR, Style.ATHLEISURE, Style.SPORTY],
        "fusion_possible": [Style.CONTEMPORARY, Style.INDO_WESTERN],
        "notes": "Wedding attire should be celebratory and elevated"
    },
    
    # Party with other styles
    Style.PARTY: {
        "compatible": [Style.PARTY, Style.CLUB, Style.COCKTAIL, Style.CONTEMPORARY,
                      Style.ROCK, Style.FESTIVE],
        "incompatible": [Style.BUSINESS, Style.MINIMALIST, Style.CASUAL],
        "fusion_possible": [Style.LUXURY, Style.STREETWEAR],
        "notes": "Party styles can be bold and expressive"
    },
    
    # Club with other styles
    Style.CLUB: {
        "compatible": [Style.CLUB, Style.PARTY, Style.ROCK, Style.STREETWEAR,
                      Style.CONTEMPORARY],
        "incompatible": [Style.BUSINESS, Style.FORMAL, Style.TRADITIONAL],
        "fusion_possible": [Style.LUXURY, Style.MINIMALIST],
        "notes": "Club wear is edgy and bold"
    },
    
    # Cocktail with other styles
    Style.COCKTAIL: {
        "compatible": [Style.COCKTAIL, Style.PARTY, Style.FORMAL, Style.LUXURY,
                      Style.CONTEMPORARY, Style.ROMANTIC],
        "incompatible": [Style.CASUAL, Style.ATHLEISURE, Style.STREETWEAR],
        "fusion_possible": [Style.VINTAGE, Style.INDO_WESTERN],
        "notes": "Cocktail attire is dressy but not too formal"
    },
    
    # Black Tie with other styles
    Style.BLACK_TIE: {
        "compatible": [Style.BLACK_TIE, Style.FORMAL, Style.WHITE_TIE, Style.LUXURY],
        "incompatible": [Style.CASUAL, Style.STREETWEAR, Style.BOHEMIAN, Style.ROCK,
                        Style.ATHLEISURE, Style.PREPPY],
        "fusion_possible": [Style.CONTEMPORARY, Style.MINIMALIST],
        "notes": "Black tie has strict rules, avoid mixing casually"
    },
    
    # White Tie with other styles
    Style.WHITE_TIE: {
        "compatible": [Style.WHITE_TIE, Style.FORMAL, Style.BLACK_TIE, Style.LUXURY],
        "incompatible": [Style.CASUAL, Style.STREETWEAR, Style.BOHEMIAN, Style.ROCK,
                        Style.ATHLEISURE, Style.PREPPY, Style.CONTEMPORARY],
        "fusion_possible": [],
        "notes": "White tie is the most formal - stick to strict rules"
    },
    
    # Luxury with other styles
    Style.LUXURY: {
        "compatible": [Style.LUXURY, Style.FORMAL, Style.BLACK_TIE, Style.WHITE_TIE,
                      Style.COCKTAIL, Style.PARTY, Style.CONTEMPORARY],
        "incompatible": [Style.CASUAL, Style.STREETWEAR, Style.BOHEMIAN],
        "fusion_possible": [Style.ROCK, Style.ATHLEISURE, Style.MINIMALIST],
        "notes": "Luxury can elevate edgy styles"
    },
    
    # Romantic with other styles
    Style.ROMANTIC: {
        "compatible": [Style.ROMANTIC, Style.FORMAL, Style.COCKTAIL, Style.WEDDING,
                      Style.VINTAGE, Style.PARTY],
        "incompatible": [Style.STREETWEAR, Style.ROCK, Style.PUNK, Style.GRUNGE],
        "fusion_possible": [Style.CONTEMPORARY, Style.BOHEMIAN],
        "notes": "Romantic styles are feminine and soft"
    },
    
    # Festive with other styles
    Style.FESTIVE: {
        "compatible": [Style.FESTIVE, Style.PARTY, Style.TRADITIONAL, Style.ETHNIC,
                      Style.WEDDING, Style.CONTEMPORARY],
        "incompatible": [Style.MINIMALIST, Style.BUSINESS, Style.ATHLEISURE],
        "fusion_possible": [Style.INDO_WESTERN, Style.BOHEMIAN],
        "notes": "Festive styles are vibrant and celebratory"
    }
}

# Occasion-appropriate style mappings
OCCASION_STYLES = {
    Occasion.WEDDING: {
        "primary": [Style.WEDDING, Style.FORMAL, Style.TRADITIONAL, Style.ETHNIC, 
                   Style.LUXURY, Style.ROMANTIC],
        "acceptable": [Style.SMART_CASUAL, Style.CONTEMPORARY, Style.INDO_WESTERN, 
                      Style.FESTIVE, Style.COCKTAIL],
        "avoid": [Style.STREETWEAR, Style.ROCK, Style.ATHLEISURE, Style.CASUAL,
                  Style.PUNK, Style.GRUNGE],
        "notes": "Weddings call for elevated, celebratory attire"
    },
    Occasion.RECEPTION: {
        "primary": [Style.FORMAL, Style.COCKTAIL, Style.LUXURY, Style.PARTY,
                   Style.BLACK_TIE, Style.CONTEMPORARY],
        "acceptable": [Style.SMART_CASUAL, Style.INDO_WESTERN, Style.FESTIVE],
        "avoid": [Style.CASUAL, Style.STREETWEAR, Style.ATHLEISURE, Style.SPORTY],
        "notes": "Evening events require dressier styles"
    },
    Occasion.ENGAGEMENT: {
        "primary": [Style.SMART_CASUAL, Style.CONTEMPORARY, Style.ROMANTIC, 
                   Style.COCKTAIL, Style.PARTY],
        "acceptable": [Style.CASUAL, Style.PREPPY, Style.VINTAGE, Style.INDO_WESTERN],
        "avoid": [Style.FORMAL, Style.BLACK_TIE, Style.STREETWEAR, Style.ROCK],
        "notes": "Engagements balance celebration with intimacy"
    },
    Occasion.MEHENDI: {
        "primary": [Style.TRADITIONAL, Style.ETHNIC, Style.FESTIVE, Style.CASUAL,
                   Style.BOHEMIAN, Style.CONTEMPORARY],
        "acceptable": [Style.INDO_WESTERN, Style.PARTY],
        "avoid": [Style.FORMAL, Style.MINIMALIST, Style.BUSINESS, Style.BLACK_TIE],
        "notes": "Vibrant, festive styles for this celebration"
    },
    Occasion.SANGEET: {
        "primary": [Style.FESTIVE, Style.PARTY, Style.CONTEMPORARY, Style.TRADITIONAL,
                   Style.BOHEMIAN, Style.INDO_WESTERN],
        "acceptable": [Style.CASUAL, Style.ROCK, Style.STREETWEAR],
        "avoid": [Style.MINIMALIST, Style.BUSINESS, Style.FORMAL],
        "notes": "Dance events call for movement-friendly styles"
    },
    Occasion.HALDI: {
        "primary": [Style.CASUAL, Style.TRADITIONAL, Style.FESTIVE, Style.BOHEMIAN],
        "acceptable": [Style.CONTEMPORARY, Style.INDO_WESTERN],
        "avoid": [Style.FORMAL, Style.BLACK_TIE, Style.MINIMALIST],
        "notes": "Yellow/colorful, casual festive wear"
    },
    Occasion.PARTY: {
        "primary": [Style.PARTY, Style.CLUB, Style.COCKTAIL, Style.CONTEMPORARY, 
                   Style.ROCK, Style.STREETWEAR, Style.LUXURY],
        "acceptable": [Style.CASUAL, Style.FESTIVE, Style.VINTAGE, Style.RETRO],
        "avoid": [Style.BUSINESS, Style.MINIMALIST, Style.TRADITIONAL, Style.FORMAL],
        "notes": "Parties are for expressive, bold styles"
    },
    Occasion.CLUB: {
        "primary": [Style.CLUB, Style.PARTY, Style.ROCK, Style.STREETWEAR,
                   Style.CONTEMPORARY, Style.PUNK],
        "acceptable": [Style.CASUAL, Style.ATHLEISURE, Style.GRUNGE],
        "avoid": [Style.BUSINESS, Style.FORMAL, Style.TRADITIONAL, Style.PREPPY],
        "notes": "Club wear is edgy and bold"
    },
    Occasion.OFFICE: {
        "primary": [Style.BUSINESS, Style.FORMAL, Style.SMART_CASUAL, Style.MINIMALIST,
                   Style.PREPPY, Style.CLASSIC],
        "acceptable": [Style.CONTEMPORARY, Style.CASUAL, Style.INDO_WESTERN],
        "avoid": [Style.STREETWEAR, Style.ROCK, Style.BOHEMIAN, Style.PARTY,
                  Style.PUNK, Style.GRUNGE, Style.ATHLEISURE],
        "notes": "Professional environments require polished styles"
    },
    Occasion.BUSINESS_MEETING: {
        "primary": [Style.BUSINESS, Style.FORMAL, Style.MINIMALIST, Style.SMART_CASUAL],
        "acceptable": [Style.PREPPY, Style.CLASSIC, Style.CONTEMPORARY],
        "avoid": [Style.CASUAL, Style.STREETWEAR, Style.ROCK, Style.BOHEMIAN],
        "notes": "Keep it professional and conservative"
    },
    Occasion.INTERVIEW: {
        "primary": [Style.BUSINESS, Style.FORMAL, Style.MINIMALIST, Style.CLASSIC],
        "acceptable": [Style.SMART_CASUAL, Style.PREPPY],
        "avoid": [Style.CASUAL, Style.STREETWEAR, Style.ROCK, Style.BOHEMIAN,
                  Style.ATHLEISURE, Style.PARTY],
        "notes": "First impressions matter - conservative and professional"
    },
    Occasion.CASUAL: {
        "primary": [Style.CASUAL, Style.STREETWEAR, Style.ATHLEISURE, Style.SPORTY,
                   Style.BOHEMIAN, Style.VINTAGE, Style.RETRO],
        "acceptable": [Style.SMART_CASUAL, Style.PREPPY, Style.CONTEMPORARY,
                      Style.MINIMALIST, Style.GRUNGE],
        "avoid": [Style.FORMAL, Style.BUSINESS, Style.BLACK_TIE, Style.WHITE_TIE],
        "notes": "Comfort and personal expression take priority"
    },
    Occasion.DATE: {
        "primary": [Style.ROMANTIC, Style.CONTEMPORARY, Style.SMART_CASUAL, 
                   Style.COCKTAIL, Style.PARTY, Style.CLASSIC],
        "acceptable": [Style.CASUAL, Style.PREPPY, Style.VINTAGE, Style.BOHEMIAN],
        "avoid": [Style.STREETWEAR, Style.ROCK, Style.ATHLEISURE, Style.PUNK,
                  Style.GRUNGE],
        "notes": "Show personality while looking put-together"
    },
    Occasion.DINNER: {
        "primary": [Style.SMART_CASUAL, Style.CONTEMPORARY, Style.COCKTAIL,
                   Style.ROMANTIC, Style.PARTY],
        "acceptable": [Style.CASUAL, Style.FORMAL, Style.PREPPY, Style.VINTAGE],
        "avoid": [Style.STREETWEAR, Style.ATHLEISURE, Style.SPORTY],
        "notes": "Dinner dates call for stylish but comfortable looks"
    },
    Occasion.BRUNCH: {
        "primary": [Style.CASUAL, Style.SMART_CASUAL, Style.BOHEMIAN, Style.PREPPY,
                   Style.CONTEMPORARY, Style.VINTAGE],
        "acceptable": [Style.ROMANTIC, Style.ATHLEISURE, Style.STREETWEAR],
        "avoid": [Style.FORMAL, Style.BUSINESS, Style.BLACK_TIE],
        "notes": "Brunch is casual-chic and daytime appropriate"
    },
    Occasion.BEACH: {
        "primary": [Style.CASUAL, Style.BOHEMIAN, Style.RESORT, Style.SPORTY,
                   Style.ATHLEISURE, Style.CONTEMPORARY],
        "acceptable": [Style.VINTAGE, Style.RETRO, Style.MINIMALIST],
        "avoid": [Style.FORMAL, Style.BUSINESS, Style.BLACK_TIE, Style.WEDDING],
        "notes": "Relaxed, breathable styles for beach settings"
    },
    Occasion.VACATION: {
        "primary": [Style.CASUAL, Style.RESORT, Style.BOHEMIAN, Style.ATHLEISURE,
                   Style.VINTAGE, Style.CONTEMPORARY],
        "acceptable": [Style.SMART_CASUAL, Style.ROMANTIC, Style.STREETWEAR],
        "avoid": [Style.FORMAL, Style.BUSINESS, Style.BLACK_TIE],
        "notes": "Vacation style should be comfortable and versatile"
    },
    Occasion.FESTIVAL: {
        "primary": [Style.FESTIVE, Style.BOHEMIAN, Style.STREETWEAR,
                   Style.CONTEMPORARY, Style.PARTY, Style.ROCK],
        "acceptable": [Style.CASUAL, Style.VINTAGE, Style.RETRO, Style.GRUNGE],
        "avoid": [Style.FORMAL, Style.BUSINESS, Style.MINIMALIST, Style.PREPPY],
        "notes": "Express yourself with bold, artistic styles"
    },
    Occasion.CONCERT: {
        "primary": [Style.ROCK, Style.PUNK, Style.GRUNGE, Style.STREETWEAR,
                   Style.CASUAL, Style.PARTY],
        "acceptable": [Style.CONTEMPORARY, Style.VINTAGE, Style.ATHLEISURE],
        "avoid": [Style.FORMAL, Style.BUSINESS, Style.PREPPY, Style.CLASSIC],
        "notes": "Concert style should match the music genre"
    },
    Occasion.SPORTS_EVENT: {
        "primary": [Style.SPORTY, Style.CASUAL, Style.ATHLEISURE, Style.STREETWEAR],
        "acceptable": [Style.CONTEMPORARY, Style.PREPPY],
        "avoid": [Style.FORMAL, Style.BUSINESS, Style.BLACK_TIE],
        "notes": "Comfortable, team-spirit appropriate"
    },
    Occasion.POOJA: {
        "primary": [Style.TRADITIONAL, Style.ETHNIC, Style.CASUAL, Style.MINIMALIST],
        "acceptable": [Style.CONTEMPORARY, Style.INDO_WESTERN],
        "avoid": [Style.STREETWEAR, Style.ROCK, Style.PARTY],
        "notes": "Respectful, modest attire for religious occasions"
    },
    Occasion.TEMPLE_VISIT: {
        "primary": [Style.TRADITIONAL, Style.ETHNIC, Style.CASUAL, Style.MINIMALIST],
        "acceptable": [Style.CONTEMPORARY],
        "avoid": [Style.STREETWEAR, Style.ROCK, Style.ATHLEISURE, Style.PARTY],
        "notes": "Conservative, respectful dressing"
    },
    Occasion.DIWALI: {
        "primary": [Style.TRADITIONAL, Style.ETHNIC, Style.FESTIVE, Style.PARTY,
                   Style.CONTEMPORARY, Style.INDO_WESTERN],
        "acceptable": [Style.CASUAL, Style.BOHEMIAN],
        "avoid": [Style.MINIMALIST, Style.BUSINESS, Style.ATHLEISURE],
        "notes": "Festival of lights calls for bright, celebratory wear"
    },
    Occasion.HOLI: {
        "primary": [Style.CASUAL, Style.STREETWEAR, Style.ATHLEISURE, Style.BOHEMIAN],
        "acceptable": [Style.CONTEMPORARY, Style.FESTIVE],
        "avoid": [Style.FORMAL, Style.BUSINESS, Style.PREPPY],
        "notes": "Wear clothes you don't mind getting color on"
    }
}

# Age-appropriate style guidelines
AGE_STYLE_GUIDELINES = {
    AgeGroup.TEEN: {
        "recommended": [Style.CASUAL, Style.STREETWEAR, Style.ATHLEISURE, 
                       Style.SPORTY, Style.GRUNGE, Style.ROCK, Style.CONTEMPORARY],
        "avoid": [Style.FORMAL, Style.BUSINESS, Style.CLASSIC, Style.MINIMALIST],
        "notes": "Trendy, expressive, age-appropriate"
    },
    AgeGroup.YOUNG_ADULT: {
        "recommended": [Style.CONTEMPORARY, Style.CASUAL, Style.SMART_CASUAL, 
                       Style.STREETWEAR, Style.ATHLEISURE, Style.ROCK, Style.PARTY],
        "avoid": [Style.TRADITIONAL],
        "notes": "Experiment while building professional wardrobe"
    },
    AgeGroup.ADULT: {
        "recommended": [Style.SMART_CASUAL, Style.BUSINESS, Style.CONTEMPORARY,
                       Style.MINIMALIST, Style.CLASSIC, Style.PREPPY],
        "avoid": [Style.STREETWEAR, Style.GRUNGE],
        "notes": "Quality pieces, polished casual"
    },
    AgeGroup.MATURE: {
        "recommended": [Style.BUSINESS, Style.CLASSIC, Style.MINIMALIST, 
                       Style.SMART_CASUAL, Style.ELEGANT, Style.FORMAL],
        "avoid": [Style.STREETWEAR, Style.ROCK, Style.PUNK],
        "notes": "Sophisticated, timeless elegance"
    },
    AgeGroup.KIDS: {
        "recommended": [Style.CASUAL, Style.SPORTY, Style.ATHLEISURE],
        "avoid": [Style.FORMAL, Style.BUSINESS],
        "notes": "Comfortable, play-friendly clothes"
    }
}

# Gender-based style recommendations
GENDER_STYLE_RECOMMENDATIONS = {
    Gender.MALE: {
        "general": [Style.FORMAL, Style.BUSINESS, Style.CASUAL, Style.STREETWEAR,
                   Style.ATHLEISURE, Style.ROCK, Style.PREPPY, Style.CLASSIC],
        "notes": "Most styles work for men with appropriate cuts"
    },
    Gender.FEMALE: {
        "general": [Style.FORMAL, Style.BUSINESS, Style.CASUAL, Style.STREETWEAR,
                   Style.ATHLEISURE, Style.ROMANTIC, Style.BOHEMIAN, Style.PREPPY,
                   Style.CLASSIC, Style.CONTEMPORARY],
        "notes": "Women have the widest range of style options"
    },
    Gender.UNISEX: {
        "general": [Style.CASUAL, Style.STREETWEAR, Style.ATHLEISURE, Style.MINIMALIST,
                   Style.CONTEMPORARY, Style.SPORTY, Style.CLASSIC],
        "notes": "Unisex styles tend to be more casual and minimalist"
    }
}

# Style-specific color rules (simplified - main rules in color_rules.py)
STYLE_COLOR_RULES = {
    Style.FORMAL: {
        "max_colors": 3,
        "prefer_patterns": False,
        "pattern_types": ["solid", "pinstripe", "subtle"],
        "rules": "Conservative color palette, minimal contrast",
    },
    Style.BUSINESS: {
        "max_colors": 4,
        "prefer_patterns": True,
        "pattern_types": ["solid", "stripe", "subtle_check"],
        "rules": "Professional colors, modest patterns",
    },
    Style.CASUAL: {
        "max_colors": 6,
        "prefer_patterns": True,
        "pattern_types": ["all"],
        "rules": "Personal expression, no strict rules",
    },
    Style.STREETWEAR: {
        "max_colors": 8,
        "prefer_patterns": True,
        "pattern_types": ["bold", "graphic", "camo"],
        "rules": "High contrast, bold color blocking",
    },
    Style.TRADITIONAL: {
        "max_colors": 5,
        "prefer_patterns": True,
        "pattern_types": ["ethnic", "embroidery", "print"],
        "rules": "Rich colors, traditional motifs",
    },
    Style.ETHNIC: {
        "max_colors": 5,
        "prefer_patterns": True,
        "pattern_types": ["ethnic", "embroidery", "print"],
        "rules": "Vibrant colors, traditional patterns",
    },
    Style.MINIMALIST: {
        "max_colors": 2,
        "prefer_patterns": False,
        "pattern_types": ["solid"],
        "rules": "Monochromatic or one accent color",
    },
    Style.BOHEMIAN: {
        "max_colors": 7,
        "prefer_patterns": True,
        "pattern_types": ["floral", "ethnic", "tribal", "print"],
        "rules": "Earthy tones with pops of color",
    },
    Style.ROCK: {
        "max_colors": 4,
        "prefer_patterns": True,
        "pattern_types": ["leather", "studs", "plaid", "graphic"],
        "rules": "Dark base with bold accents",
    },
    Style.PUNK: {
        "max_colors": 4,
        "prefer_patterns": True,
        "pattern_types": ["leather", "studs", "plaid", "graphic"],
        "rules": "Dark colors with aggressive accents",
    },
    Style.GRUNGE: {
        "max_colors": 5,
        "prefer_patterns": True,
        "pattern_types": ["plaid", "flannel", "distressed"],
        "rules": "Muted, earthy, lived-in look",
    },
    Style.PREPPY: {
        "max_colors": 4,
        "prefer_patterns": True,
        "pattern_types": ["stripe", "check", "solid", "plaid"],
        "rules": "Classic color combinations",
    },
    Style.CLASSIC: {
        "max_colors": 3,
        "prefer_patterns": True,
        "pattern_types": ["solid", "stripe", "subtle"],
        "rules": "Timeless, never-out-of-style combinations",
    },
    Style.VINTAGE: {
        "max_colors": 4,
        "prefer_patterns": True,
        "pattern_types": ["vintage", "retro", "floral"],
        "rules": "Colors and patterns from past eras",
    },
    Style.RETRO: {
        "max_colors": 5,
        "prefer_patterns": True,
        "pattern_types": ["retro", "geometric", "bold"],
        "rules": "Bold colors and patterns from specific decades",
    },
    Style.ATHLEISURE: {
        "max_colors": 5,
        "prefer_patterns": True,
        "pattern_types": ["color_block", "stripe", "logo", "graphic"],
        "rules": "Sporty colors, reflective elements optional",
    },
    Style.SPORTY: {
        "max_colors": 4,
        "prefer_patterns": True,
        "pattern_types": ["stripe", "color_block", "logo"],
        "rules": "Team colors, high-visibility options",
    },
    Style.SMART_CASUAL: {
        "max_colors": 4,
        "prefer_patterns": True,
        "pattern_types": ["solid", "stripe", "subtle"],
        "rules": "Balanced, put-together without being too formal",
    },
    Style.CONTEMPORARY: {
        "max_colors": 4,
        "prefer_patterns": True,
        "pattern_types": ["modern", "abstract", "solid"],
        "rules": "Current trends with personal twist",
    },
    Style.ROMANTIC: {
        "max_colors": 4,
        "prefer_patterns": True,
        "pattern_types": ["floral", "lace", "soft"],
        "rules": "Soft, feminine colors and patterns",
    },
    Style.LUXURY: {
        "max_colors": 3,
        "prefer_patterns": False,
        "pattern_types": ["solid", "subtle"],
        "rules": "Rich, expensive-looking colors",
    },
    Style.FESTIVE: {
        "max_colors": 6,
        "prefer_patterns": True,
        "pattern_types": ["all"],
        "rules": "Bright, celebratory colors",
    },
    Style.RESORT: {
        "max_colors": 5,
        "prefer_patterns": True,
        "pattern_types": ["floral", "tropical", "solid"],
        "rules": "Light, airy, vacation-appropriate colors",
    },
    Style.COCKTAIL: {
        "max_colors": 3,
        "prefer_patterns": True,
        "pattern_types": ["solid", "sequin", "subtle"],
        "rules": "Elegant, evening-appropriate colors",
    },
    Style.BLACK_TIE: {
        "max_colors": 2,
        "prefer_patterns": False,
        "pattern_types": ["solid"],
        "rules": "Very formal, limited color palette",
    },
    Style.WHITE_TIE: {
        "max_colors": 2,
        "prefer_patterns": False,
        "pattern_types": ["solid"],
        "rules": "Ultra-formal, traditional colors only",
    },
    Style.ELEGANT: {
        "max_colors": 3,
        "prefer_patterns": False,
        "pattern_types": ["solid", "subtle"],
        "rules": "Refined, sophisticated color choices",
    }
}

# Helper functions
def validate_style_combination(styles: List[Style], primary_style: Optional[Style] = None) -> Tuple[bool, str, float]:
    """
    Validate if multiple styles work together in an outfit.
    Returns: (is_valid, reason, confidence_score)
    """
    if len(styles) < 2:
        return True, "Single style is always valid", 1.0
    
    # If primary style specified, use that for main compatibility
    if primary_style:
        main_style = primary_style
    else:
        # Determine primary style (most formal or most dominant)
        style_hierarchy = [Style.WHITE_TIE, Style.BLACK_TIE, Style.FORMAL, Style.BUSINESS, 
                          Style.SMART_CASUAL, Style.PREPPY, Style.CONTEMPORARY, 
                          Style.MINIMALIST, Style.CLASSIC, Style.CASUAL, Style.BOHEMIAN, 
                          Style.ATHLEISURE, Style.STREETWEAR, Style.ROCK, Style.PUNK]
        
        for s in style_hierarchy:
            if s in styles:
                main_style = s
                break
        else:
            main_style = styles[0]
    
    # Check compatibility with main style
    if main_style in STYLE_COMPATIBILITY:
        rules = STYLE_COMPATIBILITY[main_style]
        
        for style in styles:
            if style == main_style:
                continue
            
            if style in rules.get("incompatible", []):
                return False, f"{style.value} doesn't work well with {main_style.value}", 0.3
            
            if style in rules.get("fusion_possible", []):
                return True, f"{style.value} can work with {main_style.value} with careful styling", 0.7
    
    # Check number of distinct styles
    if len(set(styles)) > 3:
        return False, "Too many distinct styles in one outfit", 0.4
    
    return True, "Styles work well together", 0.8

def validate_style_for_occasion(style: Style, occasion: Occasion) -> Tuple[bool, str, float]:
    """
    Validate if a style is appropriate for an occasion.
    """
    if occasion in OCCASION_STYLES:
        occasion_rules = OCCASION_STYLES[occasion]
        
        if style in occasion_rules.get("primary", []):
            return True, f"{style.value} is perfect for {occasion.value}", 1.0
        elif style in occasion_rules.get("acceptable", []):
            return True, f"{style.value} is acceptable for {occasion.value}", 0.8
        elif style in occasion_rules.get("avoid", []):
            return False, f"{style.value} should be avoided for {occasion.value}", 0.3
        else:
            return True, f"{style.value} can work for {occasion.value}", 0.6
    
    return True, "No specific rules for this occasion", 0.7

def suggest_styles_for_occasion(occasion: Occasion, count: int = 3) -> List[Style]:
    """
    Suggest appropriate styles for an occasion.
    """
    if occasion in OCCASION_STYLES:
        return OCCASION_STYLES[occasion].get("primary", [Style.CASUAL])[:count]
    return [Style.CASUAL]  # Default fallback

def suggest_styles_for_age(age_group: AgeGroup, count: int = 3) -> List[Style]:
    """
    Suggest styles based on age group.
    """
    if age_group in AGE_STYLE_GUIDELINES:
        return AGE_STYLE_GUIDELINES[age_group].get("recommended", [Style.CASUAL])[:count]
    return [Style.CASUAL]

def get_style_compatibility_score(style1: Style, style2: Style) -> float:
    """
    Get compatibility score between two styles (0-1).
    """
    if style1 == style2:
        return 1.0
    
    # Check compatibility matrix
    if style1 in STYLE_COMPATIBILITY:
        rules = STYLE_COMPATIBILITY[style1]
        if style2 in rules.get("compatible", []):
            return 0.9
        elif style2 in rules.get("fusion_possible", []):
            return 0.7
        elif style2 in rules.get("incompatible", []):
            return 0.3
    
    # Default moderate compatibility
    return 0.5

def get_style_color_limits(style: Style) -> Dict:
    """
    Get color-related limits and rules for a style.
    """
    if style in STYLE_COLOR_RULES:
        return STYLE_COLOR_RULES[style]
    
    return {
        "max_colors": 5,
        "prefer_patterns": True,
        "pattern_types": ["all"],
        "rules": "No specific rules",
    }

def get_style_description(style: Style) -> str:
    """
    Get a detailed description of a style.
    """
    descriptions = {
        Style.FORMAL: "Structured, tailored clothing for formal occasions. Includes suits, gowns, and dress shoes.",
        Style.BUSINESS: "Professional attire for workplace. Blazers, trousers, blouses, and modest hemlines.",
        Style.CASUAL: "Comfortable, everyday clothing. Jeans, t-shirts, sneakers, and relaxed fits.",
        Style.STREETWEAR: "Urban, trendy fashion inspired by street culture. Hoodies, sneakers, and bold graphics.",
        Style.URBAN: "City-inspired fashion with modern, edgy elements.",
        Style.TRADITIONAL: "Cultural and ethnic clothing reflecting heritage. Sarees, kurtas, and lehengas.",
        Style.ETHNIC: "Traditional cultural attire from various regions.",
        Style.MINIMALIST: "Clean, simple aesthetics with neutral colors and no embellishments.",
        Style.CONTEMPORARY: "Modern, current fashion that's trendy but not extreme.",
        Style.BOHEMIAN: "Free-spirited, artistic style with flowy fabrics, prints, and natural elements.",
        Style.BOHO: "Casual, free-spirited style similar to bohemian but more relaxed.",
        Style.ROCK: "Edgy, rebellious aesthetic with leather, studs, and dark colors.",
        Style.PUNK: "Rebellious style with leather, spikes, and anti-establishment themes.",
        Style.GRUNGE: "Gritty, laid-back style from the 90s with flannel and distressed pieces.",
        Style.PREPPY: "Classic, collegiate-inspired style with polo shirts, chinos, and clean lines.",
        Style.CLASSIC: "Timeless, never-out-of-style pieces that form a wardrobe foundation.",
        Style.VINTAGE: "Clothing from past eras (20+ years old) or vintage-inspired pieces.",
        Style.RETRO: "Modern clothing inspired by styles from the 50s-80s.",
        Style.ATHLEISURE: "Sporty, comfortable clothing that works for both workouts and casual wear.",
        Style.SPORTY: "Athletic-inspired clothing for active lifestyles.",
        Style.SMART_CASUAL: "Polished yet relaxed style bridging formal and casual. Blazers with jeans.",
        Style.INDO_WESTERN: "Fusion of Indian traditional and Western contemporary styles.",
        Style.FUSION: "Creative mixing of different cultural and style elements.",
        Style.ROMANTIC: "Feminine, soft style with lace, ruffles, and delicate details.",
        Style.LUXURY: "High-end, designer pieces with premium fabrics and craftsmanship.",
        Style.FESTIVE: "Celebratory, vibrant clothing for special occasions and festivals.",
        Style.WEDDING: "Special occasion wear for weddings, either as guest or wedding party.",
        Style.PARTY: "Bold, celebratory clothing for social events and parties.",
        Style.CLUB: "Edgy, trendy clothing for nightclubs and late-night venues.",
        Style.COCKTAIL: "Semi-formal attire for cocktail parties and evening events.",
        Style.BLACK_TIE: "Formal evening wear requiring tuxedos or evening gowns.",
        Style.WHITE_TIE: "The most formal dress code, requiring tailcoats and full-length gowns.",
        Style.ELEGANT: "Sophisticated, refined style with graceful silhouettes.",
        Style.RESORT: "Vacation-ready style with light fabrics and relaxed silhouettes.",
    }
    
    return descriptions.get(style, f"{style.value} style")

def get_style_warning_level(styles: List[Style], occasion: Occasion) -> Dict:
    """
    Get warning level and suggestions for style combinations.
    """
    if not styles:
        return {
            "level": "info",
            "message": "No styles specified",
            "suggestions": [f"Consider {suggest_styles_for_occasion(occasion)[0].value} for this occasion"]
        }
    
    is_valid, reason, confidence = validate_style_combination(styles)
    occasion_valid, occasion_reason, occasion_confidence = validate_style_for_occasion(styles[0] if styles else Style.CASUAL, occasion)
    
    overall_confidence = min(confidence, occasion_confidence)
    
    if overall_confidence >= 0.8:
        return {
            "level": "safe",
            "message": "Great style choice!",
            "suggestions": ["Your style works well for this occasion"]
        }
    elif overall_confidence >= 0.5:
        suggestions = []
        if not occasion_valid:
            suggested = suggest_styles_for_occasion(occasion)
            if suggested:
                suggestions.append(f"Consider a more {suggested[0].value} style for this occasion")
        return {
            "level": "caution",
            "message": reason if not is_valid else occasion_reason,
            "suggestions": suggestions
        }
    else:
        suggested_styles = suggest_styles_for_occasion(occasion)
        style_names = [s.value for s in suggested_styles]
        return {
            "level": "warning",
            "message": reason if not is_valid else occasion_reason,
            "suggestions": [
                f"Try these styles instead: {', '.join(style_names)}"
            ]
        }

# Add this function to your existing style_rules.py

def get_styles_for_occasion(occasion):
    """
    Get recommended styles for a given occasion.
    """
    # Map occasions to recommended styles
    occasion_style_map = {
        Occasion.WEDDING: [Style.FORMAL, Style.TRADITIONAL, Style.ETHNIC, Style.WEDDING],
        Occasion.RECEPTION: [Style.FORMAL, Style.COCKTAIL, Style.PARTY],
        Occasion.ENGAGEMENT: [Style.SMART_CASUAL, Style.CONTEMPORARY, Style.ROMANTIC],
        Occasion.MEHENDI: [Style.TRADITIONAL, Style.ETHNIC, Style.FESTIVE, Style.CASUAL],
        Occasion.SANGEET: [Style.FESTIVE, Style.PARTY, Style.CONTEMPORARY, Style.TRADITIONAL],
        Occasion.OFFICE: [Style.BUSINESS, Style.FORMAL, Style.SMART_CASUAL, Style.MINIMALIST],
        Occasion.BUSINESS_MEETING: [Style.BUSINESS, Style.FORMAL, Style.MINIMALIST],
        Occasion.INTERVIEW: [Style.BUSINESS, Style.FORMAL, Style.MINIMALIST, Style.CLASSIC],
        Occasion.CASUAL: [Style.CASUAL, Style.STREETWEAR, Style.ATHLEISURE, Style.SPORTY],
        Occasion.PARTY: [Style.PARTY, Style.CLUB, Style.COCKTAIL, Style.CONTEMPORARY],
        Occasion.CLUB: [Style.CLUB, Style.PARTY, Style.ROCK, Style.STREETWEAR],
        Occasion.DATE: [Style.ROMANTIC, Style.CONTEMPORARY, Style.SMART_CASUAL, Style.COCKTAIL],
        Occasion.DINNER: [Style.SMART_CASUAL, Style.CONTEMPORARY, Style.COCKTAIL, Style.ROMANTIC],
        Occasion.BEACH: [Style.CASUAL, Style.BOHEMIAN, Style.RESORT, Style.SPORTY],
        Occasion.VACATION: [Style.CASUAL, Style.RESORT, Style.BOHEMIAN, Style.ATHLEISURE],
        Occasion.FESTIVAL: [Style.FESTIVE, Style.BOHEMIAN, Style.STREETWEAR, Style.CONTEMPORARY],
        Occasion.DIWALI: [Style.TRADITIONAL, Style.ETHNIC, Style.FESTIVE, Style.PARTY],
        Occasion.HOLI: [Style.CASUAL, Style.STREETWEAR, Style.ATHLEISURE, Style.BOHEMIAN],
        Occasion.POOJA: [Style.TRADITIONAL, Style.ETHNIC, Style.CASUAL, Style.MINIMALIST],
        Occasion.TEMPLE_VISIT: [Style.TRADITIONAL, Style.ETHNIC, Style.CASUAL, Style.MINIMALIST],
    }
    
    # Return styles for the occasion, or default to casual
    return occasion_style_map.get(occasion, [Style.CASUAL, Style.SMART_CASUAL, Style.CONTEMPORARY])
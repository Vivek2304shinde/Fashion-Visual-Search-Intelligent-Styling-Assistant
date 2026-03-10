"""
Intelligent Styling Engine
Uses color_rules and style_rules to generate smart outfit combinations
"""

import random
from typing import Dict, List, Any, Optional
from ai_stylist.config.color_rules import (
    get_complementary_colors, get_analogous_colors,
    COLOR_FAMILIES, WARM_COLORS, COOL_COLORS, NEUTRAL_COLORS
)
from ai_stylist.config.style_rules import (
    STYLE_COMPATIBILITY, OCCASION_STYLES
)
from ai_stylist.schemas import Color, Style, Occasion

class IntelligentStylingEngine:
    """
    Generates intelligent outfit combinations using fashion rules
    """
    
    def __init__(self):
        # Modern fashion combinations for 2024-2025
        self.TRENDY_COMBINATIONS = {
            "navy": {
                "primary": ["beige", "cream", "white", "burgundy"],
                "accent": ["gold", "brown", "tan"],
                "avoid": ["black", "dark_grey"]
            },
            "blue": {
                "primary": ["white", "grey", "beige", "brown"],
                "accent": ["orange", "yellow", "red"],
                "avoid": ["purple", "pink"]
            },
            "black": {
                "primary": ["white", "grey", "red", "gold"],
                "accent": ["silver", "purple", "emerald"],
                "avoid": ["brown", "navy"]
            },
            "burgundy": {
                "primary": ["beige", "cream", "navy", "grey"],
                "accent": ["gold", "black", "emerald"],
                "avoid": ["purple", "pink"]
            },
            "green": {
                "primary": ["beige", "brown", "cream", "navy"],
                "accent": ["gold", "orange", "burgundy"],
                "avoid": ["blue", "purple"]
            }
        }
        
        # Category-specific styling rules
        self.CATEGORY_STYLING = {
            "kurta": {
                "fits": ["regular", "slim", "relaxed"],
                "fabrics": ["cotton", "silk", "linen", "chiffon"],
                "patterns": ["solid", "embroidered", "printed"]
            },
            "churidar": {
                "fits": ["slim", "regular"],
                "fabrics": ["cotton", "lycra", "silk"],
                "colors": ["beige", "cream", "white", "black", "maroon"]
            },
            "mojari": {
                "styles": ["traditional", "ethnic"],
                "colors": ["brown", "black", "beige", "maroon", "gold"]
            },
            "watch": {
                "styles": ["classic", "sporty", "luxury"],
                "materials": ["leather", "metal", "silicone"]
            },
            "shawl": {
                "styles": ["traditional", "casual"],
                "fabrics": ["wool", "pashmina", "cotton"],
                "colors": ["beige", "cream", "brown", "maroon", "gold"]
            },
            "sunglasses": {
                "styles": ["aviator", "wayfarer", "round"],
                "colors": ["black", "brown", "gold", "silver"]
            }
        }
    
    def generate_smart_queries(self, collected_info: Dict) -> Dict[str, List[str]]:
        """
        Generate intelligent search queries with complementary colors
        """
        occasion = collected_info.get("occasion", "wedding")
        gender = collected_info.get("gender", "male")
        primary_color = collected_info.get("color_preference", "navy")
        style = collected_info.get("style_preference", "traditional")
        season = collected_info.get("season", "summer")
        
        # Get complementary colors using your color_rules
        try:
            color_enum = Color(primary_color)
            complementary = get_complementary_colors(color_enum, count=4)
            comp_colors = [c.value for c in complementary]
        except:
            # Fallback to trendy combinations
            comp_colors = self.TRENDY_COMBINATIONS.get(primary_color, {}).get("primary", 
                ["beige", "cream", "white", "brown"])
        
        # Define outfit composition based on occasion and gender
        outfit = self._get_outfit_composition(occasion, gender, style)
        
        smart_queries = {}
        
        # Assign intelligent colors to each category
        for idx, category in enumerate(outfit):
            queries = []
            
            # Base query
            queries.append(f"{gender} {category}")
            
            # Primary color for main items
            if category in ["kurta", "sherwani", "shirt", "dress", "saree"]:
                # Main garment gets primary color
                queries.append(f"{primary_color} {gender} {category} {style}")
                queries.append(f"{style} {gender} {category} {primary_color}")
                
                # Add season-specific
                if season:
                    queries.append(f"{season} {gender} {category} {primary_color}")
            
            elif category in ["churidar", "pants", "jeans", "palazzo"]:
                # Bottom wear gets complementary colors
                for comp in comp_colors[:2]:
                    queries.append(f"{comp} {gender} {category}")
                    queries.append(f"{style} {gender} {category} {comp}")
            
            elif category in ["mojari", "jutti", "shoes", "loafers"]:
                # Footwear gets accent colors
                accent_colors = ["brown", "black", "tan", "beige"]
                for color in accent_colors[:2]:
                    queries.append(f"{color} {gender} {category} {style}")
            
            elif category in ["watch", "sunglasses", "belt"]:
                # Accessories get metallic or neutral
                accessory_colors = ["black", "brown", "gold", "silver", "tan"]
                for color in accessory_colors[:2]:
                    queries.append(f"{color} {gender} {category} {style}")
            
            elif category in ["necklace", "earrings", "bangles"]:
                # Jewelry gets metallic
                jewelry_colors = ["gold", "silver", "rose gold", "oxidized"]
                for color in jewelry_colors[:2]:
                    queries.append(f"{color} {gender} {category} {style}")
            
            elif category in ["shawl", "dupatta", "jacket"]:
                # Layering pieces get complementary or accent
                for comp in comp_colors[:2]:
                    queries.append(f"{comp} {gender} {category} {style}")
            
            # Add trendy/modern modifiers
            trendy_modifiers = ["designer", "trendy", "fashion", "latest", "premium"]
            queries.append(f"{gender} {category} {random.choice(trendy_modifiers)}")
            
            # Remove duplicates and limit
            smart_queries[category] = list(set(queries))[:5]
        
        return smart_queries
    
    def _get_outfit_composition(self, occasion: str, gender: str, style: str) -> List[str]:
        """Get appropriate outfit composition"""
        
        # Traditional Indian wedding outfit
        if occasion == "wedding" and style == "traditional":
            if gender == "male":
                return ["sherwani", "churidar", "mojari", "watch", "shawl", "sunglasses"]
            else:
                return ["lehenga", "blouse", "heels", "necklace", "earrings", "bangles", "clutch"]
        
        # Modern fusion wedding
        elif occasion == "wedding" and style == "contemporary":
            if gender == "male":
                return ["bandhgala", "churidar", "mojari", "watch", "sunglasses"]
            else:
                return ["indo_western", "palazzo", "heels", "necklace", "earrings", "clutch"]
        
        # Party wear
        elif occasion == "party":
            if gender == "male":
                return ["shirt", "jeans", "jacket", "boots", "watch", "sunglasses"]
            else:
                return ["dress", "heels", "clutch", "necklace", "earrings", "watch"]
        
        # Office wear
        elif occasion == "office":
            if gender == "male":
                return ["shirt", "pants", "blazer", "formal_shoes", "watch", "belt"]
            else:
                return ["blouse", "pants", "blazer", "heels", "watch", "bag"]
        
        # Casual
        else:
            if gender == "male":
                return ["t_shirt", "jeans", "sneakers", "watch", "cap"]
            else:
                return ["top", "jeans", "sneakers", "watch", "bag"]
    
    def get_styling_advice(self, collected_info: Dict) -> Dict[str, str]:
        """Generate styling advice for each category"""
        
        primary_color = collected_info.get("color_preference", "navy")
        occasion = collected_info.get("occasion", "wedding")
        
        advice = {}
        
        # Get complementary colors
        try:
            color_enum = Color(primary_color)
            complements = get_complementary_colors(color_enum, count=3)
            comp_names = [c.value for c in complements]
        except:
            comp_names = ["beige", "cream", "brown"]
        
        # Kurta/Sherwani advice
        advice["main"] = f"Choose a {primary_color} {collected_info.get('style_preference', 'traditional')} style piece"
        
        # Bottom wear advice
        advice["bottom"] = f"Pair with {comp_names[0]} colored bottom wear for a classic contrast"
        
        # Footwear advice
        if primary_color in ["navy", "blue", "black"]:
            advice["footwear"] = f"Brown or tan footwear would complement your {primary_color} outfit perfectly"
        else:
            advice["footwear"] = f"Choose neutral {comp_names[1]} or brown footwear"
        
        # Accessories advice
        advice["accessories"] = f"Add gold-toned accessories to elevate the look"
        
        # Watch advice
        if primary_color in ["navy", "black"]:
            advice["watch"] = "A brown leather strap watch would look sophisticated"
        else:
            advice["watch"] = "A metal bracelet watch would complement well"
        
        return advice
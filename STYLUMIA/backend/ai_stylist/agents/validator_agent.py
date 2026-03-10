"""
Validator Agent: Validates outfit combinations.
Uses color_rules and style_rules from config.
"""

from typing import Dict, List, Any, Optional
from ai_stylist.schemas import Product, CategorySpec, Occasion, Style, Color
from ai_stylist.config.color_rules import (
    validate_color_combination, get_complementary_colors
)
from ai_stylist.config.style_rules import (
    validate_style_combination, validate_style_for_occasion
)

class ValidatorAgent:
    """
    Agent responsible for validating outfit combinations.
    Uses the actual rules from config files.
    """
    
    async def validate_outfit(
        self,
        products: Dict[str, List[Product]],
        categories: Dict[str, CategorySpec],
        intent: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate the complete outfit.
        Returns validation results and suggestions.
        """
        
        validation_result = {
            "is_valid": True,
            "score": 0.0,
            "issues": [],
            "warnings": [],
            "suggestions": [],
            "color_advice": "",
            "style_advice": ""
        }
        
        # Get selected products (top 1 from each category)
        selected = {}
        for category, items in products.items():
            if items:
                selected[category] = items[0]
        
        if not selected:
            validation_result["is_valid"] = False
            validation_result["issues"].append("No products selected")
            return validation_result
        
        # 1. Extract colors from products
        product_colors = []
        for cat, product in selected.items():
            if product.color:
                try:
                    # Try to convert to Color enum
                    color_enum = Color(product.color.lower())
                    product_colors.append(color_enum)
                except (ValueError, AttributeError):
                    # If not in enum, just use string
                    pass
        
        # 2. Validate color combinations using config rules
        if len(product_colors) >= 2:
            occasion = intent.get("occasion", "casual")
            try:
                occasion_enum = Occasion(occasion)
            except:
                occasion_enum = Occasion.CASUAL
            
            colors_valid, color_reason, color_score = validate_color_combination(
                product_colors, occasion_enum
            )
            
            validation_result["color_advice"] = color_reason
            
            if not colors_valid:
                validation_result["issues"].append(f"Color issue: {color_reason}")
                validation_result["is_valid"] = False
                
                # Suggest better colors using config function
                if product_colors:
                    complements = get_complementary_colors(product_colors[0], count=3)
                    if complements:
                        validation_result["suggestions"].append(
                            f"Try colors like: {', '.join([c.value for c in complements])}"
                        )
        
        # 3. Validate style compatibility using config rules
        product_styles = []
        for cat, product in selected.items():
            if product.style:
                try:
                    style_enum = Style(product.style.lower())
                    product_styles.append(style_enum)
                except (ValueError, AttributeError):
                    pass
        
        if product_styles:
            primary_style = intent.get("style", "casual")
            try:
                primary_style_enum = Style(primary_style)
            except:
                primary_style_enum = Style.CASUAL
            
            styles_valid, style_reason, style_score = validate_style_combination(
                product_styles, primary_style_enum
            )
            
            validation_result["style_advice"] = style_reason
            
            if not styles_valid:
                validation_result["issues"].append(f"Style issue: {style_reason}")
                validation_result["is_valid"] = False
        
        # 4. Validate against occasion using config
        if "occasion" in intent and product_styles:
            occasion = intent["occasion"]
            try:
                occasion_enum = Occasion(occasion)
                style_ok, occasion_reason, _ = validate_style_for_occasion(
                    product_styles[0], occasion_enum
                )
                
                if not style_ok:
                    validation_result["warnings"].append(occasion_reason)
            except:
                pass
        
        # 5. Calculate overall score
        color_score = len([c for c in validation_result.get("color_advice", "") if "works" in c.lower()]) * 20
        style_score = len([s for s in validation_result.get("style_advice", "") if "works" in s.lower()]) * 20
        completeness_score = min(100, len(selected) * 20)  # 20 points per item
        
        validation_result["score"] = (color_score + style_score + completeness_score) / 3
        
        return validation_result
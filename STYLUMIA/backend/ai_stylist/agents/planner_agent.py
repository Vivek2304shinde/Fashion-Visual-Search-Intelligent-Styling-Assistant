"""
Planner Agent: Determines which categories to scrape based on intent.
Uses category config as single source of truth.
"""

import json
from typing import Dict, List, Any, Optional
from openai import OpenAI
from groq import Groq
import os

from ai_stylist.schemas import CategorySpec
from ai_stylist.config.categories import (
    OUTFIT_CATEGORIES, get_category_config, get_category_display_name
)
from config import config

class PlannerAgent:
    """
    Agent responsible for planning which categories to scrape.
    Uses templates based on occasion and gender.
    """
    
    def __init__(self):
        self.client = Groq( api_key = os.getenv("OPENAI_API_KEY"),
                                base_url = os.getenv("OPENAI_BASE_URL"))
        
        # Define outfit templates based on occasion and gender
        # Using occasion values that match your schemas
        self.OUTFIT_TEMPLATES = {
            "male": {
                "wedding": ["sherwani", "kurta", "pants", "mojari", "watch"],
                "reception": ["suit", "shirt", "tie", "formal_shoes", "watch"],
                "engagement": ["suit", "shirt", "formal_shoes", "watch"],
                "office": ["shirt", "pants", "formal_shoes", "watch", "belt"],
                "business_meeting": ["shirt", "pants", "blazer", "formal_shoes", "watch"],
                "interview": ["shirt", "pants", "formal_shoes", "watch", "belt"],
                "casual": ["t_shirt", "jeans", "sneakers", "watch"],
                "party": ["shirt", "jeans", "boots", "watch", "jacket"],
                "club": ["shirt", "jeans", "boots", "watch"],
                "date": ["polo", "chinos", "loafers", "watch"],
                "dinner": ["shirt", "pants", "loafers", "watch"],
                "brunch": ["polo", "chinos", "sneakers", "watch"],
                "beach": ["t_shirt", "shorts", "sandals", "sunglasses"],
                "vacation": ["t_shirt", "shorts", "sandals", "sunglasses", "hat"],
                "festival": ["kurta", "jeans", "mojari", "watch"],
                "diwali": ["kurta", "churidar", "mojari", "watch"],
                "holi": ["t_shirt", "shorts", "sneakers"],
                "traditional": ["kurta", "churidar", "mojari", "watch"],
                "ethnic": ["kurta", "churidar", "mojari", "watch"],
                "sports_event": ["t_shirt", "jeans", "sneakers", "cap"],
                "concert": ["t_shirt", "jeans", "boots", "watch"],
                "graduation": ["shirt", "pants", "formal_shoes", "watch"],
                "anniversary": ["shirt", "pants", "formal_shoes", "watch"],
                "birthday": ["shirt", "jeans", "sneakers", "watch"],
                "pooja": ["kurta", "dhoti", "mojari"],
                "temple_visit": ["kurta", "pants", "mojari"],
                "cocktail": ["shirt", "pants", "blazer", "formal_shoes", "watch"],
                "formal": ["suit", "shirt", "tie", "formal_shoes", "watch"],
                "semi_formal": ["shirt", "pants", "blazer", "formal_shoes", "watch"],
                "black_tie": ["tuxedo", "shirt", "bow_tie", "formal_shoes", "watch"],
                "white_tie": ["tailcoat", "shirt", "bow_tie", "formal_shoes", "watch"],
            },
            "female": {
                "wedding": ["saree", "blouse", "heels", "necklace", "earrings", "bangles", "clutch"],
                "reception": ["gown", "heels", "clutch", "necklace", "earrings"],
                "engagement": ["dress", "heels", "clutch", "necklace", "earrings"],
                "office": ["blouse", "pants", "blazer", "heels", "watch", "bag"],
                "business_meeting": ["blouse", "pants", "blazer", "heels", "watch", "bag"],
                "interview": ["blouse", "pants", "blazer", "heels", "watch", "bag"],
                "casual": ["t_shirt", "jeans", "sneakers", "watch"],
                "party": ["dress", "heels", "clutch", "necklace", "earrings"],
                "club": ["dress", "heels", "clutch", "earrings"],
                "date": ["dress", "heels", "clutch", "necklace"],
                "dinner": ["dress", "heels", "clutch", "necklace"],
                "brunch": ["dress", "sandals", "sunglasses", "bag"],
                "beach": ["dress", "sandals", "sunglasses", "hat", "bag"],
                "vacation": ["dress", "sandals", "sunglasses", "hat", "bag"],
                "festival": ["kurti", "palazzo", "jutti", "necklace", "earrings", "bangles"],
                "diwali": ["kurti", "palazzo", "jutti", "necklace", "earrings", "bangles"],
                "holi": ["kurti", "leggings", "sneakers"],
                "traditional": ["saree", "blouse", "heels", "necklace", "earrings", "bangles"],
                "ethnic": ["kurti", "palazzo", "jutti", "necklace", "earrings", "bangles"],
                "sports_event": ["t_shirt", "jeans", "sneakers", "cap"],
                "concert": ["top", "jeans", "boots", "watch"],
                "graduation": ["dress", "heels", "clutch", "earrings"],
                "anniversary": ["dress", "heels", "clutch", "necklace", "earrings"],
                "birthday": ["dress", "heels", "clutch", "earrings"],
                "pooja": ["kurti", "leggings", "dupatta", "jutti"],
                "temple_visit": ["kurti", "leggings", "dupatta", "jutti"],
                "cocktail": ["cocktail_dress", "heels", "clutch", "necklace", "earrings"],
                "formal": ["gown", "heels", "clutch", "necklace", "earrings"],
                "semi_formal": ["dress", "heels", "clutch", "necklace", "earrings"],
                "black_tie": ["evening_gown", "heels", "clutch", "diamond_jewelry"],
                "white_tie": ["ball_gown", "heels", "clutch", "diamond_jewelry", "gloves"],
            },
            "unisex": {
                "wedding": ["shirt", "pants", "blazer", "shoes", "watch"],
                "reception": ["shirt", "pants", "blazer", "shoes", "watch"],
                "engagement": ["shirt", "pants", "blazer", "shoes", "watch"],
                "office": ["shirt", "pants", "shoes", "watch"],
                "business_meeting": ["shirt", "pants", "blazer", "shoes", "watch"],
                "interview": ["shirt", "pants", "shoes", "watch"],
                "casual": ["t_shirt", "jeans", "sneakers", "watch"],
                "party": ["shirt", "jeans", "shoes", "watch"],
                "club": ["shirt", "jeans", "shoes", "watch"],
                "date": ["shirt", "pants", "shoes", "watch"],
                "dinner": ["shirt", "pants", "shoes", "watch"],
                "brunch": ["t_shirt", "jeans", "sneakers", "watch"],
                "beach": ["t_shirt", "shorts", "sandals", "sunglasses"],
                "vacation": ["t_shirt", "shorts", "sandals", "sunglasses"],
                "festival": ["kurta", "pants", "mojari", "watch"],
                "diwali": ["kurta", "pants", "mojari", "watch"],
                "holi": ["t_shirt", "shorts", "sneakers"],
                "traditional": ["kurta", "pants", "mojari", "watch"],
                "ethnic": ["kurta", "pants", "mojari", "watch"],
                "sports_event": ["t_shirt", "jeans", "sneakers"],
                "concert": ["t_shirt", "jeans", "boots", "watch"],
                "graduation": ["shirt", "pants", "shoes", "watch"],
                "anniversary": ["shirt", "pants", "shoes", "watch"],
                "birthday": ["shirt", "jeans", "shoes", "watch"],
                "pooja": ["kurta", "pants", "mojari"],
                "temple_visit": ["kurta", "pants", "mojari"],
                "cocktail": ["shirt", "pants", "blazer", "shoes", "watch"],
                "formal": ["suit", "shirt", "tie", "shoes", "watch"],
                "semi_formal": ["shirt", "pants", "blazer", "shoes", "watch"],
                "black_tie": ["tuxedo", "shirt", "bow_tie", "shoes", "watch"],
                "white_tie": ["tailcoat", "shirt", "bow_tie", "shoes", "watch"],
            }
        }
    
    async def plan_categories(
        self,
        intent: Dict[str, Any],
        user_context: Optional[Any] = None
    ) -> Dict[str, CategorySpec]:
        """
        Plan which categories to scrape based on intent.
        Returns dict of category -> CategorySpec.
        """
        
        # Extract key info
        occasion = intent.get("occasion", "casual")
        style = intent.get("style", "casual")
        gender = intent.get("gender", "unisex")
        primary_color = intent.get("primary_color")
        specific_reqs = intent.get("specific_requirements", {})
        
        # Get base categories from template
        base_categories = self._get_categories_for_occasion(occasion, gender)
        
        # Build specs for each category
        categories = {}
        
        for category in base_categories:
            # Check if category exists in our config
            if category not in OUTFIT_CATEGORIES:
                print(f"⚠️ Warning: {category} not in category config, skipping")
                continue
            
            # Get category config
            cat_config = get_category_config(category)
            
            # Build spec
            spec = CategorySpec()
            
            # Apply general intent
            if primary_color:
                spec.color = primary_color
            
            # Apply category-specific requirements
            if category in specific_reqs:
                reqs = specific_reqs[category]
                if "color" in reqs:
                    spec.color = reqs["color"]
                if "fit" in reqs:
                    spec.fit = reqs["fit"]
                if "fabric" in reqs:
                    spec.fabric = reqs["fabric"]
            
            # Add style to spec
            spec.style = style
            
            # Add budget hints
            budget_tier = intent.get("budget_tier", "mid_range")
            if budget_tier == "budget":
                spec.max_price = 2000
            elif budget_tier == "mid_range":
                spec.min_price = 1000
                spec.max_price = 5000
            elif budget_tier == "premium":
                spec.min_price = 3000
                spec.max_price = 10000
            elif budget_tier == "luxury":
                spec.min_price = 8000
            
            categories[category] = spec
        
        # Use LLM to refine the plan if needed (less than 3 categories)
        if len(categories) < 3:
            enhanced = await self._enhance_plan(intent, categories)
            if enhanced and len(enhanced) > len(categories):
                return enhanced
        
        return categories
    
    def _get_categories_for_occasion(self, occasion: str, gender: str) -> List[str]:
        """
        Get base categories for occasion/gender from templates.
        """
        # Normalize occasion to match template keys
        occasion = occasion.lower().replace(" ", "_")
        
        # Get gender-appropriate template
        gender_key = gender if gender in self.OUTFIT_TEMPLATES else "unisex"
        template = self.OUTFIT_TEMPLATES[gender_key].get(occasion, [])
        
        # If no template for this occasion, return default based on formality
        if not template:
            # Try to infer from occasion name
            if any(word in occasion for word in ["wedding", "reception", "engagement"]):
                template = self.OUTFIT_TEMPLATES[gender_key].get("wedding", [])
            elif any(word in occasion for word in ["office", "business", "interview"]):
                template = self.OUTFIT_TEMPLATES[gender_key].get("office", [])
            elif any(word in occasion for word in ["party", "club", "cocktail"]):
                template = self.OUTFIT_TEMPLATES[gender_key].get("party", [])
            elif any(word in occasion for word in ["beach", "vacation"]):
                template = self.OUTFIT_TEMPLATES[gender_key].get("beach", [])
            elif any(word in occasion for word in ["traditional", "ethnic", "festival"]):
                template = self.OUTFIT_TEMPLATES[gender_key].get("traditional", [])
            else:
                # Default to casual
                template = self.OUTFIT_TEMPLATES[gender_key].get("casual", 
                    ["t_shirt", "jeans", "sneakers", "watch"])
        
        return template
    
    async def _enhance_plan(
        self,
        intent: Dict[str, Any],
        current_categories: Dict[str, CategorySpec]
    ) -> Optional[Dict[str, CategorySpec]]:
        """
        Use LLM to enhance the plan if base templates are insufficient.
        """
        try:
            # Get available categories from config
            available_categories = list(OUTFIT_CATEGORIES.keys())
            
            prompt = f"""You are an outfit planner. Based on this request, suggest 4-6 clothing categories to search for.

INTENT:
- Occasion: {intent.get('occasion')}
- Style: {intent.get('style')} 
- Gender: {intent.get('gender')}
- Primary color: {intent.get('primary_color')}

CURRENT PLAN: {list(current_categories.keys())}

AVAILABLE CATEGORIES: {available_categories[:50]}

Return a JSON object with categories as keys and specifications as values.
Each spec can include: color, style, fit, fabric (use null if not specified).

Example:
{{
    "shirt": {{"color": "navy", "style": "formal", "fit": "slim"}},
    "pants": {{"color": "black", "style": "formal", "fit": "regular"}},
    "shoes": {{"style": "formal"}},
    "watch": {{}}
}}

Return ONLY valid JSON."""
            
            response = self.client.chat.completions.create(
                model=config.LLM_MODEL,
                temperature=0.3,
                messages=[
                    {"role": "system", "content": "You are an outfit planner. Return JSON only."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            enhanced = json.loads(response.choices[0].message.content)
            
            # Convert to CategorySpec objects
            result = {}
            for cat, spec_dict in enhanced.items():
                if cat in OUTFIT_CATEGORIES:
                    # Merge with existing spec if any
                    if cat in current_categories:
                        existing = current_categories[cat].dict()
                        existing.update(spec_dict)
                        spec = CategorySpec(**existing)
                    else:
                        spec = CategorySpec(**spec_dict)
                    result[cat] = spec
            
            if result and len(result) > len(current_categories):
                return result
                
        except Exception as e:
            print(f"⚠️ Plan enhancement failed: {e}")
        
        return None
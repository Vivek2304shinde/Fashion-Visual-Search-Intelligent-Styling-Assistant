# """
# Intent Agent: Analyzes user query to extract structured intent.
# Uses LLM to understand occasion, style, colors, and requirements.
# """

# import json
# import re
# from typing import Dict, Any, Optional, List
# from datetime import datetime
# from openai import OpenAI

# from ai_stylist.schemas import (
#     UserQuery, UserContext, Occasion, Style, Gender, 
#     Color, Season, PriceRange, CategorySpec
# )
# from ai_stylist.config.categories import get_all_categories
# from config import config

# class IntentAgent:
#     """
#     Agent responsible for understanding user intent from natural language.
#     Extracts occasion, style preferences, colors, and implicit requirements.
#     """
    
#     def __init__(self):
#         self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        
#         # Intent extraction prompt
#         self.INTENT_PROMPT = """You are an expert fashion stylist AI. Analyze the user's query and extract structured intent.

# User Query: {user_query}

# Additional Context (if any):
# {context}

# Available Options:
# - Occasions: {occasions}
# - Styles: {styles}
# - Colors: {colors}
# - Categories: {categories}

# Your task is to extract:
# 1. Primary occasion (from the list above)
# 2. Primary style (from the list above)
# 3. Gender (male/female/unisex) - infer from query
# 4. Primary color (from the list above) - if mentioned or implied
# 5. Secondary/accent colors - if mentioned
# 6. Specific category requirements (e.g., "slim fit shirt", "leather shoes")
# 7. Budget range (low/medium/high/luxury) - if implied
# 8. Season/weather - if relevant
# 9. Any specific brands mentioned
# 10. Any items to avoid or exclude

# Also note any implicit needs:
# - Is this for a specific time of day? (morning/evening/night)
# - Indoor or outdoor event?
# - Formalness level (1-10)
# - Any cultural considerations?

# Return a structured JSON with:
# {{
#     "occasion": "occasion_name",
#     "style": "style_name", 
#     "gender": "male/female/unisex",
#     "primary_color": "color_name or null",
#     "secondary_colors": ["color1", "color2"] or [],
#     "accent_color": "color_name or null",
#     "budget_tier": "budget/economy/mid_range/premium/luxury",
#     "season": "summer/winter/spring/fall/monsoon/all",
#     "specific_requirements": {{
#         "category_name": {{
#             "fit": "fit_type",
#             "fabric": "fabric_type",
#             "color": "color_name",
#             "style": "style_name",
#             "must_have": ["feature1", "feature2"],
#             "avoid": ["feature1", "feature2"]
#         }}
#     }},
#     "mentioned_brands": ["brand1", "brand2"],
#     "excluded_items": ["item1", "item2"],
#     "implicit_needs": {{
#         "time_of_day": "morning/afternoon/evening/night",
#         "indoor_outdoor": "indoor/outdoor/both",
#         "formality_level": 1-10,
#         "cultural_context": "description if any"
#     }},
#     "query_summary": "Brief one-line summary of what user wants"
# }}

# Be intelligent about implicit needs:
# - "wedding" usually means formal/traditional
# - "beach" suggests casual, light fabrics
# - "office" suggests formal/business
# - "date night" suggests semi-formal, stylish
# - "party" suggests trendy, possibly bold

# If information isn't specified, use null or empty lists.
# """
    
#     async def extract_intent(self, query: UserQuery) -> Dict[str, Any]:
#         """
#         Extract structured intent from user query.
#         """
#         try:
#             # Prepare context string
#             context_str = ""
#             if query.context:
#                 context_str = f"User Context: {query.context.dict()}"
#             if query.occasion:
#                 context_str += f"\nSpecified Occasion: {query.occasion}"
#             if query.season:
#                 context_str += f"\nSpecified Season: {query.season}"
            
#             # Get available options for prompting
#             occasions = [o.value for o in Occasion]
#             styles = [s.value for s in Style]
#             colors = [c.value for c in Color][:50]  # Limit to avoid token overflow
#             categories = get_all_categories()
            
#             # Call LLM
#             response = self.client.chat.completions.create(
#                 model=config.LLM_MODEL,
#                 temperature=0.3,  # Lower temperature for consistent extraction
#                 messages=[
#                     {"role": "system", "content": "You are an expert fashion intent extractor. Return only valid JSON."},
#                     {"role": "user", "content": self.INTENT_PROMPT.format(
#                         user_query=query.message,
#                         context=context_str,
#                         occasions=", ".join(occasions[:20]),
#                         styles=", ".join(styles[:20]),
#                         colors=", ".join(colors[:30]),
#                         categories=", ".join(categories[:30])
#                     )}
#                 ],
#                 response_format={"type": "json_object"}
#             )
            
#             # Parse response
#             intent = json.loads(response.choices[0].message.content)
            
#             # Validate and clean intent
#             intent = self._validate_intent(intent)
            
#             return intent
            
#         except Exception as e:
#             print(f"❌ Intent extraction failed: {e}")
#             # Return default intent
#             return self._get_default_intent(query.message)
    
#     def _validate_intent(self, intent: Dict) -> Dict:
#         """
#         Validate and clean extracted intent.
#         """
#         # Ensure occasion is valid
#         if "occasion" in intent and intent["occasion"]:
#             try:
#                 # Try to match to enum
#                 occasion_value = intent["occasion"].lower().replace(" ", "_")
#                 if occasion_value in [o.value for o in Occasion]:
#                     intent["occasion"] = occasion_value
#                 else:
#                     # Find closest match
#                     intent["occasion"] = self._find_closest_match(
#                         occasion_value, 
#                         [o.value for o in Occasion]
#                     ) or "casual"
#             except:
#                 intent["occasion"] = "casual"
#         else:
#             intent["occasion"] = "casual"
        
#         # Ensure style is valid
#         if "style" in intent and intent["style"]:
#             try:
#                 style_value = intent["style"].lower().replace(" ", "_")
#                 if style_value in [s.value for s in Style]:
#                     intent["style"] = style_value
#                 else:
#                     intent["style"] = self._find_closest_match(
#                         style_value,
#                         [s.value for s in Style]
#                     ) or "casual"
#             except:
#                 intent["style"] = "casual"
#         else:
#             intent["style"] = "casual"
        
#         # Ensure gender is valid
#         if "gender" in intent and intent["gender"]:
#             gender = intent["gender"].lower()
#             if gender in ["male", "female", "unisex"]:
#                 intent["gender"] = gender
#             else:
#                 intent["gender"] = "unisex"
#         else:
#             intent["gender"] = "unisex"
        
#         # Ensure color is valid if provided
#         if "primary_color" in intent and intent["primary_color"]:
#             color_str = intent["primary_color"].lower().replace(" ", "_")
#             if color_str in [c.value for c in Color]:
#                 intent["primary_color"] = color_str
#             else:
#                 # Try to find closest color
#                 matched = self._find_closest_match(
#                     color_str,
#                     [c.value for c in Color]
#                 )
#                 intent["primary_color"] = matched if matched else None
        
#         return intent
    
#     def _find_closest_match(self, value: str, options: List[str]) -> Optional[str]:
#         """
#         Find closest matching string from options.
#         Simple implementation - in production use fuzzy matching.
#         """
#         value_lower = value.lower()
#         for option in options:
#             if option in value_lower or value_lower in option:
#                 return option
#         return None
    
#     def _get_default_intent(self, query: str) -> Dict:
#         """
#         Get default intent when LLM fails.
#         """
#         return {
#             "occasion": "casual",
#             "style": "casual",
#             "gender": "unisex",
#             "primary_color": None,
#             "secondary_colors": [],
#             "accent_color": None,
#             "budget_tier": "mid_range",
#             "season": "all",
#             "specific_requirements": {},
#             "mentioned_brands": [],
#             "excluded_items": [],
#             "implicit_needs": {
#                 "time_of_day": None,
#                 "indoor_outdoor": None,
#                 "formality_level": 5,
#                 "cultural_context": None
#             },
#             "query_summary": query[:100]
#         }


"""
Intent Agent: Analyzes user query to extract structured intent.
Uses LLM with prompt engineering - no complex functions needed.
"""

import json
import os
import os
from typing import Dict, Any, Optional
from openai import OpenAI
from groq import Groq

from ai_stylist.schemas import UserQuery, Occasion, Style, Color
from config import config

class IntentAgent:
    """
    Agent responsible for understanding user intent from natural language.
    Pure prompt engineering - no vague helper functions.
    """
    
    def __init__(self):
        self.client = Groq( api_key = os.getenv("OPENAI_API_KEY"),
                                base_url = os.getenv("OPENAI_BASE_URL"))
        
        # Clean, focused prompt - no complex logic needed
        self.INTENT_PROMPT = """You are a fashion intent extractor. Analyze the user's message and extract structured information.

USER MESSAGE: {user_query}

AVAILABLE OPTIONS (use these exact values):
- Occasions: {occasions}
- Styles: {styles}
- Colors: {colors}

TASK: Extract the following as JSON. Use null if not mentioned.
- occasion: most relevant from list above
- style: most relevant from list above
- gender: "male", "female", or "unisex"
- primary_color: main color mentioned or implied
- secondary_colors: array of other colors mentioned
- budget_tier: "budget", "mid_range", "premium", or "luxury" based on clues
- season: "summer", "winter", "spring", "fall", "monsoon", or "all"
- specific_requirements: object with category-specific needs
- mentioned_brands: array of brand names mentioned
- query_summary: brief one-line summary

EXAMPLES:
Input: "I need a navy blue suit for a wedding next month"
Output: {{"occasion": "wedding", "style": "formal", "gender": "male", "primary_color": "navy", "secondary_colors": [], "budget_tier": "mid_range", "season": "all", "specific_requirements": {{"suit": {{"color": "navy"}}}}, "mentioned_brands": [], "query_summary": "navy suit for wedding"}}

Input: "Looking for a casual summer dress for a beach party"
Output: {{"occasion": "beach", "style": "casual", "gender": "female", "primary_color": null, "secondary_colors": [], "budget_tier": "mid_range", "season": "summer", "specific_requirements": {{"dress": {{"style": "casual"}}}}, "mentioned_brands": [], "query_summary": "casual summer dress for beach"}}

Return ONLY valid JSON, no other text.
"""
    
    async def extract_intent(self, query: UserQuery) -> Dict[str, Any]:
        """
        Extract structured intent from user query using pure LLM.
        """
        try:
            # Prepare available options (limited to avoid token overflow)
            occasions = [o.value for o in Occasion][:30]
            styles = [s.value for s in Style][:30]
            colors = [c.value for c in Color][:50]
            
            # Call LLM with clean prompt
            response = self.client.chat.completions.create(
                model=config.LLM_MODEL,
                temperature=0.2,  # Low temp for consistent extraction
                messages=[
                    {"role": "system", "content": "You extract fashion intent as JSON. Use only provided values."},
                    {"role": "user", "content": self.INTENT_PROMPT.format(
                        user_query=query.message,
                        occasions=", ".join(occasions),
                        styles=", ".join(styles),
                        colors=", ".join(colors[:30])
                    )}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse response
            intent = json.loads(response.choices[0].message.content)
            
            # Add any explicit context from query
            if query.occasion:
                intent["occasion"] = query.occasion.value
            if query.season:
                intent["season"] = query.season.value
            if query.budget_total:
                # Simple budget tier inference
                if query.budget_total < 5000:
                    intent["budget_tier"] = "budget"
                elif query.budget_total < 15000:
                    intent["budget_tier"] = "mid_range"
                elif query.budget_total < 50000:
                    intent["budget_tier"] = "premium"
                else:
                    intent["budget_tier"] = "luxury"
            
            return intent
            
        except Exception as e:
            print(f"❌ Intent extraction failed: {e}")
            # Return minimal valid intent
            return {
                "occasion": "casual",
                "style": "casual",
                "gender": "unisex",
                "primary_color": None,
                "secondary_colors": [],
                "budget_tier": "mid_range",
                "season": "all",
                "specific_requirements": {},
                "mentioned_brands": [],
                "query_summary": query.message[:100]
            }
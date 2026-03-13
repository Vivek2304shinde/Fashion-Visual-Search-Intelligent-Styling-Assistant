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
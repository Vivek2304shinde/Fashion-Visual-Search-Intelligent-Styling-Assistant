"""
Reasoning Agent: Explains why the outfit works.
Uses prompt engineering - no complex parsing functions.
"""

import os
from typing import Dict, List, Any
from openai import OpenAI
from groq import Groq
from ai_stylist.schemas import Product
from config import config

class ReasoningAgent:
    """
    Agent responsible for explaining styling decisions.
    Pure prompt engineering - no vague helper functions.
    """
    
    def __init__(self):
        self.client = Groq( api_key = os.getenv("OPENAI_API_KEY"),
                                base_url = os.getenv("OPENAI_BASE_URL"))
        
        self.REASONING_PROMPT = """You are an expert fashion stylist explaining an outfit to a client.

USER'S REQUEST: {user_query}
OCCASION: {occasion}
STYLE: {style}

SELECTED ITEMS:
{selected_items}

VALIDATION RESULTS:
- Score: {validation_score}/100
- Issues: {validation_issues}
- Warnings: {validation_warnings}

Write a warm, expert explanation covering:
1. Overall impression (2-3 sentences)
2. Why the colors work together
3. How the style fits the occasion
4. 3 specific styling tips
5. Alternative suggestions if any item isn't available

Make it conversational and helpful. Use fashion terms but explain them.
"""

    async def generate_reasoning(
        self,
        user_query: str,
        intent: Dict[str, Any],
        products: Dict[str, List[Product]],
        validation: Dict[str, Any]
    ) -> str:
        """
        Generate natural language reasoning for the outfit.
        Returns a complete explanation string.
        """
        
        try:
            # Prepare selected items summary
            selected_summary = []
            for category, items in products.items():
                if items and len(items) > 0:
                    top = items[0]
                    selected_summary.append(
                        f"• {category.title()}: {top.brand} {top.product_name[:50]}"
                    )
            
            selected_text = "\n".join(selected_summary) if selected_summary else "No items selected"
            
            # Prepare validation summary
            issues = validation.get('issues', [])
            warnings = validation.get('warnings', [])
            
            issues_text = ", ".join(issues) if issues else "None"
            warnings_text = ", ".join(warnings) if warnings else "None"
            
            # Call LLM
            response = self.client.chat.completions.create(
                model=config.LLM_MODEL,
                temperature=0.7,
                messages=[
                    {"role": "system", "content": "You are an expert fashion stylist providing outfit advice."},
                    {"role": "user", "content": self.REASONING_PROMPT.format(
                        user_query=user_query,
                        occasion=intent.get("occasion", "casual"),
                        style=intent.get("style", "casual"),
                        selected_items=selected_text,
                        validation_score=validation.get("score", 0),
                        validation_issues=issues_text,
                        validation_warnings=warnings_text
                    )}
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ Reasoning generation failed: {e}")
            return self._get_fallback_reasoning(products)
    
    def _get_fallback_reasoning(self, products: Dict[str, List[Product]]) -> str:
        """Fallback reasoning when LLM fails"""
        
        item_count = sum(len(items) for items in products.values())
        
        if item_count == 0:
            return "I couldn't find products matching your request. Try being more specific about what you're looking for."
        
        categories = list(products.keys())
        
        return f"""I've put together an outfit with {item_count} items for you.

The {', '.join(categories)} work well together for a cohesive look. 

Styling tips:
• Make sure everything fits well - alterations can make a big difference
• Pay attention to fabric care instructions
• Consider the weather when wearing this outfit
• Accessorize to add personal flair

If any item isn't available, look for similar pieces in the same color family."""
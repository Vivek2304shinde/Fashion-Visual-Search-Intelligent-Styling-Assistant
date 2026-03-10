"""
Fixed Conversation Manager - With STRICT extraction rules
"""

import json
import os
import re
from typing import Dict, Any, List
from groq import Groq

class ConversationManagerFixed:
    """
    Conversation manager with strict intent extraction rules.
    MUST extract gender, occasion, and other preferences.
    """
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL", "https://api.groq.com")
        
        print(f"🔧 ConversationManagerFixed initializing...")
        print(f"   API Key set: {'Yes' if api_key else 'No'}")
        
        self.client = Groq(api_key=api_key, base_url=base_url)
        self.model = "llama-3.3-70b-versatile"
        
        # Test client
        try:
            test_response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Say OK"}],
                max_tokens=5
            )
            print(f"✅ Groq test passed")
        except Exception as e:
            print(f"❌ Groq test failed: {e}")
        
        # STRICT PROMPT with required fields
        self.SYSTEM_PROMPT = """You are a friendly, warm AI fashion stylist. Your job is to have a natural conversation while EXTRACTING specific information.

CRITICAL - YOU MUST EXTRACT THESE FIELDS (in order of priority):
1. gender (male/female/unisex) - This is MANDATORY. If not mentioned, ask for it.
2. occasion (wedding/party/office/casual/etc.) - This is MANDATORY.
3. style_preference (formal/casual/traditional/etc.)
4. color_preference (any specific colors mentioned)
5. budget_tier (budget/mid_range/premium/luxury based on clues or amounts)
6. season (summer/winter/spring/fall/monsoon)
7. specific_preferences - Capture ANY specific details like:
   - Fit preferences (baggy, slim, regular, oversized)
   - Specific items (jeans, shirt, dress, etc.)
   - Fabric preferences (cotton, linen, silk)
   - Any other specific requirements

CONVERSATION RULES:
- Be friendly and use emojis! 😊
- If gender is not mentioned in first message, politely ask for it
- If occasion is not mentioned, ask about it
- Don't ask all questions at once - make it natural
- When you have gender + occasion + at least 2 other details, set ready_for_recommendations to true

Current collected info: {collected_info}
User message: {message}

Respond in this EXACT JSON format:
{
    "response": "your friendly message here with emojis ✨",
    "extracted_info": {
        "gender": null,
        "occasion": null,
        "style_preference": null,
        "color_preference": null,
        "budget_tier": null,
        "season": null,
        "specific_preferences": {}
    },
    "ready_for_recommendations": false
}

Return ONLY valid JSON, no other text."""
    
    def _extract_json(self, text: str) -> Dict:
        """Extract JSON from text, handling various formats"""
        # Try to parse directly
        try:
            return json.loads(text)
        except:
            pass
        
        # Try to find JSON between curly braces
        try:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except:
            pass
        
        # Default fallback
        return {
            "response": "Tell me more about what you're looking for! 😊",
            "extracted_info": {},
            "ready_for_recommendations": False
        }
    
    def process_message(self, message: str, context: Dict) -> Dict:
        try:
            collected = context.get("collected_info", {})
            
            # Format collected info
            collected_json = json.dumps(collected)
            
            # Build prompt
            prompt = self.SYSTEM_PROMPT.replace("__COLLECTED_INFO__", collected_json)
            prompt = prompt.replace("__MESSAGE__", message)
            
            print(f"\n📤 Sending to Groq: {message[:50]}...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a JSON-only fashion assistant. Always respond with valid JSON. You MUST extract gender and occasion."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            text = response.choices[0].message.content
            print(f"📥 Raw: {text[:100]}...")
            
            # Clean the response
            text = text.strip()
            if text.startswith('```json'):
                text = text[7:]
            elif text.startswith('```'):
                text = text[3:]
            if text.endswith('```'):
                text = text[:-3]
            text = text.strip()
            
            # Extract JSON
            try:
                result = json.loads(text)
            except json.JSONDecodeError:
                match = re.search(r'\{.*\}', text, re.DOTALL)
                if match:
                    result = json.loads(match.group())
                else:
                    result = {
                        "response": text[:200] if text else "Tell me more!",
                        "extracted_info": {},
                        "ready_for_recommendations": False
                    }
            
            # Ensure result is a dictionary
            if not isinstance(result, dict):
                result = {
                    "response": str(result),
                    "extracted_info": {},
                    "ready_for_recommendations": False
                }
            
            # Ensure required keys
            if "response" not in result:
                result["response"] = "Thanks for sharing! Tell me more."
            if "extracted_info" not in result:
                result["extracted_info"] = {}
            if "ready_for_recommendations" not in result:
                result["ready_for_recommendations"] = False
            
            # Update collected info
            extracted = result.get("extracted_info", {})
            for k, v in extracted.items():
                if v and v != "null" and v not in [None, "", "None"]:
                    if k == "specific_preferences" and isinstance(v, dict):
                        if "specific_preferences" not in collected:
                            collected["specific_preferences"] = {}
                        collected["specific_preferences"].update(v)
                    elif v:
                        collected[k] = v
            
            # Check if we have minimum required fields
            has_gender = collected.get("gender") not in [None, "null", ""]
            has_occasion = collected.get("occasion") not in [None, "null", ""]
            other_details = sum(1 for k in ["style_preference", "color_preference", "budget_tier", "season"] 
                              if collected.get(k) not in [None, "null", ""])
            
            ready = has_gender and has_occasion and other_details >= 2
            
            return {
                "response": result["response"],
                "updated_context": {"collected_info": collected},
                "ready_for_recommendation": ready,
                "extracted_info": extracted
            }
            
        except Exception as e:
            print(f"❌ Error in process_message: {e}")
            import traceback
            traceback.print_exc()
            return {
                "response": "I'm here to help! What kind of outfit are you looking for? 😊",
                "updated_context": context,
                "ready_for_recommendation": False,
                "extracted_info": {}
            }
"""
Fixed Conversation Manager - With DEBUGGING
"""

import json
import os
import re
import traceback
from typing import Dict, Any, List
from groq import Groq

class ConversationManagerFixed:
    """
    Conversation manager with proper context handling.
    Maintains conversation history and extracts information progressively.
    """
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL", "https://api.groq.com/openai/v1")
        
        print("\n" + "="*60)
        print("🔧 ConversationManagerFixed INITIALIZING...")
        print("="*60)
        print(f"   API Key: {api_key[:10]}...{api_key[-5:] if len(api_key) > 15 else 'too short'}")
        print(f"   Base URL: {base_url}")
        
        # Initialize client
        try:
            self.client = Groq(api_key=api_key)
            self.model = "llama-3.3-70b-versatile"
            print(f"✅ Client initialized with model: {self.model}")
        except Exception as e:
            print(f"❌ Client initialization failed: {e}")
            traceback.print_exc()
            self.client = None
        
        # Test client if initialized
        if self.client:
            try:
                print("\n🔍 Testing Groq connection...")
                test_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": "Say 'OK' in one word"}],
                    max_tokens=5,
                    temperature=0
                )
                test_result = test_response.choices[0].message.content
                print(f"✅ Groq test passed: '{test_result}'")
            except Exception as e:
                print(f"❌ Groq test failed: {e}")
                traceback.print_exc()
                self.client = None
        
        print("="*60 + "\n")
        
        # Enhanced system prompt
        self.SYSTEM_PROMPT = """You are a friendly, warm AI fashion stylist. Your job is to have a natural conversation while EXTRACTING specific information.

IMPORTANT RULES:
1. Track what information you've already collected - don't ask for it again
2. Ask natural follow-up questions based on previous answers
3. Be warm and use emojis! 😊
4. When you have enough info, suggest moving to recommendations

Information to collect (in priority order):
1. gender (male/female/unisex) - Ask if not provided
2. occasion (wedding/party/office/casual/etc.) - Ask if not provided
3. style_preference (formal/casual/traditional/trendy etc.)
4. color_preference (specific colors or color families)
5. budget_tier (budget/mid_range/premium/luxury)
6. season (summer/winter/spring/fall/monsoon)
7. specific_preferences (fit, fabric, specific items, etc.)

CURRENT CONVERSATION HISTORY:
{conversation_history}

CURRENT COLLECTED INFO:
{collected_info}

LATEST USER MESSAGE: {message}

Respond in this EXACT JSON format:
{
    "response": "your friendly, contextual message here with emojis ✨",
    "extracted_info": {
        "gender": null or extracted value,
        "occasion": null or extracted value,
        "style_preference": null or extracted value,
        "color_preference": null or extracted value,
        "budget_tier": null or extracted value,
        "season": null or extracted value,
        "specific_preferences": {} or extracted details
    },
    "ready_for_recommendations": false/true
}

EXTRACTION RULES:
- Only extract information that's explicitly mentioned in the conversation
- For gender: look for words like male, female, man, woman, boy, girl, unisex
- For occasion: look for words like wedding, party, office, work, casual, date, etc.
- For budget: look for price mentions, budget constraints, or luxury indicators
- If information is already collected, don't extract it again (keep existing value)

Return ONLY valid JSON, no other text."""
    
    def _extract_json(self, text: str) -> Dict:
        """Extract JSON from text, handling various formats"""
        print(f"\n🔍 Extracting JSON from: '{text[:100]}...'")
        
        # Clean the text first
        text = text.strip()
        
        # Remove markdown code blocks
        if text.startswith('```json'):
            text = text[7:]
        elif text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        text = text.strip()
        
        # Try to parse directly
        try:
            result = json.loads(text)
            print(f"✅ Direct JSON parse successful")
            return result
        except json.JSONDecodeError as e:
            print(f"⚠️ Direct JSON parse failed: {e}")
            pass
        
        # Try to find JSON between curly braces
        try:
            match = re.search(r'\{[\s\S]*\}', text)
            if match:
                json_str = match.group()
                result = json.loads(json_str)
                print(f"✅ Extracted JSON from braces")
                return result
        except Exception as e:
            print(f"⚠️ Brace extraction failed: {e}")
            pass
        
        # Default fallback
        print(f"⚠️ Using fallback response")
        return {
            "response": "Tell me more about what you're looking for! 😊",
            "extracted_info": {},
            "ready_for_recommendations": False
        }
    
    def _format_conversation_history(self, messages: List[Dict]) -> str:
        """Format conversation history for the prompt"""
        if not messages:
            return "No previous messages."
        
        history = []
        for msg in messages[-5:]:  # Keep last 5 messages for context
            role = "User" if msg["role"] == "user" else "Assistant"
            history.append(f"{role}: {msg['content']}")
        
        return "\n".join(history)
    
    def process_message(self, message: str, context: Dict) -> Dict:
        print("\n" + "="*60)
        print("📤 PROCESSING MESSAGE")
        print("="*60)
        print(f"Message: '{message}'")
        print(f"Context keys: {list(context.keys())}")
        
        try:
            # Get conversation history from context or initialize empty
            conversation_history = context.get("conversation_history", [])
            collected = context.get("collected_info", {})
            
            print(f"\n📊 Current collected info: {json.dumps(collected, indent=2)}")
            print(f"📜 Conversation history length: {len(conversation_history)}")
            
            # Check if client exists
            if not self.client:
                print("❌ Groq client not initialized!")
                return {
                    "response": "I'm here to help! What kind of outfit are you looking for? 😊",
                    "updated_context": context,
                    "ready_for_recommendation": False,
                    "extracted_info": {}
                }
            
            # Format conversation history
            history_str = self._format_conversation_history(conversation_history)
            
            # Format collected info
            collected_json = json.dumps(collected, indent=2)
            
            # Build prompt with all context
            prompt = self.SYSTEM_PROMPT.replace("{conversation_history}", history_str)
            prompt = prompt.replace("{collected_info}", collected_json)
            prompt = prompt.replace("{message}", message)
            
            print(f"\n🤖 Sending to Groq...")
            print(f"   Model: {self.model}")
            print(f"   Prompt length: {len(prompt)} chars")
            
            # Call Groq
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a JSON-only fashion assistant. Always respond with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                
                raw_response = response.choices[0].message.content
                print(f"\n📥 Raw response received:")
                print(f"   Length: {len(raw_response)} chars")
                print(f"   Preview: {raw_response[:200]}...")
                
            except Exception as e:
                print(f"❌ Groq API call failed: {e}")
                traceback.print_exc()
                return {
                    "response": "I'm here to help! Tell me more about what you're looking for. 😊",
                    "updated_context": context,
                    "ready_for_recommendation": False,
                    "extracted_info": {}
                }
            
            # Extract JSON from response
            result = self._extract_json(raw_response)
            print(f"\n✅ Parsed result:")
            print(f"   Response: {result.get('response', 'N/A')[:100]}...")
            print(f"   Extracted: {json.dumps(result.get('extracted_info', {}))}")
            print(f"   Ready: {result.get('ready_for_recommendations', False)}")
            
            # Update conversation history
            if "conversation_history" not in context:
                context["conversation_history"] = []
            
            # Add current messages to history
            context["conversation_history"].append({"role": "user", "content": message})
            context["conversation_history"].append({"role": "assistant", "content": result.get("response", "")})
            
            # Update collected info
            extracted = result.get("extracted_info", {})
            updated_collected = collected.copy()
            
            for key, value in extracted.items():
                if value and value not in [None, "null", "", "None"]:
                    if key == "specific_preferences" and isinstance(value, dict):
                        if "specific_preferences" not in updated_collected:
                            updated_collected["specific_preferences"] = {}
                        updated_collected["specific_preferences"].update(value)
                    elif value:  # Only update if value is not empty
                        updated_collected[key] = value
                        print(f"   ✅ Updated {key}: {value}")
            
            # Check if we have minimum required fields
            has_gender = updated_collected.get("gender") not in [None, "null", ""]
            has_occasion = updated_collected.get("occasion") not in [None, "null", ""]
            
            # Count other fields
            other_fields = [k for k in ["style_preference", "color_preference", "budget_tier", "season"] 
                          if updated_collected.get(k) not in [None, "null", ""]]
            
            # Add specific_preferences if it has content
            if updated_collected.get("specific_preferences") and len(updated_collected["specific_preferences"]) > 0:
                other_fields.append("specific_preferences")
            
            ready = has_gender and has_occasion and len(other_fields) >= 1
            
            print(f"\n📊 Update summary:")
            print(f"   - Has gender: {has_gender} ({updated_collected.get('gender', 'None')})")
            print(f"   - Has occasion: {has_occasion} ({updated_collected.get('occasion', 'None')})")
            print(f"   - Other fields: {other_fields}")
            print(f"   - Ready for recommendations: {ready}")
            
            return {
                "response": result.get("response", "Tell me more about what you're looking for! 😊"),
                "updated_context": {
                    "collected_info": updated_collected,
                    "conversation_history": context["conversation_history"]
                },
                "ready_for_recommendation": ready,
                "extracted_info": extracted
            }
            
        except Exception as e:
            print(f"\n❌ UNEXPECTED ERROR in process_message:")
            print(f"   Error: {e}")
            traceback.print_exc()
            
            return {
                "response": "I'm here to help! What kind of outfit are you looking for? 😊",
                "updated_context": context,
                "ready_for_recommendation": False,
                "extracted_info": {}
            }
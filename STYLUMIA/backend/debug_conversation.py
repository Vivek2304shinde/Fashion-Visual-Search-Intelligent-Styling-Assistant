# debug_conversation.py
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

load_dotenv()

print("✅ Config loaded:")
print(f"   - Using API URL: {os.getenv('OPENAI_BASE_URL', 'https://api.groq.com')}")
print(f"   - Model: llama-3.3-70b-versatile")
print(f"   - API Key set: {bool(os.getenv('OPENAI_API_KEY'))}")

from ai_stylist.agents.conversation_manager_fixed import ConversationManagerFixed

def generate_search_queries(self, outfit_plan, gender):
    """Step 3: Generate REAL search queries for scraper"""
    self.print_section("STEP 3: SEARCH QUERIES FOR SCRAPER (REAL)")
    
    # PASS THE ACTUAL GENDER FROM COLLECTED INFO
    search_queries = self.stylist_agent.extract_categories_for_scraping(outfit_plan, gender)
    
    print("🔍 QUERIES BY CATEGORY:")
    for category, queries in search_queries.items():
        print(f"\n  {category.upper()}:")
        for q in queries:
            print(f"    • {q}")
    
    return search_queries

def test_conversation():
    """Test the conversation manager"""
    
    print("="*60)
    print("🧪 TESTING CONVERSATION MANAGER")
    print("="*60)
    
    # Initialize
    manager = ConversationManagerFixed()
    
    # Test messages
    test_messages = [
        "Hi, I need help finding an outfit",
        "I'm looking for something for a wedding",
        "I'm male and I prefer traditional style",
        "My budget is around 20000",
        "I like blue colors"
    ]
    
    context = {"collected_info": {}}
    
    for i, msg in enumerate(test_messages, 1):
        print(f"\n--- Test {i} ---")
        print(f"👤 User: {msg}")
        
        result = manager.process_message(msg, context)
        context = result["updated_context"]
        
        print(f"🤖 Assistant: {result['response']}")
        print(f"📊 Collected: {context['collected_info']}")
        print(f"✅ Ready for recommendations: {result['ready_for_recommendation']}")
        
        if result['ready_for_recommendation']:
            print("🎯 READY FOR RECOMMENDATIONS!")
            break
    
    print("\n" + "="*60)
    print("✅ Test complete")
    print("="*60)

if __name__ == "__main__":
    test_conversation()
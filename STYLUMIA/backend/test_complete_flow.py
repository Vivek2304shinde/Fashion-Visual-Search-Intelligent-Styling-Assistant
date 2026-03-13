"""
COMPLETE REAL FLOW DEBUG - Tests actual API calls with real data
Run this to see the entire pipeline with REAL products from scraper
"""

import os
import sys
import json
import asyncio
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

# Add backend to path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

load_dotenv()

print("="*80)
print("🔥 COMPLETE REAL FLOW DEBUG - NO MOCK DATA")
print("="*80)
print(f"✅ API URL: {os.getenv('OPENAI_BASE_URL', 'https://api.groq.com')}")
print(f"✅ Model: llama-3.3-70b-versatile")
print(f"✅ API Key: {'✓ Set' if os.getenv('GROQ_API_KEY') else '✗ Missing'}")
print("="*80)

# Import agents
from ai_stylist.agents.conversation_manager_fixed import ConversationManagerFixed
from ai_stylist.agents.stylist_agent import StylistAgent
from ai_stylist.schemas import Product
from scraper import MyntraScraper

class RealFlowDebugger:
    """Debug the entire flow with REAL API calls"""
    
    def __init__(self):
        self.conversation_manager = ConversationManagerFixed()
        self.stylist_agent = StylistAgent()
        self.scraper = MyntraScraper()
        self.session_context = {"collected_info": {}}
        self.session_id = f"debug_{int(time.time())}"
        
    def print_section(self, title):
        """Print a formatted section header"""
        print("\n" + "="*80)
        print(f"📌 {title}")
        print("="*80)
    
    def print_json(self, data, label=""):
        """Pretty print JSON data"""
        if label:
            print(f"\n{label}:")
        print(json.dumps(data, indent=2, default=str))
    
    async def run_conversation(self, messages):
        """Step 1: Run REAL conversation and extract intent"""
        self.print_section("STEP 1: CONVERSATION MANAGER (REAL)")
        
        for i, msg in enumerate(messages, 1):
            print(f"\n--- Message {i} ---")
            print(f"👤 USER: {msg}")
            
            result = self.conversation_manager.process_message(msg, self.session_context)
            self.session_context = result["updated_context"]
            
            print(f"🤖 AI: {result['response']}")
            print(f"📊 EXTRACTED: {json.dumps(result['extracted_info'], indent=2)}")
            print(f"📦 COLLECTED SO FAR: {json.dumps(self.session_context['collected_info'], indent=2)}")
            
            if result['ready_for_recommendation']:
                print("\n✨ READY FOR RECOMMENDATIONS!")
                break
        
        return self.session_context['collected_info']
    
    async def run_stylist(self, collected_info):
        """Step 2: Get REAL outfit plan from stylist"""
        self.print_section("STEP 2: STYLIST AGENT (REAL)")
        
        print("📥 INPUT TO STYLIST:")
        self.print_json(collected_info)
        
        outfit_plan = await self.stylist_agent.create_outfit_plan(collected_info)
        
        print("\n📤 OUTFIT PLAN FROM STYLIST:")
        self.print_json(outfit_plan)
        
        return outfit_plan
    
    def generate_search_queries(self, outfit_plan, gender):
        """Step 3: Generate REAL search queries for scraper"""
        self.print_section("STEP 3: SEARCH QUERIES FOR SCRAPER (REAL)")
        
        search_queries = self.stylist_agent.extract_categories_for_scraping(outfit_plan, gender)
        
        print("🔍 QUERIES BY CATEGORY:")
        for category, queries in search_queries.items():
            print(f"\n  {category.upper()}:")
            for q in queries:
                print(f"    • {q}")
        
        return search_queries
    
    def run_scraper_sync(self, query, max_results=5):
        """Synchronous wrapper for scraper"""
        try:
            print(f"\n🔍 Scraping: {query}")
            results = self.scraper.search_products(query, max_results)
            return results if results else []
        except Exception as e:
            print(f"❌ Scraper error for {query}: {e}")
            return []
    
    async def scrape_real_products(self, search_queries):
        """Step 4: Run REAL scraper to get actual products"""
        self.print_section("STEP 4: SCRAPER RESULTS (REAL PRODUCTS)")
        
        all_products = {}
        total_products = 0
        
        for category, queries in search_queries.items():
            print(f"\n📦 SCRAPING CATEGORY: {category}")
            print("-" * 40)
            
            category_products = []
            
            for query in queries[:2]:  # Use first 2 queries per category
                # Run scraper
                loop = asyncio.get_event_loop()
                products = await loop.run_in_executor(
                    None,
                    self.run_scraper_sync,
                    query,
                    5
                )
                
                if products:
                    for p in products:
                        # Convert to Product object for consistency
                        product = Product(
                            product_id=p.get("product_id", f"{category}_{abs(hash(str(p.get('product_url', ''))))}"),
                            brand=p.get("brand", "Unknown"),
                            product_name=p.get("product_name", ""),
                            price=float(p.get("price", 0)),
                            original_price=float(p.get("original_price", 0)) if p.get("original_price") else None,
                            discount=p.get("discount", ""),
                            image_url=p.get("image_url", ""),
                            product_url=p.get("product_url", ""),
                            source="myntra",
                            category=category,
                            scraped_at=int(time.time()),
                            match_score=85
                        )
                        category_products.append(product)
                    
                    print(f"  ✓ Found {len(products)} products for query: {query}")
                    
                    # Show first product details
                    if products and len(products) > 0:
                        first = products[0]
                        print(f"    Example: {first.get('brand', 'N/A')} - {first.get('product_name', 'N/A')[:50]}...")
                        print(f"    Price: ₹{first.get('price', 0)}")
                        print(f"    🖼️  Image: {first.get('image_url', 'N/A')}")
                        print(f"    🔗 URL: {first.get('product_url', 'N/A')}")
            
            if category_products:
                all_products[category] = category_products[:5]  # Keep top 5
                total_products += len(category_products[:5])
                print(f"\n  ✅ Total for {category}: {len(category_products[:5])} products")
            else:
                all_products[category] = []
                print(f"  ❌ No products found for {category}")
        
        print(f"\n📊 TOTAL REAL PRODUCTS FOUND: {total_products}")
        return all_products, total_products
    
    def display_products_for_frontend(self, products):
        """Format products exactly as they would be sent to frontend"""
        self.print_section("STEP 5: FRONTEND PAYLOAD (REAL DATA)")
        
        formatted_products = {}
        
        for category, items in products.items():
            formatted_products[category] = []
            if items:
                for item in items[:3]:  # Show top 3 per category
                    if hasattr(item, 'dict'):
                        product_dict = item.dict()
                    else:
                        product_dict = item
                    
                    formatted = {
                        "id": product_dict.get("product_id", ""),
                        "brand": product_dict.get("brand", "Unknown"),
                        "name": product_dict.get("product_name", ""),
                        "price": float(product_dict.get("price", 0)),
                        "original_price": float(product_dict.get("original_price", 0)) if product_dict.get("original_price") else None,
                        "discount": product_dict.get("discount", ""),
                        "image_url": product_dict.get("image_url", ""),
                        "product_url": product_dict.get("product_url", ""),
                        "source": product_dict.get("source", "myntra"),
                        "category": category,
                        "match_score": product_dict.get("match_score", 85)
                    }
                    formatted_products[category].append(formatted)
        
        # Print the exact JSON that would go to frontend
        print("\n📦 FRONTEND PRODUCTS PAYLOAD:")
        for category, items in formatted_products.items():
            print(f"\n{category.upper()} ({len(items)} items):")
            for item in items:
                print(f"\n  📍 {item['brand']} - {item['name']}")
                print(f"     💰 ₹{item['price']}")
                if item['original_price']:
                    print(f"     🏷️  Was: ₹{item['original_price']}")
                print(f"     🖼️  {item['image_url']}")
                print(f"     🔗 {item['product_url']}")
        
        return formatted_products
    
    async def debug_real_flow(self, test_scenario):
        """Run complete debug flow with REAL data"""
        
        print("\n" + "🔥"*40)
        print(f"🔥 TEST SCENARIO: {test_scenario['name']}")
        print(f"🔥 Gender: {test_scenario.get('gender', 'not specified')}")
        print("🔥"*40)
        
        # Step 1: REAL Conversation
        collected = await self.run_conversation(test_scenario['messages'])
        
        # If gender not extracted, use from scenario
        if 'gender' not in collected and test_scenario.get('gender'):
            collected['gender'] = test_scenario['gender']
        
        # Step 2: REAL Stylist
        outfit_plan = await self.run_stylist(collected)
        
        # Step 3: REAL Search Queries
        gender = collected.get('gender', 'male')
        search_queries = self.generate_search_queries(outfit_plan, gender)
        
        # Step 4: REAL Scraper Results
        products, total = await self.scrape_real_products(search_queries)
        
        # Step 5: Format for Frontend
        frontend_products = self.display_products_for_frontend(products)
        
        # Summary
        self.print_section("📊 FLOW SUMMARY")
        print(f"✅ Session ID: {self.session_id}")
        print(f"✅ Messages processed: {len(test_scenario['messages'])}")
        print(f"✅ Intent extracted: {len(collected)} fields")
        print(f"✅ Outfit items planned: {len(outfit_plan.get('outfit_plan', {}))}")
        print(f"✅ Search queries generated: {sum(len(q) for q in search_queries.values())}")
        print(f"✅ REAL products found: {total}")
        
        return {
            "session_id": self.session_id,
            "collected_info": collected,
            "outfit_plan": outfit_plan,
            "search_queries": search_queries,
            "products": frontend_products,
            "total_products": total
        }

async def main():
    """Run multiple REAL test scenarios"""
    
    # Test Scenario 1: MALE - Party with Baggy Jeans
    debugger1 = RealFlowDebugger()
    scenario1 = {
        "name": "👨 MALE - Party Outfit with Baggy Jeans",
        "gender": "male",
        "messages": [
            "I need baggy jeans for a party",
            "I like light blue color",
            "My budget is around ₹3000",
            "It's for a casual party with friends"
        ]
    }
    
    print("\n" + "🚀"*40)
    print("🚀 RUNNING SCENARIO 1: MALE PARTY OUTFIT")
    print("🚀"*40)
    result1 = await debugger1.debug_real_flow(scenario1)
    
    # Test Scenario 2: FEMALE - Wedding Guest
    debugger2 = RealFlowDebugger()
    scenario2 = {
        "name": "👩 FEMALE - Wedding Guest",
        "gender": "female",
        "messages": [
            "I need an outfit for a wedding",
            "I prefer maroon color",
            "My budget is around ₹15000"
        ]
    }
    
    print("\n" + "🚀"*40)
    print("🚀 RUNNING SCENARIO 2: FEMALE WEDDING GUEST")
    print("🚀"*40)
    result2 = await debugger2.debug_real_flow(scenario2)
    
    print("\n" + "✨"*40)
    print("✨ DEBUG COMPLETE - ALL REAL DATA")
    print("✨"*40)
    print(f"\n✅ Scenario 1: {result1['total_products']} real products found")
    print(f"✅ Scenario 2: {result2['total_products']} real products found")

if __name__ == "__main__":
    asyncio.run(main())
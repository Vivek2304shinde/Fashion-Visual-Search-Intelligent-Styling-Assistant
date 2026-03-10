"""
Orchestrator: Coordinates all agents to fulfill user requests.
Now properly integrated with ConversationManager.
"""

import time
import asyncio
from typing import Dict, Any

from ai_stylist.schemas import UserQuery
from ai_stylist.agents.conversation_manager_fixed import ConversationManagerFixed
from ai_stylist.agents.stylist_agent import StylistAgent
from ai_stylist.agents.retrieval_agent import RetrievalAgent

class Orchestrator:
    """
    Main orchestrator that coordinates all agents.
    Now using ConversationManager for natural chat and StylistAgent for outfit planning.
    """
    
    def __init__(self):
        # Use the new agents
        self.conversation_manager = ConversationManagerFixed()
        self.stylist_agent = StylistAgent()
        self.retrieval_agent = RetrievalAgent()
        
        # Keep track of active conversations
        self.active_sessions = {}
    
    async def process_query(self, query: UserQuery, session_id: str = None) -> Dict[str, Any]:
        """
        Process a user query through the entire pipeline.
        If session_id is provided, continues existing conversation.
        """
        start_time = time.time()
        
        print(f"\n🎯 Processing: {query.message}")
        
        try:
            # If no session_id, this is a direct query without conversation context
            # We'll use the stylist agent directly
            if not session_id:
                print("🤔 Direct query - using stylist agent...")
                
                # Create a simple intent from the query
                intent = {
                    "message": query.message,
                    "occasion": query.occasion.value if query.occasion else "casual",
                    "gender": query.context.gender if query.context else "unisex",
                    "budget_tier": query.context.typical_budget if query.context else "mid_range"
                }
                
                # Get outfit plan from stylist
                outfit_plan = await self.stylist_agent.create_outfit_plan(intent)
                
                # Extract search queries
                search_queries = self.stylist_agent.extract_categories_for_scraping(outfit_plan)
                
                # Retrieve products
                print("🔍 Retrieving products...")
                products = {}
                for category, queries in search_queries.items():
                    # Use retrieval agent to get products
                    category_products = await self.retrieval_agent.search_products(
                        queries[0],  # Use first query
                        max_results=5
                    )
                    if category_products:
                        products[category] = category_products
                
                processing_time = time.time() - start_time
                
                return {
                    "success": True,
                    "query": query.message,
                    "outfit_plan": outfit_plan.get("outfit_plan", {}),
                    "styling_advice": outfit_plan.get("styling_advice", ""),
                    "products_found": {k: len(v) for k, v in products.items()},
                    "products": products,
                    "processing_time": processing_time
                }
            
            # If we have a session_id, this is part of an ongoing conversation
            # This would be called from your conversation endpoints
            else:
                # Get session context
                session_context = self.active_sessions.get(session_id, {})
                
                # Process through conversation manager
                result = self.conversation_manager.process_message(
                    query.message, 
                    session_context
                )
                
                # Update session
                self.active_sessions[session_id] = result["updated_context"]
                
                # If ready for recommendations, generate outfit plan
                if result["ready_for_recommendation"]:
                    collected_info = result["updated_context"].get("collected_info", {})
                    
                    # Get outfit plan from stylist
                    outfit_plan = await self.stylist_agent.create_outfit_plan(collected_info)
                    
                    # Extract search queries
                    search_queries = self.stylist_agent.extract_categories_for_scraping(outfit_plan)
                    
                    # Retrieve products
                    print("🔍 Retrieving products...")
                    products = {}
                    for category, queries in search_queries.items():
                        category_products = await self.retrieval_agent.search_products(
                            queries[0],  # Use first query
                            max_results=5
                        )
                        if category_products:
                            products[category] = category_products
                    
                    result["outfit_plan"] = outfit_plan.get("outfit_plan", {})
                    result["styling_advice"] = outfit_plan.get("styling_advice", "")
                    result["products"] = products
                
                processing_time = time.time() - start_time
                result["processing_time"] = processing_time
                
                return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"❌ Pipeline error: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                "success": False,
                "query": query.message,
                "error": str(e),
                "processing_time": processing_time
            }
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
import re
import pandas as pd
import os
import sys
import logging
from datetime import datetime
import traceback
import asyncio
from typing import Dict, Any, Optional, List
import json
import uuid
from pydantic import BaseModel, Field
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# =========================
# LOGGING
# =========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =========================
# LOAD PRODUCT DATA (FOR METADATA)
# =========================
def load_product_data():
    csv_path = r"C:\Users\Dell\Downloads\Stylumia\Fashion-Visual-Search-Intelligent-Styling-Assistant\STYLUMIA\data\dresses_bd_processed_data.csv"
    
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding='latin1')
        
    return df

product_df = load_product_data()
print(f"✅ Loaded {len(product_df)} products from CSV")

# =========================
# PATH SETUP
# =========================
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# =========================
# IMPORTS
# =========================
# CLIP and FAISS imports for image search (ADD THESE BACK)
from scripts.clip_embeddings import get_embedding
from scripts.faiss_search import EmbeddingSimilaritySearch

# Your existing scraper
from scraper import MyntraScraper

# AI Stylist imports
from ai_stylist.orchestrator import Orchestrator
from ai_stylist.schemas import UserQuery, UserContext, Product  # ADD Product here
from ai_stylist.config.categories import OUTFIT_CATEGORIES, get_all_categories

# =========================
# FASTAPI INIT
# =========================
app = FastAPI(
    title="Stylumia AI Fashion Assistant",
    description="AI-powered fashion styling with visual search and intelligent recommendations",
    version="2.0.0"
)

# =========================
# CORS CONFIGURATION
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("CORS middleware configured")

# =========================
# INITIALIZE COMPONENTS
# =========================
# Initialize FAISS search engine for image search (ADD THIS)
faiss_index_path = r"C:\Users\Dell\Downloads\Stylumia\Fashion-Visual-Search-Intelligent-Styling-Assistant\STYLUMIA\faiss_index"
try:
    search_engine = EmbeddingSimilaritySearch(faiss_index_path)
    logger.info(f"✅ FAISS Index Loaded from {faiss_index_path}")
except Exception as e:
    logger.error(f"❌ Failed to load FAISS index: {e}")
    search_engine = None

# Initialize scrapers
myntra_scraper = MyntraScraper()

# Initialize AI Stylist Orchestrator
ai_stylist = Orchestrator()
logger.info("✅ AI Stylist Orchestrator initialized")

# Initialize OpenAI/Groq client
openai_client = Groq(api_key=os.getenv("OPENAI_API_KEY"),
                       base_url=os.getenv("OPENAI_BASE_URL"))

# Initialize the ultimate stylist
from ai_stylist.agents.stylist_agent import StylistAgent
stylist_agent = StylistAgent()

# =========================
# LOAD PRODUCT METADATA FOR VISUAL SEARCH
# =========================
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, "..", "data", "dresses_bd_processed_data.csv")

if os.path.exists(data_path):
    products_df = pd.read_csv(data_path).set_index('product_id')
    logger.info(f"✅ Loaded {len(products_df)} products for visual search")
else:
    products_df = pd.DataFrame()
    logger.warning("⚠️ Product data file not found")

# =========================
# CHAT HISTORY MANAGEMENT
# =========================
class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)

class ChatSession(BaseModel):
    session_id: str
    messages: List[ChatMessage] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

# In-memory chat storage
chat_sessions: Dict[str, ChatSession] = {}

# =========================
# CONVERSATION MANAGER
# =========================
from ai_stylist.agents.conversation_manager_fixed import ConversationManagerFixed
conversation_manager = ConversationManagerFixed()

# =========================
# HEALTH CHECK ENDPOINT
# =========================
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "ai_stylist": "active",
            "visual_search": "active" if len(products_df) > 0 and search_engine else "limited",
            "web_scraper": "active",
            "faiss_index": "loaded" if search_engine else "not loaded"
        },
        "stats": {
            "products_in_db": len(products_df),
            "categories_available": len(get_all_categories())
        }
    }

# =========================
# MAIN IMAGE SEARCH ENDPOINT (FROM YOUR OLD WORKING CODE)
# =========================
@app.post("/search")
async def search_by_image(file: UploadFile = File(...), top_k: int = 30):
    """
    Image search endpoint using CLIP and FAISS
    """
    logger.info("=== NEW SEARCH REQUEST ===")
    logger.info(f"File received: {file.filename}")
    
    try:
        # Check if FAISS is loaded
        if not search_engine:
            raise HTTPException(500, "FAISS index not loaded")

        # Validate image
        if not file.content_type.startswith("image/"):
            raise HTTPException(400, "Only image files allowed")

        # Process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # Generate embedding
        embedding = get_embedding(image)
        
        if embedding is None:
            raise HTTPException(500, "Failed to generate image embedding")
        
        # Search FAISS
        similar_product_ids = search_engine.search(embedding, top_k=top_k)
        
        # Prepare response
        results = []
        for product_id in similar_product_ids:
            if product_id not in products_df.index:
                continue
                
            product_data = products_df.loc[product_id].to_dict()
            
            results.append({
                "product_id": product_id,
                "product_name": product_data.get("product_name", "Unknown"),
                "brand": product_data.get("brand", "Unknown"),
                "price": product_data.get("selling_price", 0),
                "image_url": product_data.get("feature_image_s3", ""),
            })
        
        return {
            "success": True,
            "results": results,
            "total_found": len(results),
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Search failed: {e}")
        traceback.print_exc()
        raise HTTPException(500, f"Search failed: {str(e)}")

# =========================
# LEGACY IMAGE SEARCH ENDPOINT
# =========================
@app.post("/search/image")
async def search_by_image_legacy(
    file: UploadFile = File(...),
    top_k: int = Form(30)
):
    """Legacy endpoint - uses the main search"""
    return await search_by_image(file, top_k)

# =========================
# TEXT SEARCH ENDPOINT
# =========================
@app.post("/search/text")
async def search_by_text(query_data: Dict[str, Any]):
    try:
        query = query_data.get("query", "")
        top_k = int(query_data.get("top_k", 30))
        
        if not query:
            raise HTTPException(400, "Query is required")
        
        logger.info(f"🔍 Text search: '{query}'")
        
        results = myntra_scraper.search_products(query, top_k)
        
        validated_results = []
        for product in results:
            validated_results.append({
                "product_id": str(product.get("product_id", "")),
                "product_name": str(product.get("product_name", "")),
                "brand": str(product.get("brand", "")),
                "price": float(product.get("price", 0)),
                "image_url": str(product.get("image_url", "")),
                "product_url": str(product.get("product_url", "")),
                "source": "myntra"
            })

        return {
            "success": True,
            "query": query,
            "results": validated_results,
            "total_found": len(validated_results),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Text search failed: {e}")
        raise HTTPException(500, str(e))

# =========================
# AI STYLIST - CHAT ENDPOINT
# =========================
@app.post("/api/stylist/chat")
async def stylist_chat(request: Dict[str, Any]):
    try:
        message = request.get("message", "")
        if not message:
            raise HTTPException(400, "Message is required")
        
        logger.info(f"💬 AI Stylist request: '{message[:50]}...'")
        
        context = None
        if any([
            request.get("gender"),
            request.get("age_group"),
            request.get("body_type"),
            request.get("skin_tone"),
            request.get("preferred_brands"),
            request.get("avoided_brands")
        ]):
            context = UserContext(
                gender=request.get("gender", "unisex"),
                age_group=request.get("age_group", "adult"),
                body_type=request.get("body_type"),
                skin_tone=request.get("skin_tone"),
                preferred_brands=request.get("preferred_brands", []),
                avoided_brands=request.get("avoided_brands", []),
                typical_budget=request.get("budget_tier", "mid_range")
            )
        
        user_query = UserQuery(
            message=message,
            context=context,
            occasion=request.get("occasion"),
            season=request.get("season"),
            budget_total=request.get("budget")
        )
        
        response = await ai_stylist.process_query(user_query)
        
        if hasattr(response, 'dict'):
            response_dict = response.dict()
        else:
            response_dict = response
        
        return {
            "success": True,
            "data": response_dict
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ AI Stylist error: {e}")
        traceback.print_exc()
        raise HTTPException(500, f"AI Stylist error: {str(e)}")

# =========================
# QUICK SUGGEST ENDPOINT
# =========================
@app.post("/api/stylist/suggest")
async def quick_suggest(request: Dict[str, Any]):
    try:
        occasion = request.get("occasion")
        if not occasion:
            raise HTTPException(400, "Occasion is required")
        
        query = f"I need an outfit for a {occasion}"
        if request.get("style"):
            query += f" with {request.get('style')} style"
        
        chat_request = {
            "message": query,
            "gender": request.get("gender", "unisex"),
            "budget_tier": request.get("budget", "mid_range")
        }
        
        return await stylist_chat(chat_request)
        
    except Exception as e:
        logger.error(f"❌ Quick suggest error: {e}")
        raise HTTPException(500, str(e))

# =========================
# GET CATEGORIES
# =========================
@app.get("/api/stylist/categories")
async def get_stylist_categories():
    try:
        categories = get_all_categories()
        return {
            "success": True,
            "categories": categories,
            "total_count": len(categories)
        }
    except Exception as e:
        logger.error(f"❌ Failed to get categories: {e}")
        raise HTTPException(500, str(e))

# =========================
# GET STYLING TIPS
# =========================
@app.get("/api/stylist/tips/{occasion}")
async def get_styling_tips(occasion: str):
    try:
        # Simple tips based on occasion
        tips = {
            "wedding": [
                "Avoid wearing white or black",
                "Consider the venue and time",
                "Comfortable footwear is essential"
            ],
            "office": [
                "Stick to neutral colors",
                "Ensure clothes are well-ironed",
                "Keep accessories minimal"
            ],
            "party": [
                "Don't be afraid to experiment",
                "Statement accessories work well",
                "Comfort is key"
            ]
        }
        
        occasion_tips = tips.get(occasion.lower(), [
            "Dress appropriately for the occasion",
            "Choose colors that complement you",
            "Ensure proper fit"
        ])
        
        return {
            "success": True,
            "occasion": occasion,
            "styling_tips": occasion_tips
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get tips: {e}")
        raise HTTPException(500, str(e))

# =========================
# FEEDBACK ENDPOINT
# =========================
@app.post("/api/stylist/feedback")
async def submit_feedback(feedback: Dict[str, Any]):
    try:
        logger.info(f"📝 Feedback received: {feedback}")
        return {
            "success": True,
            "message": "Thank you for your feedback!",
            "feedback_id": datetime.now().timestamp()
        }
    except Exception as e:
        logger.error(f"❌ Failed to submit feedback: {e}")
        raise HTTPException(500, str(e))

# =========================
# CONVERSATION START
# =========================
@app.post("/api/stylist/conversation/start")
async def start_conversation(request: Dict[str, Any]):
    try:
        session_id = str(uuid.uuid4())
        initial_message = request.get("initial_message", "Hello, I need styling help")
        
        session = ChatSession(
            session_id=session_id,
            messages=[ChatMessage(role="user", content=initial_message)],
            context={
                "gender": request.get("gender"),
                "age_group": request.get("age_group"),
                "occasion": request.get("occasion"),
                "conversation_state": "GREETING",
                "collected_info": {}
            }
        )
        
        result = conversation_manager.process_message(initial_message, session.context)
        session.context = result["updated_context"]
        session.messages.append(ChatMessage(role="assistant", content=result["response"]))
        
        chat_sessions[session_id] = session
        
        return {
            "success": True,
            "session_id": session_id,
            "message": result["response"],
            "ready_for_recommendation": result["ready_for_recommendation"]
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to start conversation: {e}")
        traceback.print_exc()
        raise HTTPException(500, str(e))

# =========================
# CONTINUE CONVERSATION
# =========================
@app.post("/api/stylist/conversation/{session_id}/chat")
async def continue_conversation(session_id: str, request: Dict[str, Any]):
    try:
        if session_id not in chat_sessions:
            raise HTTPException(404, f"Session {session_id} not found")
        
        message = request.get("message")
        if not message:
            raise HTTPException(400, "Message is required")
        
        session = chat_sessions[session_id]
        session.messages.append(ChatMessage(role="user", content=message))
        
        result = conversation_manager.process_message(message, session.context)
        session.context = result["updated_context"]
        session.messages.append(ChatMessage(role="assistant", content=result["response"]))
        session.updated_at = datetime.now()
        
        return {
            "success": True,
            "session_id": session_id,
            "message": result["response"],
            "collected_info": session.context.get("collected_info", {}),
            "ready_for_recommendation": result["ready_for_recommendation"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Conversation error: {e}")
        traceback.print_exc()
        raise HTTPException(500, str(e))

# =========================
# GET RECOMMENDATIONS
# =========================
@app.post("/api/stylist/conversation/{session_id}/recommend")
async def get_intelligent_recommendations(session_id: str):
    try:
        if session_id not in chat_sessions:
            raise HTTPException(404, f"Session {session_id} not found")
            
        session = chat_sessions[session_id]
        collected_info = session.context.get("collected_info", {})
        
        # Get outfit plan
        outfit_plan = await stylist_agent.create_outfit_plan(collected_info)
        
        # Extract search queries
        search_queries = stylist_agent.extract_categories_for_scraping(outfit_plan)
        
        # Store in session
        session.context["outfit_plan"] = outfit_plan
        
        return {
            "success": True,
            "outfit_plan": outfit_plan.get("outfit_plan", {}),
            "styling_advice": outfit_plan.get("styling_advice", "")
        }
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        traceback.print_exc()
        raise HTTPException(500, str(e))

# =========================
# ERROR HANDLERS
# =========================
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "Endpoint not found",
            "path": str(request.url)
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc) if os.getenv("DEBUG") else "An error occurred"
        }
    )

# =========================
# ROOT ENDPOINT
# =========================
@app.get("/")
async def root():
    return {
        "name": "Stylumia AI Fashion Assistant API",
        "version": "2.0.0",
        "endpoints": {
            "health": "GET /health",
            "image_search": "POST /search",
            "text_search": "POST /search/text",
            "ai_stylist": {
                "chat": "POST /api/stylist/chat",
                "conversation": {
                    "start": "POST /api/stylist/conversation/start",
                    "chat": "POST /api/stylist/conversation/{session_id}/chat",
                    "recommend": "POST /api/stylist/conversation/{session_id}/recommend"
                }
            }
        },
        "documentation": "/docs"
    }

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 STYLUMIA AI FASHION ASSISTANT")
    print("="*60)
    print(f"📊 Products in database: {len(products_df)}")
    print(f"👔 Categories available: {len(get_all_categories())}")
    print(f"🔍 FAISS Index: {'✅ Loaded' if search_engine else '❌ Not Loaded'}")
    print(f"🤖 AI Stylist: Active")
    print(f"💬 Conversational API: Active")
    print("\n📡 Server running on http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("="*60 + "\n")
    
    uvicorn.run(
        "alternative_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
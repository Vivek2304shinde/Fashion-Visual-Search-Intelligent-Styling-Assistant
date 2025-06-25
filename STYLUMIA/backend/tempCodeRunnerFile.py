from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from PIL import Image
import io
import pandas as pd
import os
import sys
import logging
from datetime import datetime
import traceback
import asyncio
from pydantic import BaseModel 
from typing import Dict, Any 

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'


# Add after your other initializations
def load_product_data():
    csv_path = r"C:\Users\ANAND\Downloads\STYLUMIA\Fashion-Visual-Search-Intelligent-Styling-Assistant\STYLUMIA\data\dresses_bd_processed_data.csv"
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding='latin1')
    return df


# Load data once at startup
product_df = load_product_data()
print(f"Loaded {len(product_df)} products from CSV")


# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import your existing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.clip_embeddings import get_embedding
from scripts.faiss_search import EmbeddingSimilaritySearch
from scraper import MyntraScraper

app = FastAPI()

search_engine = EmbeddingSimilaritySearch(r"C:\Users\ANAND\Downloads\STYLUMIA\Fashion-Visual-Search-Intelligent-Styling-Assistant\STYLUMIA\faiss_index")

# CORS Setup - Enhanced for debugging
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,  # Added for better CORS support
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("CORS middleware configured")


# Load product metadata with corrected path handling
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, "..", "data", "dresses_bd_processed_data.csv")
logger.info(f"Loading product data from: {data_path}")

try:
    products_df = pd.read_csv(data_path).set_index('product_id')
    logger.info(f"Product data loaded successfully. Shape: {products_df.shape}")
    logger.info(f"Sample product IDs: {list(products_df.index[:5])}")
except Exception as e:
    logger.error(f"Failed to load product data: {e}")
    raise

# DEBUG: Add a simple health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint to verify backend is running"""
    logger.info("Health check requested")
    return JSONResponse({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "Stylumia backend is running"
    })

@app.post("/search")
async def search_by_image(file: UploadFile = File(...), top_k: int = 30):
    """
    Endpoint flow:
    1. Receive image upload
    2. Generate embedding using clip.py
    3. Search FAISS index via search_faiss.py
    4. Enrich results with product data
    """
    # DEBUG: Log request details
    logger.info("=== NEW SEARCH REQUEST ===")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info(f"File received: {file.filename}")
    logger.info(f"File content type: {file.content_type}")
    logger.info(f"File size: {file.size if hasattr(file, 'size') else 'unknown'}")
    logger.info(f"Top K requested: {top_k}")
    
    try:
        # 1. Validate input
        logger.info("Step 1: Validating input...")
        if not file.content_type.startswith("image/"):
            logger.error(f"Invalid file type: {file.content_type}")
            raise HTTPException(400, "Only image files allowed")
        logger.info("✓ File type validation passed")

        # 2. Process image
        logger.info("Step 2: Processing image...")
        contents = await file.read()
        logger.info(f"✓ File read successfully. Size: {len(contents)} bytes")
        
        image = Image.open(io.BytesIO(contents))
        logger.info(f"✓ PIL Image created successfully. Size: {image.size}, Mode: {image.mode}")
        
        # 3. Get embedding (from your clip.py)
        logger.info("Step 3: Generating embedding...")
        embedding = get_embedding(image)
        logger.info(f"✓ Embedding generated. Shape: {embedding.shape if embedding is not None else 'None'}")
        
        if embedding is None:
            logger.error("Embedding generation failed")
            raise HTTPException(500, "Failed to generate image embedding")
        
        # 4. Search FAISS (from your search_faiss.py)
        logger.info("Step 4: Searching FAISS index...")
        similar_product_ids = search_engine.search(embedding, top_k=30)
        logger.info(f"✓ FAISS search completed. Found {len(similar_product_ids)} results")
        logger.info(f"Similar product IDs: {similar_product_ids}")
        
        # 5. Prepare response
        logger.info("Step 5: Preparing response...")
        results = []
        for i, product_id in enumerate(similar_product_ids):
            logger.info(f"Processing result {i+1}: {product_id}")
            
            if product_id not in products_df.index:
                logger.warning(f"Product ID {product_id} not found in metadata")
                continue
                
            product_data = products_df.loc[product_id].to_dict()
            s3_url = product_data['feature_image_s3'] 
            logger.info(f"📷 Product {product_id} S3 URL: {s3_url}")  # Fixed: moved outside dict

            
            result = {
                "product_id": product_id,
                "product_name": product_data.get("product_name"),
                "brand": product_data.get("brand"),
                "price": product_data.get("selling_price"),
                "image_url": s3_url,  # Direct S3 URL
            }
            results.append(result)
            print(f"📷 Product: {product_id}, S3 URL: {s3_url}")
            logger.info(f"✓ Added result: {product_data.get('product_name', 'Unknown')}")
        
        logger.info(f"✓ Response prepared with {len(results)} results")
        
        response = {
            "success": True,
            "results": results,
            "total_found": len(results),
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info("=== SEARCH REQUEST COMPLETED SUCCESSFULLY ===")
        return JSONResponse(response)

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"=== SEARCH REQUEST FAILED ===")
        logger.error(f"Error: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(500, f"Search failed: {str(e)}")


@app.post("/search/text")
async def search_by_text(query_data: Dict[str, Any]):
    """
    Complete text search endpoint with Myntra scraping
    Accepts: {"query": "search term", "top_k": 30}
    Returns: List of products with complete details
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Validate input exists and is a dictionary
        if not isinstance(query_data, dict):
            raise HTTPException(
                status_code=422,
                detail="Request body must be a JSON object"
            )

        # Extract and validate query
        query = query_data.get("query", "").strip()
        if not query:
            raise HTTPException(
                status_code=400,
                detail="Search query cannot be empty"
            )

        # Extract and validate top_k
        try:
            top_k = int(query_data.get("top_k", 30))
            if not (1 <= top_k <= 100):
                raise ValueError("top_k must be between 1 and 100")
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

        # Execute search
        scraper = MyntraScraper()
        try:
            results = await asyncio.wait_for(
                asyncio.to_thread(scraper.search_products, query, top_k),
                timeout=60.0
            )
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=504,
                detail="Search operation timed out"
            )

        # Validate and format results
        validated_results = []
        for product in results:
            if not all(k in product for k in ['product_id', 'product_name', 'price']):
                continue
                
            validated_results.append({
                "product_id": str(product["product_id"]),
                "product_name": str(product["product_name"]),
                "brand": str(product.get("brand", "")),
                "price": float(product["price"]),
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

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server on http://0.0.0.0:8000")
    logger.info("API endpoints available:")
    logger.info("  - GET  /health - Health check")
    logger.info("  - POST /search - Image search")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
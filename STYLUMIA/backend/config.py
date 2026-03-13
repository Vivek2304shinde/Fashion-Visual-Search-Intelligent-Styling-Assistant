"""
Configuration settings for the application
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")  
    
    # LLM Settings
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")  # Will be overridden by .env
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    
    # Scraping Settings
    MAX_PRODUCTS_PER_CATEGORY = int(os.getenv("MAX_PRODUCTS_PER_CATEGORY", "10"))
    SCRAPING_TIMEOUT = int(os.getenv("SCRAPING_TIMEOUT", "30"))
    MAX_CONCURRENT_SCRAPERS = int(os.getenv("MAX_CONCURRENT_SCRAPERS", "5"))
    
    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
    
    # Cache Settings
    CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour
    
    # Debug
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

config = Config()

# Add this debug print to verify configuration
print(f"✅ Config loaded:")
print(f"   - Using API URL: {config.OPENAI_BASE_URL or 'https://api.openai.com/v1 (default)'}")
print(f"   - Model: {config.LLM_MODEL}")
print(f"   - API Key set: {bool(config.GROQ_API_KEY)}")
"""
Retrieval Agent: Handles product scraping for all categories.
Uses category config for search terms.
"""

import asyncio
import time
import random
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor

from scraper import MyntraScraper
from ai_stylist.schemas import Product, ScrapingTask, CategorySpec
from ai_stylist.config.categories import (
    OUTFIT_CATEGORIES, get_category_search_terms, get_category_display_name
)

class RetrievalAgent:
    """
    Single agent that handles retrieval for ALL categories.
    Uses configuration to generate appropriate search queries.
    """
    
    def __init__(self, max_workers: int = 5):
        self.scraper = MyntraScraper()
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        
        # Popular colors to try if none specified
        self.POPULAR_COLORS = [
            "black", "navy", "blue", "white", "grey", "brown", 
            "beige", "maroon", "green", "red"
        ]
    
    async def retrieve(
        self,
        categories: Dict[str, CategorySpec],
        gender: str = "unisex",
        max_results_per_category: int = 10
    ) -> Dict[str, List[Product]]:
        """
        Retrieve products for multiple categories in parallel.
        """
        # Create tasks for each category
        tasks = []
        for category, spec in categories.items():
            # Generate search queries for this category
            search_queries = self._generate_search_queries(category, spec, gender)
            
            task = ScrapingTask(
                category=category,
                search_query=search_queries[0] if search_queries else category,
                max_results=max_results_per_category,
                spec=spec
            )
            tasks.append(task)
        
        # Run retrievals in parallel
        results = await asyncio.gather(*[
            self._retrieve_single_category(task) for task in tasks
        ], return_exceptions=True)
        
        # Organize results
        products_by_category = {}
        for task, result in zip(tasks, results):
            if isinstance(result, Exception):
                print(f"❌ Failed to retrieve {task.category}: {result}")
                products_by_category[task.category] = []
            else:
                products_by_category[task.category] = result
        
        return products_by_category
    
    async def _retrieve_single_category(self, task: ScrapingTask) -> List[Product]:
        """
        Retrieve products for a single category with multiple query attempts.
        """
        all_products = []
        search_queries = self._generate_search_queries(
            task.category, task.spec, "men women"
        )
        
        print(f"🔍 Retrieving {task.category}...")
        
        for query_idx, query in enumerate(search_queries[:5]):  # Max 5 queries
            try:
                # Random delay between queries
                if query_idx > 0:
                    await asyncio.sleep(random.uniform(1, 2))
                
                # Run scraper
                products = await self._run_scraper(query, task.max_results * 2)
                
                if products:
                    # Convert to Product objects
                    converted = self._convert_to_products(products, task.category)
                    
                    # Score and filter
                    scored = self._score_products(converted, task)
                    
                    all_products.extend(scored)
                    
                    print(f"  ✓ Found {len(scored)} for '{query[:40]}...'")
                    
                    # Stop if we have enough good products
                    high_quality = [p for p in all_products if p.match_score > 70]
                    if len(high_quality) >= task.max_results:
                        break
                        
            except Exception as e:
                print(f"  ✗ Query failed: {e}")
                continue
        
        # Deduplicate and sort
        all_products = self._deduplicate(all_products)
        all_products.sort(key=lambda x: x.match_score, reverse=True)
        
        return all_products[:task.max_results]
    
    def _generate_search_queries(
        self,
        category: str,
        spec: Optional[CategorySpec],
        gender: str
    ) -> List[str]:
        """
        Generate multiple search queries for a category.
        """
        queries = []
        
        # Get base search terms from config
        base_terms = get_category_search_terms(category)
        
        # Colors to try
        colors = []
        if spec and spec.color:
            color_str = spec.color.replace('_', ' ') if isinstance(spec.color, str) else spec.color
            colors.append(color_str)
        colors.extend(self.POPULAR_COLORS[:3])
        colors = list(set(colors))  # Remove duplicates
        
        # Generate queries
        for term in base_terms[:2]:  # Use top 2 search terms
            # Basic query
            queries.append(f"{term} {gender}")
            
            # With colors
            for color in colors[:2]:
                queries.append(f"{color} {term} {gender}")
        
        # Remove duplicates
        seen = set()
        unique_queries = []
        for q in queries:
            if q not in seen:
                seen.add(q)
                unique_queries.append(q)
        
        return unique_queries[:8]  # Max 8 queries
    
    async def _run_scraper(self, query: str, max_results: int) -> List[Dict]:
        """Run scraper in thread pool"""
        loop = asyncio.get_event_loop()
        try:
            products = await loop.run_in_executor(
                self.executor,
                self.scraper.search_products,
                query,
                max_results
            )
            return products if products else []
        except Exception as e:
            print(f"Scraper error: {e}")
            return []
    
    def _convert_to_products(self, raw_products: List[Dict], category: str) -> List[Product]:
        """Convert raw products to Product objects"""
        products = []
        
        for p in raw_products:
            try:
                # Generate unique ID
                product_id = p.get('product_id', '')
                if not product_id and p.get('product_url'):
                    product_id = f"{category}_{abs(hash(p['product_url']))}"
                
                product = Product(
                    product_id=product_id,
                    brand=p.get('brand', '').strip(),
                    product_name=p.get('product_name', '').strip(),
                    price=p.get('price', 0),
                    original_price=p.get('original_price', 0),
                    discount=p.get('discount', ''),
                    image_url=p.get('image_url', ''),
                    product_url=p.get('product_url', ''),
                    source="myntra",
                    category=category,
                    scraped_at=int(time.time()),
                    match_score=0.0,
                    match_reasons=[]
                )
                
                # Only keep if has essential fields
                if product.product_name and product.image_url and product.price > 0:
                    products.append(product)
                    
            except Exception as e:
                continue
                
        return products
    
    def _score_products(self, products: List[Product], task: ScrapingTask) -> List[Product]:
        """Score products based on relevance to task"""
        
        for product in products:
            score = 50
            reasons = []
            
            # Brand score
            if product.brand and len(product.brand) > 2:
                score += 10
                reasons.append("Known brand")
            
            # Price reasonability
            if 500 < product.price < 10000:
                score += 10
                reasons.append("Good price range")
            
            # Has discount
            if product.discount:
                score += 5
                reasons.append("Discounted")
            
            # Image quality
            if product.image_url and 'placeholder' not in product.image_url:
                score += 5
            
            # Match with spec if available
            if task.spec:
                # Color match
                if task.spec.color:
                    color_str = str(task.spec.color).replace('_', ' ')
                    if color_str.lower() in product.product_name.lower():
                        score += 15
                        reasons.append("Color match")
            
            product.match_score = min(100, score)
            product.match_reasons = reasons[:3]
        
        return products
    
    def _deduplicate(self, products: List[Product]) -> List[Product]:
        """Remove duplicate products"""
        seen = set()
        unique = []
        
        for p in products:
            key = f"{p.product_url}_{p.price}"
            if key not in seen:
                seen.add(key)
                unique.append(p)
        
        return unique
    
    def __del__(self):
        """Cleanup executor"""
        self.executor.shutdown(wait=False)
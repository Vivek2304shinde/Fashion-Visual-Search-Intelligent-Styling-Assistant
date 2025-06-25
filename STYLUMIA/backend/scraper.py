import re
import time
import json
from fastapi import HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class MyntraScraper:
    def __init__(self):
        self.driver = self._setup_driver()
        
    def _setup_driver(self):
        """Configure headless Chrome browser"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        return webdriver.Chrome(options=chrome_options)

    def search_products(self, query: str, max_results: int = 30):
        """Search Myntra and scrape product results"""
        try:
            search_url = f"https://www.myntra.com/{query.replace(' ', '-')}"
            print(f"🔍 Searching Myntra: {search_url}")
            self.driver.get(search_url)
            
            # Wait for results to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.product-base"))
            )
            
            # Scroll to load all products
            self._scroll_page()
            
            # Get all product elements
            products = self.driver.find_elements(By.CSS_SELECTOR, "li.product-base")[:max_results]
            results = []
            
            print(f"📦 Found {len(products)} products, extracting data...")
            
            for idx, product in enumerate(products):
                try:
                    product_data = self._extract_product_data(product)
                    if product_data:
                        results.append(product_data)
                        print(f"✓ Extracted product {idx + 1}: {product_data['name']}")
                except Exception as e:
                    print(f"❌ Failed to extract product {idx + 1}: {e}")
                    continue
                
                if len(results) >= max_results:
                    break
            
            print(f"🎉 Successfully scraped {len(results)} products")
            return results
            
        except Exception as e:
            print(f"❌ Scraping failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")
        finally:
            self.driver.quit()

    def _scroll_page(self):
        """Scroll page to load all products"""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_scrolls = 5
        
        while scroll_attempts < max_scrolls:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scroll_attempts += 1

    def _extract_product_data(self, product):
        """Extract product details from HTML element"""
        try:
            brand = product.find_element(By.CSS_SELECTOR, "h3.product-brand").text.strip()
            name = product.find_element(By.CSS_SELECTOR, "h4.product-product").text.strip()
            
            # Price extraction
            price_element = product.find_element(By.CSS_SELECTOR, "div.product-price")
            price_text = price_element.text.strip()
            selling_price = self._extract_price(price_text)
            
            # Image URL
            img_element = product.find_element(By.CSS_SELECTOR, "img.img-responsive")
            img_url = img_element.get_attribute("src") or img_element.get_attribute("data-src")
            
            # Product URL
            product_url = product.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            if product_url and not product_url.startswith("http"):
                product_url = f"https://www.myntra.com{product_url}"
            
            return {
                "product_id": f"myntra_{hash(product_url)}",  # Generate unique ID
                "brand": brand,
                "product_name": name,  # Changed from 'name' to match your interface
                "price": selling_price,
                "image_url": img_url,  # Changed from 'imageUrl' to match your interface
                "product_url": product_url,
                "source": "myntra"
            }
        except Exception as e:
            print(f"Error extracting product: {e}")
            return None

    def _extract_price(self, price_text):
        """Extract numeric price from text"""
        price_match = re.search(r'Rs\.\s*(\d+[\d,]*)', price_text)
        if price_match:
            return int(price_match.group(1).replace(',', ''))
        return 0
import re
import time
import random
import json
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSessionIdException

class MyntraScraper:
    def __init__(self):
        self.driver = None
        self._setup_driver()
        
    def _setup_driver(self):
        """Configure headless Chrome browser with anti-detection measures"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
                
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                window.navigator.chrome = { runtime: {} };
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
            """
        })
        
        return self.driver

    def search_products(self, query: str, max_results: int = 30) -> List[Dict]:
        """Search Myntra and scrape product results"""
        try:
            # Ensure driver is alive
            if not self.driver:
                self._setup_driver()
                
            search_url = f"https://www.myntra.com/{query.replace(' ', '-')}"
            print(f"🔍 Searching Myntra: {search_url}")
            
            time.sleep(random.uniform(2, 4))
            self.driver.get(search_url)
            
            # Verify the URL actually contains the expected query (small delay)
            time.sleep(2)
            current_url = self.driver.current_url
            if query.replace(' ', '-') not in current_url and query.replace(' ', '%20') not in current_url:
                print(f"⚠️ URL mismatch: expected '{query}' but got '{current_url}'. Retrying...")
                self.driver.get(search_url)
                time.sleep(2)
            
            # Check for bot detection
            if self._check_for_bot_detection():
                print("⚠️ Bot detection triggered, retrying with new driver...")
                self._setup_driver()
                time.sleep(random.uniform(3, 5))
                self.driver.get(search_url)
            
            # Wait for results
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.product-base"))
            )
            
            self._scroll_page()
            
            products = self.driver.find_elements(By.CSS_SELECTOR, "li.product-base")[:max_results * 2]
            
            results = []
            print(f"📦 Found {len(products)} raw products, extracting data...")
            
            for idx, product in enumerate(products):
                try:
                    product_data = self._extract_product_data(product)
                    if product_data and product_data.get('product_name') and product_data.get('price', 0) > 0:
                        results.append(product_data)
                        print(f"✓ Extracted: {product_data['brand']} - {product_data['product_name'][:30]}... - ₹{product_data['price']}")
                    
                    time.sleep(random.uniform(0.2, 0.4))
                    
                    if len(results) >= max_results:
                        break
                except Exception as e:
                    continue
            
            print(f"🎉 Successfully scraped {len(results)} products")
            return results
            
        except InvalidSessionIdException:
            print("❌ Session invalid, recreating driver...")
            self._setup_driver()
            return self.search_products(query, max_results)  # retry once
        except TimeoutException:
            print(f"❌ Timeout for query: {query}")
            return []
        except Exception as e:
            print(f"❌ Scraping failed: {str(e)}")
            return []
    
    def _scroll_page(self) -> None:
        try:
            scroll_pause_time = random.uniform(1.5, 2.5)
            scroll_height = 0
            max_scrolls = 12
            scroll_attempts = 0
            
            while scroll_attempts < max_scrolls:
                increment = random.randint(400, 900)
                scroll_height += increment
                self.driver.execute_script(f"window.scrollTo({{top: {scroll_height}, behavior: 'smooth'}});")
                
                time.sleep(scroll_pause_time + random.uniform(-0.5, 0.5))
                
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if scroll_height >= new_height - 500:
                    break
                
                scroll_attempts += 1
        except:
            pass

    def _extract_product_data(self, product) -> Optional[Dict]:
        try:
            brand_elem = product.find_element(By.CSS_SELECTOR, "h3.product-brand")
            brand = brand_elem.text.strip() if brand_elem else ""
            
            name_elem = product.find_element(By.CSS_SELECTOR, "h4.product-product")
            name = name_elem.text.strip() if name_elem else ""
            
            price_elem = product.find_element(By.CSS_SELECTOR, "div.product-price")
            price_text = price_elem.text.strip() if price_elem else ""
            price_match = re.search(r'Rs\.?\s*([\d,]+)', price_text, re.IGNORECASE)
            price = int(price_match.group(1).replace(',', '')) if price_match else 0
            
            img_elem = product.find_element(By.CSS_SELECTOR, "img.img-responsive")
            img_url = img_elem.get_attribute("src") or img_elem.get_attribute("data-src") or ""
            
            link_elem = product.find_element(By.CSS_SELECTOR, "a")
            product_url = link_elem.get_attribute("href") if link_elem else ""
            
            discount_elem = product.find_elements(By.CSS_SELECTOR, ".product-discountPercentage")
            discount = discount_elem[0].text.strip() if discount_elem else ""
            
            return {
                "product_id": f"myntra_{abs(hash(product_url))}",
                "brand": brand,
                "product_name": name,
                "price": price,
                "original_price": price,
                "discount": discount,
                "image_url": img_url,
                "product_url": product_url,
                "source": "myntra",
                "scraped_at": int(time.time())
            }
        except:
            return None

    def _check_for_bot_detection(self) -> bool:
        try:
            captcha_selectors = [".captcha-container", "#captcha", ".recaptcha"]
            for selector in captcha_selectors:
                if len(self.driver.find_elements(By.CSS_SELECTOR, selector)) > 0:
                    return True
            
            blocked_texts = ["access denied", "bot detected", "security check"]
            page_text = self.driver.page_source.lower()
            if any(text in page_text for text in blocked_texts):
                return True
                
            return False
        except:
            return False

    def close(self):
        """Explicitly close the driver"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None

    def __del__(self):
        self.close()
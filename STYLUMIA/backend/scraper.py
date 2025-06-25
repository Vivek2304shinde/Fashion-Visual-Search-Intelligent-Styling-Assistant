import re
import time
import random
import json
from typing import List, Dict, Optional
from fastapi import HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class MyntraScraper:
    def __init__(self):
        self.driver = self._setup_driver()
        
    def _setup_driver(self) -> webdriver.Chrome:
        """Configure headless Chrome browser with anti-detection measures"""
        chrome_options = Options()
        
        # New headless mode is less detectable
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Realistic user agent and window size
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        
        # Disable automation flags
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Mask selenium detection
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
                window.navigator.chrome = {
                    runtime: {},
                };
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
            """
        })
        
        return driver

    def search_products(self, query: str, max_results: int = 30) -> List[Dict]:
        """Search Myntra and scrape product results"""
        try:
            search_url = f"https://www.myntra.com/{query.replace(' ', '-')}"
            print(f"🔍 Searching Myntra: {search_url}")
            
            # Add random delay before request
            time.sleep(random.uniform(1, 3))
            self.driver.get(search_url)
            
            # Check for bot detection
            if self._check_for_bot_detection():
                raise HTTPException(status_code=403, detail="Bot detection triggered")
            
            # Wait for results to load with more specific selector
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.product-base h4.product-product"))
            )
            
            # Improved scrolling to load more products
            self._scroll_page()
            
            # Get all product elements
            products = self.driver.find_elements(By.CSS_SELECTOR, "li.product-base")[:max_results * 2]  # Get extra in case some fail
            
            results = []
            print(f"📦 Found {len(products)} raw products, extracting data...")
            
            for idx, product in enumerate(products):
                try:
                    product_data = self._extract_product_data(product)
                    if product_data:
                        results.append(product_data)
                        print(f"✓ Extracted product {idx + 1}: {product_data['product_name']}")
                    
                    # Random delay between product extractions
                    time.sleep(random.uniform(0.1, 0.5))
                    
                    if len(results) >= max_results:
                        break
                except Exception as e:
                    print(f"❌ Failed to extract product {idx + 1}: {e}")
                    continue
            
            print(f"🎉 Successfully scraped {len(results)} products")
            return results
            
        except TimeoutException:
            error_msg = "Timeout waiting for Myntra products to load"
            print(f"❌ {error_msg}")
            raise HTTPException(status_code=504, detail=error_msg)
        except Exception as e:
            print(f"❌ Scraping failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")
        finally:
            self.driver.quit()

    def _scroll_page(self) -> None:
        """Improved scrolling to trigger lazy loading"""
        scroll_pause_time = random.uniform(1, 2)  # Random pause between scrolls
        scroll_height = 0
        max_scrolls = 15
        scroll_attempts = 0
        
        while scroll_attempts < max_scrolls:
            # Scroll in increments to appear more human-like
            increment = random.randint(300, 800)
            scroll_height += increment
            self.driver.execute_script(f"window.scrollTo(0, {scroll_height});")
            
            # Random wait with some variation
            time.sleep(scroll_pause_time + random.uniform(-0.5, 0.5))
            
            # Check if we've reached the bottom
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if scroll_height >= new_height:
                break
            
            scroll_attempts += 1
            
            # Occasionally scroll back up a bit to mimic human behavior
            if scroll_attempts % 5 == 0:
                self.driver.execute_script(f"window.scrollBy(0, -{random.randint(100, 300)});")
                time.sleep(random.uniform(0.5, 1.5))

    def _extract_product_data(self, product) -> Optional[Dict]:
        """Robust product data extraction with fallback selectors"""
        try:
            brand = self._safe_find_text(product, ["h3.product-brand", ".product-brand"])
            name = self._safe_find_text(product, ["h4.product-product", ".product-product"])
            
            # Price extraction with multiple fallbacks
            price_element = self._safe_find(product, [
                "div.product-price", 
                ".product-price",
                "span[data-selenium='product-price']"
            ])
            price_text = price_element.text.strip() if price_element else ""
            selling_price = self._extract_price(price_text)
            
            # Image URL with multiple fallbacks
            img_element = self._safe_find(product, [
                "img.img-responsive", 
                "img[data-selenium='product-image']",
                "img"
            ])
            img_url = ""
            if img_element:
                img_url = (img_element.get_attribute("src") or 
                         img_element.get_attribute("data-src") or 
                         img_element.get_attribute("data-image"))
            
            # Product URL
            link_element = self._safe_find(product, ["a"])
            product_url = link_element.get_attribute("href") if link_element else ""
            if product_url and not product_url.startswith("http"):
                product_url = f"https://www.myntra.com{product_url}"
            
            # Discount (if available)
            discount_element = self._safe_find(product, [".product-discountPercentage"])
            discount = discount_element.text.strip() if discount_element else ""
            
            return {
                "product_id": f"myntra_{abs(hash(product_url))}",
                "brand": brand,
                "product_name": name,
                "price": selling_price,
                "original_price": self._extract_original_price(product),
                "discount": discount,
                "image_url": img_url,
                "product_url": product_url,
                "source": "myntra",
                "scraped_at": int(time.time())
            }
        except Exception as e:
            print(f"Error extracting product: {e}")
            return None

    def _safe_find(self, element, selectors: List[str]):
        """Try multiple selectors until one works"""
        for selector in selectors:
            try:
                found = element.find_element(By.CSS_SELECTOR, selector)
                if found:
                    return found
            except NoSuchElementException:
                continue
        return None

    def _safe_find_text(self, element, selectors: List[str]) -> str:
        """Safe text extraction with fallback selectors"""
        found = self._safe_find(element, selectors)
        return found.text.strip() if found else ""

    def _extract_price(self, price_text: str) -> int:
        """Extract numeric price from text with multiple format support"""
        price_match = re.search(r'(\d+[\d,]*)', price_text.replace('₹', '').replace(',', ''))
        return int(price_match.group(1)) if price_match else 0

    def _extract_original_price(self, product) -> int:
        """Extract original price if discounted"""
        try:
            original_price_element = product.find_element(By.CSS_SELECTOR, ".product-strike")
            original_price_text = original_price_element.text.strip()
            return self._extract_price(original_price_text)
        except:
            return 0

    def _check_for_bot_detection(self) -> bool:
        """Check if Myntra has detected scraping"""
        try:
            # Check for captcha elements
            captcha_selectors = [
                ".captcha-container", 
                "#captcha", 
                ".recaptcha",
                ".geetest_holder",
                ".bot-detected"
            ]
            
            for selector in captcha_selectors:
                if len(self.driver.find_elements(By.CSS_SELECTOR, selector)) > 0:
                    print("⚠️ Bot detection triggered - captcha found")
                    return True
            
            # Check for access denied messages
            blocked_texts = ["access denied", "bot detected", "security check"]
            page_text = self.driver.page_source.lower()
            if any(text in page_text for text in blocked_texts):
                print("⚠️ Bot detection triggered - access denied message")
                return True
                
            return False
        except:
            return False
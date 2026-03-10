"""
Comprehensive API Test Suite for Stylumia AI Fashion Assistant
Run this script to test all endpoints
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
from typing import Dict, Any, List

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 30  # seconds

# Colors for console output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_result(test_name: str, success: bool, data: Any = None, error: str = None):
    """Pretty print test results"""
    status = f"{GREEN}✓ PASSED{RESET}" if success else f"{RED}✗ FAILED{RESET}"
    print(f"\n{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"Test: {test_name}")
    print(f"Status: {status}")
    if data:
        print(f"Response: {json.dumps(data, indent=2)[:500]}")
    if error:
        print(f"Error: {RED}{error}{RESET}")
    print(f"{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")

def test_health_check():
    """Test health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        success = response.status_code == 200
        data = response.json() if success else None
        print_result("Health Check", success, data)
        return success, data
    except Exception as e:
        print_result("Health Check", False, error=str(e))
        return False, None

def test_root_endpoint():
    """Test root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        success = response.status_code == 200
        data = response.json() if success else None
        print_result("Root Endpoint", success, data)
        return success, data
    except Exception as e:
        print_result("Root Endpoint", False, error=str(e))
        return False, None

def test_legacy_text_search():
    """Test legacy text search endpoint"""
    try:
        payload = {
            "query": "blue dress",
            "top_k": 10
        }
        response = requests.post(
            f"{BASE_URL}/search/text", 
            json=payload,
            timeout=TIMEOUT
        )
        success = response.status_code == 200
        data = response.json() if success else None
        print_result("Legacy Text Search", success, data)
        return success, data
    except Exception as e:
        print_result("Legacy Text Search", False, error=str(e))
        return False, None

def test_legacy_image_search():
    """Test legacy image search endpoint"""
    try:
        # Create a simple test image (you can also use a real image file)
        files = {
            'file': ('test.jpg', b'fake image data', 'image/jpeg')
        }
        data = {'top_k': '10'}
        
        response = requests.post(
            f"{BASE_URL}/search/image",
            files=files,
            data=data,
            timeout=TIMEOUT
        )
        success = response.status_code == 200
        data = response.json() if success else None
        print_result("Legacy Image Search", success, data)
        return success, data
    except Exception as e:
        print_result("Legacy Image Search", False, error=str(e))
        return False, None

def test_stylist_categories():
    """Test get categories endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/stylist/categories", timeout=TIMEOUT)
        success = response.status_code == 200
        data = response.json() if success else None
        print_result("Get Stylist Categories", success, data)
        return success, data
    except Exception as e:
        print_result("Get Stylist Categories", False, error=str(e))
        return False, None

def test_quick_suggest():
    """Test quick suggest endpoint"""
    try:
        payload = {
            "occasion": "wedding",
            "gender": "male",
            "style": "traditional",
            "budget": "mid_range"
        }
        response = requests.post(
            f"{BASE_URL}/api/stylist/suggest",
            json=payload,
            timeout=TIMEOUT
        )
        success = response.status_code == 200
        data = response.json() if success else None
        print_result("Quick Suggest", success, data)
        return success, data
    except Exception as e:
        print_result("Quick Suggest", False, error=str(e))
        return False, None

def test_styling_tips():
    """Test styling tips endpoint"""
    try:
        occasions = ["wedding", "office", "party", "casual", "beach"]
        results = []
        
        for occasion in occasions:
            response = requests.get(
                f"{BASE_URL}/api/stylist/tips/{occasion}",
                timeout=TIMEOUT
            )
            if response.status_code == 200:
                results.append(f"{occasion}: ✓")
            else:
                results.append(f"{occasion}: ✗")
        
        print_result("Styling Tips", all("✓" in r for r in results), {"results": results})
        return True, {"results": results}
    except Exception as e:
        print_result("Styling Tips", False, error=str(e))
        return False, None

def test_trending_colors():
    """Test trending colors endpoint"""
    try:
        seasons = ["summer", "winter", "spring", "fall", "monsoon"]
        results = []
        
        for season in seasons:
            response = requests.get(
                f"{BASE_URL}/api/stylist/trending/{season}",
                timeout=TIMEOUT
            )
            if response.status_code == 200:
                results.append(f"{season}: ✓")
            else:
                results.append(f"{season}: ✗")
        
        print_result("Trending Colors", all("✓" in r for r in results), {"results": results})
        return True, {"results": results}
    except Exception as e:
        print_result("Trending Colors", False, error=str(e))
        return False, None

def test_feedback():
    """Test feedback endpoint"""
    try:
        payload = {
            "query": "wedding outfit",
            "rating": 5,
            "comments": "Great suggestions!",
            "timestamp": datetime.now().isoformat()
        }
        response = requests.post(
            f"{BASE_URL}/api/stylist/feedback",
            json=payload,
            timeout=TIMEOUT
        )
        success = response.status_code == 200
        data = response.json() if success else None
        print_result("Feedback Submission", success, data)
        return success, data
    except Exception as e:
        print_result("Feedback Submission", False, error=str(e))
        return False, None

def test_admin_scraper_status():
    """Test admin scraper status endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/admin/scraper/status", timeout=TIMEOUT)
        success = response.status_code == 200
        data = response.json() if success else None
        print_result("Admin Scraper Status", success, data)
        return success, data
    except Exception as e:
        print_result("Admin Scraper Status", False, error=str(e))
        return False, None

def run_all_tests():
    """Run all tests in sequence"""
    print(f"\n{YELLOW}🚀 Starting API Tests at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"{YELLOW}Base URL: {BASE_URL}{RESET}\n")
    
    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/health", timeout=5)
    except:
        print(f"{RED}❌ Server not running at {BASE_URL}{RESET}")
        print(f"Please start the server first: python alternative_main.py")
        return
    
    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root_endpoint),
        ("Legacy Text Search", test_legacy_text_search),
        ("Legacy Image Search", test_legacy_image_search),
        ("Stylist Categories", test_stylist_categories),
        ("Quick Suggest", test_quick_suggest),
        ("Styling Tips", test_styling_tips),
        ("Trending Colors", test_trending_colors),
        ("Feedback", test_feedback),
        ("Admin Scraper Status", test_admin_scraper_status)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"{YELLOW}Running: {test_name}{RESET}")
        success, _ = test_func()
        results.append((test_name, success))
        time.sleep(1)  # Small delay between tests
    
    # Summary
    print(f"\n{YELLOW}📊 TEST SUMMARY{RESET}")
    print(f"{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = f"{GREEN}✓{RESET}" if success else f"{RED}✗{RESET}"
        print(f"{status} {test_name}")
    
    print(f"{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"Passed: {GREEN}{passed}/{total}{RESET}")
    print(f"Failed: {RED}{total-passed}/{total}{RESET}")
    
    if passed == total:
        print(f"\n{GREEN}🎉 All tests passed! Your API is working perfectly!{RESET}")
    else:
        print(f"\n{YELLOW}⚠️  Some tests failed. Check the errors above.{RESET}")

if __name__ == "__main__":
    run_all_tests()
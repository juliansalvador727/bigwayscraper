from playwright.sync_api import sync_playwright
import logging
import re
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_line_size(store_id: int, timeout: int = 30000) -> Optional[int]:
    """
    Scrape the line size for a given store ID.
    
    Args:
        store_id: The store ID to scrape
        timeout: Timeout in milliseconds (default: 30 seconds)
        
    Returns:
        Number of parties in line, or None if scraping failed
    """
    url = f"https://gosnappy.io/lineup/?force=true&storeId={store_id}"
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Set timeout and navigate
            page.set_default_timeout(timeout)
            response = page.goto(url)
            
            if not response or response.status != 200:
                logger.warning(f"Failed to load page for store {store_id}: HTTP {response.status if response else 'No response'}")
                return None
            
            # Wait for the line indicator text
            try:
                page.wait_for_selector("text=/in line/i", timeout=timeout)
            except Exception as e:
                logger.warning(f"Timeout waiting for 'in line' text for store {store_id}: {e}")
                return None
            
            # Try multiple selector strategies
            selectors = [
                "xpath=//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'in line')]",
                "text=/in line/i",
                "[data-testid*='line'], [class*='line'], [id*='line']"
            ]
            
            text = None
            for selector in selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible():
                        text = element.inner_text().lower()
                        break
                except Exception:
                    continue
            
            browser.close()
            
            if not text:
                logger.warning(f"Could not find line text for store {store_id}")
                return None
                
            return parse_line_count(text)
            
    except Exception as e:
        logger.error(f"Error scraping store {store_id}: {e}")
        return None

def parse_line_count(text: str) -> int:
    """
    Parse the line count from text content.
    
    Args:
        text: The text content containing line information
        
    Returns:
        Number of parties in line
    """
    text = text.lower().strip()
    
    # Check for no one in line
    if any(phrase in text for phrase in ["no one", "no parties", "0 parties"]):
        return 0
    
    # Extract numbers using regex
    numbers = re.findall(r'\d+', text)
    
    if numbers:
        # Take the first number found
        return int(numbers[0])
    
    # If no numbers found, assume 0
    logger.warning(f"Could not parse line count from text: '{text}'")
    return 0
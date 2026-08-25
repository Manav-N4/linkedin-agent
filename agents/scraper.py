from playwright.sync_api import sync_playwright
import time

def scrape_with_headless(url: str, timeout: int = 30000) -> str:
    """
    Scrape a website using headless Chrome browser.
    Waits for JavaScript to render before extracting text.
    
    Args:
        url: The website URL to scrape
        timeout: Wait time in milliseconds for page to load (default 10s)
    
    Returns:
        Plain text content from the page
    
    Raises:
        Exception: If scraping fails
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(url, wait_until="networkidle", timeout=timeout)
            time.sleep(2)  # Extra wait for dynamic content
            content = page.content()
            
            # Extract text from HTML
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)
            
            browser.close()
            return text
        except Exception as e:
            browser.close()
            raise Exception(f"Headless scraping failed: {str(e)}")
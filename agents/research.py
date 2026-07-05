from dotenv import load_dotenv
import os
import requests 
# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup
SKIP_DOMAINS = ["instagram.com", "facebook.com", "reddit.com", "youtube.com", "twitter.com"]
load_dotenv()
def search_web(query:str) -> list[dict]:
    url = "https://google.serper.dev/search"
    api_key = os.getenv("SERPER_API_KEY")
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    body = {
        "q": query
    }       
    r = requests.post(url, headers=headers, json=body)
    r_json = r.json()
    results = r_json["organic"]
    return [{"title": result["title"], "link": result["link"]} for result in results]

def is_scrapeable(url: str) -> bool:
    return not any(domain in url for domain in SKIP_DOMAINS)

def scrape_page(url:str) -> str:
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        print("Failed to fetch page:", e)
        return ""
    soup = BeautifulSoup(response.text, "html.parser")
    if response:
        paras = soup.find_all("p")
        print(f"Found {len(paras)} paragraphs")  # add this
        print(response.status_code)              # and this
        return " ".join([p.get_text() for p in paras])
    else:
        return ""
if __name__ == "__main__":
    results = search_web("solo travel tips 2026")
    for result in results:
        if is_scrapeable(result["link"]):
            text = scrape_page(result["link"])
            if text:
                print(text[:500])
                break
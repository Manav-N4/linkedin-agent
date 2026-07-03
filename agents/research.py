from dotenv import load_dotenv
import os
import requests 
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

if __name__ == "__main__":
    print(search_web("solo travel tips 2026"))
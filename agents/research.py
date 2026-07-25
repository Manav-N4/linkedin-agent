from dotenv import load_dotenv
import os
import requests 
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient()
collection = client.get_or_create_collection("research")

SKIP_DOMAINS = ["instagram.com", "facebook.com", "reddit.com", "youtube.com", "twitter.com"]
load_dotenv()
def embed_and_store(text: str, url: str) -> None:
    words = text.split()
    chunks = [" ".join(words[i:i+200]) for i in range(0, len(words), 200)]
    embeddings = model.encode(chunks)
    collection.add(
        documents = chunks,
        embeddings = embeddings.tolist(),
        ids = [f"{url}_chunk_{i}" for i in range(len(chunks))]
    )

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
        return " ".join([p.get_text() for p in paras])
    else:
        return ""
def query_research(topic: str, n_results: int = 3) -> list[str]:
    # step 1: encode the topic into a query vector
    query = model.encode([topic]).tolist() 
    # step 2: make sure n_results doesn't exceed collection.count()
    if n_results > collection.count():
        n_results = min(n_results, collection.count()) 
    # step 3: query the collection with the vector
    res = collection.query(query_embeddings=query, n_results=n_results)
    # step 4: return the documents from the result
    return res["documents"][0]
def research_agent(topic: str) -> list[str]:
    results = search_web(topic)
    pages_scraped = 0
    for result in results:
        if is_scrapeable(result["link"]):
            text = scrape_page(result["link"])
            if text:
                embed_and_store(text, result["link"])
                pages_scraped += 1
                if pages_scraped == 3:
                    break
    return query_research(topic)
if __name__ == "__main__":
    res = research_agent("solo travel")
    print(res)
from agents.writing_critic import rate_drafts
from agents.draft import generate_drafts
from agents.hook import generate_hooks
from agents.brief import create_brief
from agents.critic import be_critique
from agents.examples import get_examples
from agents.research import research_agent
from agents.orchestrator import classify_topic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.profile_extractor import extract_profile, BrandProfile
from agents.scraper import scrape_with_headless

class GenerateRequest(BaseModel):
    topic: str
    profile: dict
class ExtractProfileRequest(BaseModel):
    website_url: str
class GenerateResponse(BaseModel):
    hooks: list[str]
    drafts: list[str]
    scores: dict

app = FastAPI()

from fastapi.responses import JSONResponse
import traceback

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Unhandled Exception: {str(exc)}"}
    )

@app.post("/extract-profile")
def extract_profile_endpoint(request: ExtractProfileRequest):
    if not request.website_url:
        raise HTTPException(status_code=400, detail="website_url is required")
    
    print(f"Scraping website: {request.website_url}")
    try:
        website_content = scrape_with_headless(request.website_url)
        if not website_content:
            raise HTTPException(status_code=400, detail="Failed to scrape website")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to scrape website: {str(e)}")
    
    print("Extracting brand profile...")
    try:
        profile = extract_profile(website_content, brand_name=request.website_url)
        return {
            "brand_name": profile.brand_name,
            "voice": profile.voice,
            "key_pillars": profile.key_pillars,
            "tone_examples": profile.tone_examples
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile extraction failed: {str(e)}")

@app.post("/generate", response_model=GenerateResponse)
def root(request:GenerateRequest):
    try:
        profile = BrandProfile(**request.profile)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid profile: {str(e)}")
    print("Classifying topic...")
    classified_topic = classify_topic(request.topic)
    if classified_topic is None:
        raise HTTPException(status_code=500, detail="Failed to classify topic")
    print("Researching...")
    research = research_agent(request.topic)
    if len(research) == 0:
        print("Failed to research")
        return
    print("Fetching suitable examples...")
    examples = get_examples(request.topic, research)
    if len(examples) == 0:
        raise HTTPException(status_code=500, detail="Failed to generate examples")
    print("Flagging mistakes...")
    critic = be_critique(request.topic, research, examples)
    if len(critic) == 0:
        raise HTTPException(status_code=500, detail="Failed to generate critic points")
    print("Creating a brief...")
    brief = create_brief(request.topic, research, examples, critic)
    if brief is None:
        raise HTTPException(status_code=500, detail="Failed to generate brief")
    print("Generating 5 Hooks...")
    hooks = generate_hooks(brief, brand_profile=profile)
    if len(hooks) < 3:
        raise HTTPException(status_code=500, detail="Failed to generate hooks")
    print(hooks)
    print("Generating 2 drafts...")
    drafts = generate_drafts(hooks, brief, brand_profile=profile)
    if len(drafts) == 0:
        raise HTTPException(status_code=500, detail="Failed to generate drafts")
    print(drafts)
    print("Scoring the drafts...")
    scoring = rate_drafts(hooks, drafts)
    if scoring is None:
        raise HTTPException(status_code=500, detail="Failed to score")
    print(scoring)
    print("Feel free to suggest any changes!")
    return GenerateResponse(hooks=hooks, drafts=drafts, scores=scoring)
    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=10000)
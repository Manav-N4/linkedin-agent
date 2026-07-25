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

class GenerateRequest(BaseModel):
    topic: str
class GenerateResponse(BaseModel):
    hooks: list[str]
    drafts: list[str]
    scores: dict

app = FastAPI()
@app.post("/generate", response_model=GenerateResponse)
async def root(request:GenerateRequest):
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
    hooks = generate_hooks(brief)
    if len(hooks) < 3:
        raise HTTPException(status_code=500, detail="Failed to generate hooks")
    print(hooks)
    print("Generating 2 drafts...")
    drafts = generate_drafts(hooks, brief)
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
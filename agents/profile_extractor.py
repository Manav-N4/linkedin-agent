from agents.orchestrator import strip_json_fences
from pydantic import BaseModel, ValidationError
from core.llm import call_llm
import json

class BrandProfile(BaseModel):
    brand_name: str
    voice: str  
    key_pillars: list[str]  
    tone_examples: list[str]  

def extract_profile(website_content: str, brand_name: str = "Brand") -> BrandProfile:
    system_prompt = """You are an expert at analyzing brand websites and extracting their core voice, values, and tone.
Return ONLY valid JSON, no markdown, no extra text."""

    user_prompt = f"""Analyze this brand's website content and extract their brand profile.

Website Content:
{website_content}

Extract and return ONLY a JSON object with these fields:
- brand_name: The brand name (use "{brand_name}" if not found)
- voice: 2-3 sentences describing their tone, personality, and how they speak to their audience
- key_pillars: A list of 3-5 core themes/values this brand stands for
- tone_examples: A list of 2-3 short (under 15 word) quotes or phrases from the website that exemplify their voice"""

    response = call_llm(system_prompt, user_prompt)
    cleaned = strip_json_fences(response)
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        print(f"LLM did not return valid JSON. Raw response:\n{response}")
        raise ValueError("Profile extraction failed: invalid JSON from LLM")
    try:
        return BrandProfile.model_validate(parsed)
    except ValidationError as e:
        print(f"Validation error: {e}")
        raise ValueError(f"Profile extraction failed: {e}")
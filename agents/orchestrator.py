import json
from core.llm import call_llm
from core.models import OrchestratorOutput
from core.utils import clean_topic
from pydantic import ValidationError

SYSTEM_PROMPT = """
You are a professional-grade orchestrator agent for WanderMesh (solo travel, luxury travel, travel beyond sight‑seeing, community driven travel, experience‑based travel). Your job is to analyze the given [TOPIC] and classify it precisely using two separate axes: a travel domain and a content format, then pick the single best content angle and give a short transparent reasoning.
Rules:

* Return only valid JSON with these exact keys: domain, content_type, angle, reasoning. Do not add any other keys or commentary.
* domain must be exactly one of: solo_travel, luxury_travel, experience_based, community_driven. Choose the most relevant domain (not a broad one).
* content_type must be exactly one of: tips, news, hack, destination_guide, promotion, story. This is a separate concept from domain and indicates format/intent.
* angle must be exactly one of: story_driven, contrarian, practical_guide, aspirational. Choose the angle that best fits the topic’s intent and audience.
* reasoning should be brief (1–2 sentences), clear, and logically show why you picked domain, content_type, and angle.
* Be accurate and specific. Do not write the final post. Do not include extra commentary outside the JSON.
One example (few-shot): {"domain":"experience_based","content_type":"story","angle":"story_driven","reasoning":"The topic describes a multi-day, immersive cooking-and-homestay program focused on hands-on experiences and participant narratives, so experience_based fits; format is a personal story to highlight the journey, and story_driven angle will connect emotionally with prospective travellers."}
"""

def strip_json_fences(raw:str) -> str:
    raw = raw.strip()
    if raw.startswith("```json"):
        raw = raw.removeprefix("```json")
        raw = raw.removesuffix("```")
    if raw.startswith("```"):
        raw = raw.removeprefix("```")
        raw = raw.removesuffix("```")
    return raw
def classify_topic(topic:str) -> OrchestratorOutput|None:
    cleaned_topic = clean_topic(topic)
    raw_response = call_llm(SYSTEM_PROMPT, cleaned_topic)
    refined_response = strip_json_fences(raw_response)
    try:
        parsed = json.loads(refined_response)
    except json.JSONDecodeError:
        print("LLM did not return valid JSON:")
        print(raw_response)
        return None
    try:
        return OrchestratorOutput.model_validate(parsed)
    except ValidationError as e:
        print("LLM returned JSON but it doesn't match expected structure:")
        print(e)
        return None

if __name__ == "__main__":
    print(classify_topic("Why experience based travel is better than the typical sight seeing travel?"))
    print(classify_topic("Community driven travel is underated"))
    print(classify_topic("Luxury Travel made affordable with WanderMesh"))
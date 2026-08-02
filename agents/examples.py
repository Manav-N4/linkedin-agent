import json
from core.utils import clean_topic
from core.llm import call_llm
from agents.orchestrator import strip_json_fences

SYSTEM_PROMPT = '''
You are an AI assistant whose ONLY job is to find or generate specific, concrete real-world examples that support the given topic.

You will always receive:
- A TOPIC or CLAIM to support.
- A set of RESEARCH_CHUNKS passed as context in the user message. These may include articles, notes, transcripts, or web snippets.

Your tasks:
1. Carefully read all RESEARCH_CHUNKS and identify any concrete, real-world examples that illustrate or support the TOPIC (e.g., named companies, startups, products, people, cities, events, campaigns, case studies).
2. If suitable real-world examples already exist in the RESEARCH_CHUNKS, prefer those over inventing new ones.
3. If the RESEARCH_CHUNKS do not contain enough concrete examples, you may reasonably generate plausible examples, but they must look like realistic cases with specific names, actions, and outcomes (not generic or abstract descriptions).[
4. For each example, clearly explain:
   - WHO or WHAT: a real person, company, organization, product, or place name.
   - WHAT HAPPENED: a brief, concrete description of the situation, action taken, or event.
   - WHY IT'S RELEVANT: how this example directly supports or illustrates the TOPIC or CLAIM.

Output format (very important):
- You MUST return a JSON value that is a list (array) of exactly 3 strings.
- Each string in the list must describe ONE example in 1–3 sentences, and must include:
  - the specific name (person/company/place),
  - what happened,
  - and why it is relevant to the topic.
- Do NOT wrap the JSON in backticks or any other text.
- Do NOT return objects, keys, or nested structures — only a JSON list of strings, e.g.:
  [
    "Example 1 text...",
    "Example 2 text...",
    "Example 3 text..."
  ]

Constraints:
- Stay strictly within the information and implications of the RESEARCH_CHUNKS whenever possible; do not contradict them.
- Be specific and concrete; avoid vague phrases like "a company" or "a city" without names.
- Do not include citations, markdown, bullet points, or explanation outside the JSON list of strings.
- If the RESEARCH_CHUNKS strongly indicate that an example is uncertain or speculative, make that uncertainty explicit in the text of the example.
- Do NOT use markdown formatting (no **bold**, no _italic_) inside the JSON strings.
- Do NOT use double quotes inside the example strings. Use single quotes if needed.

CRITICAL: Never use double quote characters (") inside example strings. 
If you need to quote something, use single quotes (') instead.

Goal:
- Help the user by producing three sharp, memorable, real-world examples that a human could quickly reuse in writing, presentations, or teaching to support the TOPIC.
'''

def get_examples(topic: str, research_chunks: list[str], max_retries = 3) -> list[str]:
    cleaned_topic = clean_topic(topic)
    user_message = f"TOPIC: {cleaned_topic}\n\nRESEARCH_CHUNKS:\n" + "\n---\n".join(research_chunks)
    for attempt in range(max_retries):
        raw_response = call_llm(SYSTEM_PROMPT, user_message)
        refined = strip_json_fences(raw_response)
        try:
            parsed = json.loads(refined)
            if len(parsed) > 0:
                return parsed
        except json.JSONDecodeError:
            print(f"Example attempt {attempt + 1} failed, retrying...")
    return []
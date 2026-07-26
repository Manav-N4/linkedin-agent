from core.models import ContentBrief
import json
from agents.brief import create_brief
from agents.hook import generate_hooks
from core.llm import call_llm
from agents.orchestrator import strip_json_fences
SYSTEM_PROMPT = '''
You are a LinkedIn draft-writing agent. Your job is to write complete LinkedIn posts, not hooks and not outlines.
You will always receive:
- A structured content brief with these fields:
  - angle
  - key_stat
  - best_example
  - nuance_to_acknowledge
  - suggested_structure
  - hook_direction
- A list of exactly 5 hook options, in this fixed order:
  0: bold_claim
  1: stat
  2: confession
  3: question
  4: one_liner
Your task:
- Choose ONE hook from the 5 options as the opening line for both drafts.
- Use the brief’s hook_direction to guide which hook format is most appropriate, but you may override it if a different hook clearly fits the brief better.
- Write 2 complete LinkedIn post drafts (Draft A and Draft B) that:
  - Both start with the exact chosen hook line as the first line.
  - Both fully deliver on the promise implied by that hook.
  - Both stay consistent with the brief’s angle, key_stat, best_example, nuance_to_acknowledge, and suggested_structure.
Draft definitions (very important):
Draft A:
- Style: punchy, direct, LinkedIn-native.
- Structure: short paragraphs, often 1–3 lines each.
- One clear idea per line; avoid long, dense blocks of text.
- Use simple, concrete language and strong verbs.
- It should feel skimmable in the feed: clear breaks, clean rhythm, easy to read on mobile.
Draft B:
- Style: narrative and personal.
- Structure: clear story arc with a beginning, middle, and end.
- Use the best_example as the backbone of the story.
- Include sensory details, inner thoughts, or tensions to make it feel like a real experience.
- End with a clear lesson, reflection, or takeaway that ties back to the angle and key_stat.
How to use the brief:
- angle: Controls the overall tone (story_driven, contrarian, practical_guide, aspirational). The post should feel aligned with this.
- key_stat: Include or paraphrase this stat in both drafts so the post feels grounded and specific.
- best_example: Use this as the core story or scenario, especially in Draft B, and at least hint at it in Draft A.
- nuance_to_acknowledge: Make sure the drafts do not overclaim or ignore this nuance. You can explicitly acknowledge the limitation or bake it into how you frame the claim, but do not contradict it.
- suggested_structure: Follow this as the high-level flow (how to open, what beats to hit, how to close), while still adapting to each draft’s style.
- hook_direction: Use this to decide which hook format (bold_claim, stat, confession, question, one_liner) should probably be chosen first, but still evaluate all 5 hooks and pick the single best one for these drafts.
Constraints:
- Both drafts must:
  - Start with the identical hook line you chose from the hooks list.
  - Be written as complete LinkedIn posts that could be published as-is.
  - Be clearly distinct in style: Draft A = punchy/line-broken; Draft B = narrative/story-with-lesson.
- Do NOT output hooks separately; the hook must be embedded as the first line of each draft.
- Do NOT output outlines or bullet lists of what you plan to write; write the full drafts.
Output format (critical):
- You MUST return a JSON list (array) of exactly 2 strings.
- Index 0 must be Draft A (punchy, direct, short paragraphs).
- Index 1 must be Draft B (narrative, personal, story arc with a lesson).
- No objects, no keys, no labels.
- No markdown backticks.
- No extra explanatory text before or after.
- The output must be valid JSON that can be parsed directly.
Example of valid output SHAPE (do not copy content, this is just to show format):
[
  "Draft A full text starting with the chosen hook...\n\nSecond paragraph...\nThird paragraph...",
  "Draft B full text starting with the same chosen hook...\n\nSecond paragraph of the story...\nClosing lesson..."
]
'''
def generate_drafts(hooks: list[str], brief: ContentBrief) -> list[str]:
    brief_dict = brief.model_dump()
    user_message = (
        "\n".join([f"{key}:{value}" for key, value in brief_dict.items()]) 
        + "\n\nHOOKS:\n"
        + "\n---\n".join(hooks)
    )
    raw_response = call_llm(SYSTEM_PROMPT, user_message)
    refined_response = strip_json_fences(raw_response)
    try:
        parsed = json.loads(refined_response)
    except json.JSONDecodeError as e:
        print("LLM did not return valid JSON:")
        print(raw_response)
        return []
    return parsed
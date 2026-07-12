from pydantic import BaseModel, ValidationError

class OrchestratorOutput(BaseModel):
    domain: str
    angle: str
    reasoning: str
    content_type: str

class ContentBrief(BaseModel):
    angle: str
    key_stat: str
    best_example: str
    nuance_to_acknowledge: str
    suggested_structure: str
    hook_direction: str

if __name__ == "__main__":
    try:
        print(OrchestratorOutput.model_validate({
            "domain": "solo_travel",
            "angle": "contrarian",
            "reasoning": "Some reason"
        }))
    except ValidationError as e:
        print(e)
    try:
        print(OrchestratorOutput.model_validate({
            "domain": "finance",
            "angle": "contrarian",
            "reasoning": "Some reason"
        }))
    except ValidationError as e:
        print(e)
    try:
        print(OrchestratorOutput.model_validate({
            "domain": "solo_travel",
            "angle": "contrarian"
        }))
    except ValidationError as e:
        print(e)
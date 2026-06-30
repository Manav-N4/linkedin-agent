from typing import Literal
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ValidationError

class OrchestratorOutput(BaseModel):
    domain: Literal["solo_travel", "luxury_travel", "experience_based", "community_driven"]
    angle: Literal["story_driven", "contrarian", "practical_guide", "aspirational"]
    reasoning: str

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
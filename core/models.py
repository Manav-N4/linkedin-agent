# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ValidationError

class OrchestratorOutput(BaseModel):
    domain: str
    angle: str
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
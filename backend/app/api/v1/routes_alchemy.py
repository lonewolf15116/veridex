from fastapi import APIRouter
from pydantic import BaseModel
from app.services.orchestrator import run_alchemy

router = APIRouter()


class IdeaRequest(BaseModel):
    idea: str
    mode: str = "build"


@router.post("/alchemy/run")
def run(request: IdeaRequest):
    result = run_alchemy(request.idea, request.mode)
    return result
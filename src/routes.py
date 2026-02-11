from fastapi import APIRouter, Request
from langchain_core.messages import BaseMessage

from src.llm.chat import process_message

router = APIRouter()


@router.get("/")
async def root():
    return {"app": "avr-chat", "version": "0.1"}


@router.post("/chat")
async def chat(request: Request, messages: list[BaseMessage]) -> list[BaseMessage]:
    app_config = request.app.state.config
    return process_message(app_config, messages)

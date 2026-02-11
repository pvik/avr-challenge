from __future__ import annotations

import json
from pathlib import Path

from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field, field_validator

from src.llm.config import OpenRouterLLMConfig

class AvrQuestion(BaseModel):
    question: str = Field(description="Question for Eva")
    answer: str = Field(description="Answer for Eva")

    def __str__(self) -> str:
        return f"Question: {self.question}\nAnswer:{self.answer}\n"

class AppConfig(BaseModel):
    llm: OpenRouterLLMConfig = Field(description="Open router Config")

    avr_questions: list[AvrQuestion] = []

    def get_system_messages(self) -> list[SystemMessage]:
        ret = []
        if self.llm.additional_context:
            ret += [SystemMessage(content=m) for m in self.llm.additional_context]

        ret += [SystemMessage(content=f"""You are AVR. one of Thoughtful AI's customer assistance agent.
Below are a list of questions and answers you should use when answering questions from users.
If the user asks a question about Thoughtful AI or it's agent that is not in the list, respond with a generic response stating your limitation of not having the knowledge to answer the question.
Always answer questions in a polite and respectful manner.
If the user asks questions that are not related to Thoughtful AI, respond with a generic response stating you are only able to assist in Thoughtful AI related questions.
""")]

        ret += [SystemMessage(content=f"{q}") for q in self.avr_questions]

        return ret


def load_config(path: str | Path) -> AppConfig:
    try:
        config_path = Path(path)
        data = json.loads(config_path.read_text(encoding="utf-8"))
        return AppConfig.model_validate(data)
    except Exception as e:
        raise ValueError(f"Failed to load config: {e}")

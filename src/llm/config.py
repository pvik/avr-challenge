from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model


class LLMConfig(BaseModel):
    api_key: str = Field(description="api key")

    model: str = Field(description="LLM model name")
    temperature: float = Field(default=0.7, description="Temperature for LLM")

    additional_context: list[str] | None = Field(default=None, description="Additional context for LLM")

class OpenRouterLLMConfig(LLMConfig):
    model_provider: str = Field(default="openai", description="Model provider")

    def get_model(self) -> BaseChatModel:
        return init_chat_model(
            model=self.model,
            model_provider=self.model_provider,
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )

from langchain_core.messages import BaseMessage, HumanMessage

from src.config import AppConfig


def process_message(app_config: AppConfig, messages: list[BaseMessage]) -> list[BaseMessage]:
    model = app_config.llm.get_model()
    if not isinstance(messages[-1], HumanMessage):
        raise ValueError("Last message must be a human message")

    sys_msgs = app_config.get_system_messages()

    response = model.invoke(sys_msgs + messages)

    return messages + [response]

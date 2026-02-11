import argparse
import logging

from langchain_core.messages import HumanMessage

from src.config import load_config
from src.llm.chat import process_message

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the EVA chat CLI.")
    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to the config JSON file.",
    )
    return parser.parse_args()


def main(config_path: str) -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logger.info("Loading config from %s", config_path)
    app_config = load_config(config_path)

    messages = []
    print("AVR chat CLI. Press Ctrl+C to exit.")
    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue

        messages.append(HumanMessage(content=user_input))
        messages = process_message(app_config, messages)
        response = messages[-1]
        print(f"AVR: {response.content}")


if __name__ == "__main__":
    args = parse_args()
    main(args.config)

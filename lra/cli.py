import argparse
import os
from langchain import agents as lagents


def main(message: str):
    assistant = lagents.create_agent(
        model=os.environ.get("agent_model"),
        system_prompt="You are a helpful assistant."
    )
    response = assistant.invoke({"messages": [{"role": "user", "content": message}]})
    return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('message')
    args = parser.parse_args()
    main(args.message)

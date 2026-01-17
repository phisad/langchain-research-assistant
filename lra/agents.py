import os

from langchain.agents import create_agent


def create_research_agent(tools):
    graph = create_agent(
        model=os.environ.get("agent_model"),
        tools=tools,
        system_prompt="You are a helpful research assistant with access to PDF documents.",
    )

    async def agent(message: str, *, thread_id: str = "default") -> str:
        config = {"configurable": {"thread_id": thread_id}}
        result = await graph.ainvoke({"messages": [{"role": "user", "content": message}]}, config=config)
        return result["messages"][-1].content

    return agent

from langchain_openai import AzureChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from src.core.config import settings
from src.tools.search import get_search_tool
import os


def create_agent():
    settings.validate_api_keys()

    memory = MemorySaver()
    model = AzureChatOpenAI(
        model_name="gpt-4o-mini",
        api_key=settings.AZURE_OPENAI_API_KEY,
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        openai_api_version="2024-02-15-preview",
        temperature=0.7,
    )

    try:
        tools = [get_search_tool()]
        return create_react_agent(model, tools, checkpointer=memory)
    except Exception as e:
        print(f"Error creating agent: {str(e)}")
        raise

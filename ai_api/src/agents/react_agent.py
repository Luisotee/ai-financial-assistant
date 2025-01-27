from langchain_openai import AzureChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from src.core.config import settings
from src.tools.search import get_search_tool
from src.tools.sheets import get_sheets_tool
import os


def get_platform_prompt(platform: str) -> str:
    base_prompt = """You are a helpful AI assistant specializing in financial and banking matters.
Always provide accurate, clear, and concise information."""

    platform_prompts = {
        "whatsapp": """Format responses for WhatsApp:
- Use emojis sparingly for emphasis 📱
- Keep messages concise and easily readable on mobile
- Use bullet points for lists
- Split long responses into shorter messages""",
        "telegram": """Format responses for Telegram:
- Support for markdown formatting
- Can use code blocks for data ```like this```
- Use emojis when appropriate 🤖
- Support for longer messages""",
        "default": "Provide clear, professional responses with appropriate formatting.",
    }

    return f"{base_prompt}\n\n{platform_prompts.get(platform.lower(), platform_prompts['default'])}"


def create_agent(platform: str = "default"):
    settings.validate_api_keys()

    memory = MemorySaver()
    model = AzureChatOpenAI(
        model_name="gpt-4o-mini",
        api_key=settings.AZURE_OPENAI_API_KEY,
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        openai_api_version="2024-02-15-preview",
        temperature=0.7,
    )

    prompt = get_platform_prompt(platform)

    try:
        tools = [get_search_tool(), get_sheets_tool()]
        return create_react_agent(
            model, tools, state_modifier=prompt, checkpointer=memory
        )
    except Exception as e:
        print(f"Error creating agent: {str(e)}")
        raise

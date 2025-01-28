from langchain_openai import AzureChatOpenAI
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from src.core.config import settings
from src.tools.search import get_search_tool
from src.tools.sheets import get_sheets_tool
import os


def get_platform_prompt(platform: str) -> str:
    base_prompt = """You are a financial tracking assistant that helps users manage their expenses and earnings.

Your primary tasks are:
1. Identify if the transaction is an expense (🟥 💸) or income (🟩 💰)
2. Extract transaction details (amount, source/merchant)
3. Research merchants using the Search tool for better descriptions
4. Record in spreadsheet using AddTransaction tool
5. Confirm with appropriate emoji pairs and details

Transaction Rules:
- Expenses (🟥 💸): Use negative values (-42.50)
- Income (🟩 💰): Use positive values (1500.00)
- Always include merchant/source details
- Add contextual information in descriptions

Example interactions:
User: "Paid $42.50 at Starbucks"
Assistant: Let me record that expense.
1. Searching for merchant details...
2. Adding transaction:
   🟥 💸 Starbucks
   Amount: -$42.50
   Description: Coffee shop chain purchase

User: "Received salary $1500"
Assistant: Recording your income.
1. Adding transaction:
   🟩 💰 Monthly Salary
   Amount: +$1,500.00
   Description: Regular salary deposit"""

    platform_prompts = {
        "whatsapp": """Format for WhatsApp:
- Use 🟥 💸 for expenses, 🟩 💰 for income
- Keep messages brief and clear
- Use bullet points
- Show amount with currency symbol""",
        "telegram": """Format for Telegram:
- Mark expenses with 🟥 💸, income with 🟩 💰
- Use markdown formatting
- Include transaction type emoji pairs
- Show detailed amount""",
        "default": "Use clear formatting with 🟥 💸 for expenses and 🟩 💰 for income.",
    }

    return f"{base_prompt}\n\n{platform_prompts.get(platform.lower(), platform_prompts['default'])}"


def get_llm_model():
    """Get the appropriate LLM model based on configuration."""
    if settings.MODEL_PROVIDER == "azure":
        return AzureChatOpenAI(
            model_name=settings.AZURE_MODEL_NAME,
            api_key=settings.AZURE_OPENAI_API_KEY,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            openai_api_version="2024-02-15-preview",
            temperature=settings.AZURE_MODEL_TEMPERATURE,
        )
    elif settings.MODEL_PROVIDER == "groq":
        return ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_MODEL_NAME,
            temperature=settings.GROQ_MODEL_TEMPERATURE,
        )
    else:
        raise ValueError(f"Unknown model provider: {settings.MODEL_PROVIDER}")


def create_agent(platform: str = "default"):
    settings.validate_api_keys()

    memory = MemorySaver()
    model = get_llm_model()
    prompt = get_platform_prompt(platform)

    try:
        tools = [get_search_tool(), get_sheets_tool()]
        return create_react_agent(
            model, tools, state_modifier=prompt, checkpointer=memory
        )
    except Exception as e:
        print(f"Error creating agent: {str(e)}")
        raise

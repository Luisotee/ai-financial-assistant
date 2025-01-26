from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import Tool
from src.core.config import settings
import os


def get_search_tool():
    # Set environment variable
    os.environ["SERPER_API_KEY"] = settings.SERPER_API_KEY

    # Initialize search wrapper
    search = GoogleSerperAPIWrapper()

    # Create and return tool
    return Tool(
        name="Search",
        func=search.run,
        description="Search tool for finding information on the internet",
    )

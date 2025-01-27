from langchain_core.tools import Tool
from src.services.google_sheets_service import GoogleSheetsService


def get_sheets_tool():
    sheets_service = GoogleSheetsService()

    def add_transaction(input_str: str) -> str:
        """Add a transaction to Google Sheets. Input format: 'name|value|description'"""
        try:
            name, value, description = input_str.split("|")
            value = float(value)

            success = sheets_service.add_transaction(name, value, description)

            if success:
                return f"Successfully added transaction: {name} - {value}"
            return "Failed to add transaction"
        except Exception as e:
            return f"Error processing transaction: {str(e)}"

    return Tool(
        name="add_transaction",
        func=add_transaction,
        description="Add a transaction to Google Sheets. Input should be in format: 'name|value|description'",
    )

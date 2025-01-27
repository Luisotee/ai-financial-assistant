from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from src.services.google_sheets_service import GoogleSheetsService
from typing import Optional


class TransactionInput(BaseModel):
    name: str = Field(..., description="Name or title of the transaction")
    value: float = Field(
        ...,
        description="Transaction amount (positive for income, negative for expenses)",
    )
    description: str = Field(..., description="Description of the transaction")


def get_sheets_tool():
    sheets_service = GoogleSheetsService()

    @StructuredTool.from_function
    def add_transaction(
        name: str = Field(..., description="Name of transaction"),
        value: float = Field(..., description="Transaction amount"),
        description: str = Field(..., description="Transaction description"),
    ) -> str:
        """Add a financial transaction to Google Sheets with name, value, and description."""
        try:
            success = sheets_service.add_transaction(name, value, description)
            if success:
                return f"✅ Added transaction: {name} - ${abs(value)}"
            return "❌ Failed to add transaction"
        except Exception as e:
            return f"Error: {str(e)}"

    return add_transaction

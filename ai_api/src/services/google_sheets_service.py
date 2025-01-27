from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
from typing import Optional
import os
from src.core.config import settings
from pathlib import Path


class GoogleSheetsService:
    def __init__(self):
        # Get base project directory (3 levels up from service file)
        base_dir = Path(__file__).parent.parent.parent.parent
        creds_path = base_dir / settings.GOOGLE_ACCOUNT_FILE

        credentials = service_account.Credentials.from_service_account_file(
            str(creds_path),
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        self.service = build("sheets", "v4", credentials=credentials)
        self.spreadsheet_id = settings.GOOGLE_SPREADSHEET_ID

    def _ensure_sheet_exists(self):
        try:
            sheets_metadata = (
                self.service.spreadsheets()
                .get(spreadsheetId=self.spreadsheet_id)
                .execute()
            )

            sheet_exists = False
            for sheet in sheets_metadata.get("sheets", ""):
                if sheet.get("properties", {}).get("title") == "Transactions":
                    sheet_exists = True
                    break

            if not sheet_exists:
                body = {
                    "requests": [
                        {
                            "addSheet": {
                                "properties": {
                                    "title": "Transactions",
                                    "gridProperties": {
                                        "rowCount": 1000,
                                        "columnCount": 4,
                                    },
                                }
                            }
                        }
                    ]
                }
                self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.spreadsheet_id, body=body
                ).execute()

                # Add headers
                self._update_headers()

            return True
        except Exception as e:
            print(f"Error ensuring sheet exists: {str(e)}")
            return False

    def _update_headers(self):
        headers = [["Date", "Name", "Value", "Description"]]
        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range="Transactions!A1:D1",
            valueInputOption="RAW",
            body={"values": headers},
        ).execute()

    def _get_formatted_date(self) -> str:
        """Get current date formatted as DD/MM/YYYY HH:MM"""
        return datetime.now().strftime("%d/%m/%Y %H:%M")

    def _extract_value(self, value_str: str) -> float:
        """Extract numeric value from string, removing currency symbols"""
        try:
            # Remove currency symbols and whitespace
            clean_value = "".join(
                c for c in value_str if c.isdigit() or c in ".-"
            )
            return float(clean_value)
        except ValueError:
            return 0.0

    def add_transaction(
        self, name: str, value: float, description: str
    ) -> bool:
        try:
            if not self._ensure_sheet_exists():
                return False

            current_date = self._get_formatted_date()
            values = [[current_date, name, value, description]]
            body = {"values": values}

            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range="Transactions!A1",
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body=body,
            ).execute()

            return True
        except Exception as e:
            print(f"Error adding transaction: {str(e)}")
            return False

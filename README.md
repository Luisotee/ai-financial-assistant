# AI Financial Assistant (POC)

AI-powered financial assistant that processes banking notifications and automatically updates Google Spreadsheets. Uses Azure OpenAI's GPT for transaction processing and categorization.

**Note**: This is a Proof of Concept project. WhatsApp and Telegram integrations are currently under development.

## Features

- 🤖 AI transaction categorization
- 📊 Automated Google Sheets tracking
- 💬 Multi-platform support (WhatsApp*, Telegram*)
- 🔍 Merchant research capability
- 📱 REST API for integration

## Setup Guide

### 1. Clone & Install

```bash
git clone https://github.com/Luisotee/ai-financial-assistant.git
cd ai-financial-assistant
yarn install
```

### 2. Spreadsheet Setup

1. Duplicate template spreadsheet: [Financial Template](https://docs.google.com/spreadsheets/d/1WxZSIVV9yOpZxtmnuv_fQLgUcMkawrfK3fLbKy2fyF4/edit?usp=sharing)
2. Copy spreadsheet ID from URL: `docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`

### 3. Google Cloud Setup

1. Visit [Google Cloud Console](https://console.cloud.google.com)
2. Create/select project
3. Enable Google Sheets API
4. Create Service Account:
   ```
   IAM & Admin > Service Accounts > Create Service Account
   Name: ai-financial-sheets
   Role: Editor
   ```
5. Create & download JSON key:
   ```
   Service Account > Keys > Add Key > Create New Key > JSON
   ```
6. Save as credentials.json:
   ```bash
   mkdir -p credentials
   mv ~/Downloads/credentials.json credentials/
   ```
7. Share spreadsheet with service account email

### 4. Environment Setup

1. Copy

```
.env.example
```

to .env in ai_api folder and fill with your credentials:

```bash
cp ai_api/.env.example ai_api/.env
nano ai_api/.env
```

Required variables:

- AZURE_OPENAI_API_KEY - Your Azure OpenAI key
- AZURE_OPENAI_ENDPOINT - Your Azure endpoint
- SERPER_API_KEY - Google Serper API key
- GOOGLE_SPREADSHEET_ID - Your spreadsheet ID

## Usage

### Start Server

```bash
yarn dev:ai
```

### API Endpoints

```bash
# Add transaction
curl -X POST http://localhost:8000/chat/send \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Paid $42.50 at Starbucks",
    "user_id": "user123",
    "platform": "whatsapp"
  }'
```

### Transaction Format

Expenses:

```
🟥 💸 Merchant Name
Amount: -$XX.XX
Description: Transaction details
```

Income:

```
🟩 💰 Source Name
Amount: +$XX.XX
Description: Income details
```

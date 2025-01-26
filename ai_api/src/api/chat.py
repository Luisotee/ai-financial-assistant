from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from src.services.chat_service import ChatService  # Add this import

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)

chat_service = ChatService()


class ChatMessage(BaseModel):
    message: str = Field(
        ...,
        description="The message to send to the chatbot",
        example="Hello, how are you?",
    )
    user_id: str = Field(
        ...,
        description="Unique identifier for the user",
        example="user123",
    )
    platform: str = Field(
        ...,
        description="Platform where the message originated",
        example="whatsapp",
    )


class ChatResponse(BaseModel):
    response: str = Field(
        ...,
        description="The response from the chatbot",
        example="Hello! I'm doing well, thank you for asking. How can I help you today?",
    )


@router.post(
    "/send",
    response_model=ChatResponse,
    summary="Send a message to the chatbot",
    description="Sends a message to the chatbot and receives an AI-powered response",
    response_description="The chatbot's response to the message",
)
async def send_message(chat_message: ChatMessage):
    """
    Send a message to the chatbot:

    - **message**: The text message to send
    - **user_id**: Unique identifier for the user
    - **platform**: Platform where the message originated

    Returns the chatbot's response
    """
    try:
        response = await chat_service.process_message(
            chat_message.message,
            chat_message.user_id,
            chat_message.platform,
        )
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from langchain_core.messages import HumanMessage, AIMessage
from typing import AsyncIterator, List, Optional
from fastapi import HTTPException
from src.agents.react_agent import create_agent


class ChatService:
    def __init__(self):
        try:
            self.agent = create_agent()
            self.config = {"configurable": {"thread_id": "default"}}
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def process_message(
        self,
        message: str,
        user_id: str,
        platform: str,
    ) -> str:
        print(f"Processing message from {user_id} on {platform}: {message}")
        try:
            self.config = {
                "configurable": {
                    "thread_id": f"{platform}_{user_id}",
                    "user_id": user_id,
                    "platform": platform,
                }
            }

            messages = [HumanMessage(content=message)]
            response = await self.agent.ainvoke(
                {"messages": messages}, self.config
            )

            print(f"Response: {response}")

            # Extract the AI's response from returned messages
            if response and "messages" in response:
                ai_messages = [
                    msg
                    for msg in response["messages"]
                    if isinstance(msg, AIMessage)
                ]
                if ai_messages:
                    return ai_messages[-1].content

            raise ValueError("No AI response found in the message chain")

        except Exception as e:
            print(f"Error in process_message: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Agent error: {str(e)}"
            )

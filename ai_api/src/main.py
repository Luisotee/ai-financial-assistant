from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.chat import router as chat_router

app = FastAPI(
    title="AI Financial Assistant API",
    description="API for AI Financial Assistant interactions",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

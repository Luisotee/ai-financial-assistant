from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.chat import router as chat_router
from src.core.config import settings
import uvicorn

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


if __name__ == "__main__":
    port = settings.PORT
    print(f"\nServer running at:")
    print(f"  - API: http://localhost:{port}")
    print(f"  - Documentation: http://localhost:{port}/docs")
    uvicorn.run("src.main:app", host="localhost", port=port, reload=True)

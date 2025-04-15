from fastapi import FastAPI
from brobot.api.routes import scenario, session, websocket
from brobot.core.config import settings  # Ensure you have a settings configuration
from fastapi.middleware.cors import CORSMiddleware

# Create the FastAPI application instance
app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description="API for managing learning scenarios, chapters, and real-time conversations with the learning bot.",
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to restrict allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scenario.router, prefix="/scenarios", tags=["Scenarios"])
app.include_router(session.router, prefix="/sessions", tags=["Sessions"])
app.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Brobot, you're teacher assistant."}

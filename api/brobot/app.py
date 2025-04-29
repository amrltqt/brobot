from fastapi import FastAPI
from brobot.api.routes import scenario, session
from brobot.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description="API for managing learning scenarios, chapters, and real-time conversations with the learning bot.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scenario.router, prefix="/scenarios", tags=["Scenarios"])
app.include_router(session.router, prefix="/sessions", tags=["Sessions"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Brobot, your teacher assistant."}

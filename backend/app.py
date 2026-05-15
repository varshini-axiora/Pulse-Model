from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.survey import router as survey_router
from backend.database.db import init_db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Survey Generation System", version="1.0.0")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database
@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("Database initialized.")

# Include Routes
app.include_router(survey_router, tags=["Survey"])

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Survey Generation API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

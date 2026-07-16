from fastapi.responses import FileResponse
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware!
from router import router as lead_router
from ai_router import router as ai_optimizer_router

app = FastAPI(
    title="Unified Developer Suite",
    description="Gateway Router (Project 3) & AI Resume Optimizer (Project 1)",
    version="1.0.0"
)

# Configure CORS so your frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local development testing
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Register both project engines
app.include_router(lead_router)
app.include_router(ai_optimizer_router)

@app.get("/health")
def health_check():
    return {"status": "online", "suite": "fully active"}

@app.get("/")
def serve_frontend():
    return FileResponse("index.html", media_type="text/html")
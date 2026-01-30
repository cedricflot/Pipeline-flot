from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.weekly_report import router as weekly_router

app = FastAPI(
    title="Fleet Operational Risk API",
    version="1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weekly_router, prefix="/api")
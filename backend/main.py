# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import health, jobs, analyze

# backend/main.py 상단 import 근처에 추가

import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


DEFAULT_FRONTEND_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


def get_frontend_origins() -> list[str]:
    raw_origins = os.getenv("FRONTEND_ORIGINS", "")

    env_origins = [
        origin.strip()
        for origin in raw_origins.split(",")
        if origin.strip()
    ]

    return list(dict.fromkeys(DEFAULT_FRONTEND_ORIGINS + env_origins))

app = FastAPI(
    title="CareerFit AI",
    description="취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(jobs.router)
app.include_router(analyze.router)


@app.get("/")
def root():
    return {
        "message": "CareerFit AI 서버가 실행 중입니다."
    }
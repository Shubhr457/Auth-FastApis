from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.models.user import User
from app.routers.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(document_models=[User])
    yield


app = FastAPI(
    title="JWT Auth Service",
    description="Production-ready authentication API with access and refresh tokens",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth_router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

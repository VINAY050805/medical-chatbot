from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.routes.health import router as health_router
from app.routes.upload import router as upload_router
from app.routes.ask import router as ask_router



app = FastAPI(

    title=settings.APP_NAME,

    version=settings.APP_VERSION,

    description="Medical AI Assistant Backend"

)

app.add_middleware(

    CORSMiddleware,

    allow_origins=settings.CORS_ORIGINS,

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"],

)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(ask_router)


@app.get("/")

async def root():

    return {

        "message": "Medical AI Assistant API Running 🚀"

    }

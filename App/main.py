import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import luz_router

# Configuración
settings = get_settings()

# Crear app FastAPI
app = FastAPI(
    title=settings.app_name,
    description="API para cálculo de métricas de iluminación natural en espacios interiores",
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://preview--luz-natural-lab-13791.lovable.app",
        "https://lovableproject.com",
        "https://lovable.app"
    ],
    allow_origin_regex=r"https://.*\.lovableproject\.com|https://.*\.lovable\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(luz_router.router, prefix="/api/v1")

# Endpoint raíz


@app.get("/")
def root():
    return {
        "mensaje": "Calculadora Luz Natural API",
        "estado": "funcionando",
        "version": settings.version,
        "docs": "/docs"
    }

# Health check


@app.get("/health")
def health_check():
    return {"estado": "ok", "servicio": "calculadora_luz_natural"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )

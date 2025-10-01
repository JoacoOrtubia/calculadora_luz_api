import os
from functools import lru_cache
from typing import List


class Settings:
    """Configuración de la aplicación"""

    app_name: str = "Calculadora Luz Natural"
    version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    # CORS - Configurado para Lovable y desarrollo local
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://preview--luz-natural-lab-13791.lovable.app",
        "https://*.lovableproject.com",
        "https://lovableproject.com",
        "https://*.lovable.app",
        "https://lovable.app"
    ]

    # Límites de validación
    max_area_vidrio: float = 12.0  # m²
    min_altura: float = 0.25  # m
    max_altura: float = 3.0   # m
    min_ancho: float = 0.25   # m
    max_ancho: float = 4.0    # m
    min_tv: float = 0.1       # transmitancia visible
    max_tv: float = 0.9       # transmitancia visible

    # Archivos
    csv_filename: str = "datos_sudi_limpio.csv"
    images_folder: str = "images"


@lru_cache()
def get_settings() -> Settings:
    """Obtener configuración singleton"""
    return Settings()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graficos import obtener_datos_heatmap

app = FastAPI()

# Configuración temporal de CORS (permitir todos los orígenes)
app.add_middleware(
    CORSMiddleware,
    # ⚠️ En producción, reemplazar "*" por el dominio real
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada


class InputData(BaseModel):
    ancho: float
    largo: float
    altura: float
    orientation: str
    tv: float

# Endpoint de cálculo


@app.post("/calcular_luz")
def calcular_luz(data: InputData):
    resultado_lux = data.ancho * data.largo * data.altura * data.tv
    grafico_data = obtener_datos_heatmap()

    return {
        "resultado_lux": resultado_lux,
        "grafico_data": grafico_data
    }

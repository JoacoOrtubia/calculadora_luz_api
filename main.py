from fastapi import FastAPI
from pydantic import BaseModel
from graficos import obtener_datos_heatmap

app = FastAPI()


class InputData(BaseModel):
    ancho: float
    largo: float
    altura: float
    orientation: str
    tv: float


@app.post("/calcular_luz")
def calcular_luz(data: InputData):
    resultado_lux = data.ancho * data.largo * data.altura * data.tv
    grafico_data = obtener_datos_heatmap()

    return {
        "resultado_lux": resultado_lux,
        "grafico_data": grafico_data
    }

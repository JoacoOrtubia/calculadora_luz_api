from graficos import obtener_datos_grafico_sudi
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class InputData(BaseModel):
    ancho: float
    largo: float
    altura: float
    orientacion: str
    tv: float


@app.post("/calcular_luz")
def calcular_luz(data: InputData):
    resultado_lux = data.ancho * data.largo * data.altura * data.tv
    grafico_data = obtener_datos_grafico_sudi()

    return {
        "resultado_lux": resultado_lux,
        "grafico_data": grafico_data
    }

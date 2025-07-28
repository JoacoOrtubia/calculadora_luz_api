from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo que define los datos que recibimos


class InputData(BaseModel):
    ancho: float
    largo: float
    altura: float
    orientacion: str
    tv: float

# Endpoint que recibe los datos y devuelve el resultado


@app.post("/calcular_luz")
def calcular_luz(data: InputData):
    # Acá va tu cálculo real, por ahora usamos algo básico
    resultado_lux = data.ancho * data.largo * data.altura * data.tv

    # Datos ficticios para el gráfico (después los reemplazás con los reales)
    grafico_data = {
        "x": [1, 2, 3],
        "y": [4, 5, 6],
        "z": [7, 8, 9]
    }

    return {
        "resultado_lux": resultado_lux,
        "grafico_data": grafico_data
    }

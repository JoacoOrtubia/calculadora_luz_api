import pandas as pd
import os


def obtener_datos_grafico_sudi():
    ruta_archivo = os.path.join(os.path.dirname(
        __file__), "datos_sudi_limpio.csv")

    df = pd.read_csv(ruta_archivo)

    datos = {
        "x": df["area_vidrio"].tolist(),
        "y": df["tv"].tolist(),
        "z": df["yhat"].tolist(),
    }

    return datos

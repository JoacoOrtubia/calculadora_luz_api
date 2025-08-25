import pandas as pd
import os


def obtener_datos_heatmap():
    ruta_archivo = os.path.join(os.path.dirname(
        __file__), "datos_sudi_limpio.csv")
    df = pd.read_csv(ruta_archivo)

    heatmap_data = [
        [row["area_vidrio"], row["tv"], row["yhat"]]
        for _, row in df.iterrows()
    ]

    return heatmap_data

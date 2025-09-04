import pandas as pd
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "datos_sUDI_limpio.csv")


def get_heatmap_data():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            "No se encontró el archivo datos_sUDI_limpio.csv")

    df = pd.read_csv(CSV_PATH)
    return df[["area_vidrio", "tv", "yhat"]].values.tolist()


def predict_yhat_nearest(area_vidrio: float, tv: float) -> tuple[float, float, float]:
    df = pd.read_csv(CSV_PATH)

    df["dist"] = ((df["area_vidrio"] - area_vidrio) ** 2 +
                  (df["tv"] - tv) ** 2) ** 0.5
    df_sorted = df.sort_values("dist")

    if df_sorted.empty:
        raise ValueError("No se encontró un punto de predicción válido.")

    fila = df_sorted.iloc[0]
    return fila["yhat"], fila["area_vidrio"], fila["tv"]

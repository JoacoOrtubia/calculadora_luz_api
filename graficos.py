import pandas as pd
import os

# Detectar automáticamente el nombre correcto del CSV


def get_csv_path():
    possible_names = [
        "datos_sudi_limpio.csv",
        "datos_sUDI_limpio.csv"  # Tu versión actual
    ]

    for name in possible_names:
        full_path = os.path.join(os.path.dirname(__file__), name)
        if os.path.exists(full_path):
            return full_path

    # Si no encuentra ninguno, usar el nombre de tu archivo
    return os.path.join(os.path.dirname(__file__), "datos_sudi_limpio.csv")


CSV_PATH = get_csv_path()


def get_heatmap_data():
    """Obtiene datos del heatmap desde el CSV"""
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            f"No se encontró el archivo CSV en: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

    # Verificar columnas necesarias
    required_cols = ["area_vidrio", "tv", "yhat"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Columnas faltantes en CSV: {missing_cols}")

    return df[["area_vidrio", "tv", "yhat"]].values.tolist()


def predict_yhat_nearest(area_vidrio: float, tv: float) -> tuple[float, float, float]:
    """
    Predice yhat usando el punto más cercano en el dataset

    Args:
        area_vidrio: Área de vidrio en m²
        tv: Transmitancia visible (0-1)

    Returns:
        tuple: (yhat_predicho, area_vidrio_usado, tv_usado)
    """
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            f"No se encontró el archivo CSV en: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

    # Verificar que el dataframe no está vacío
    if df.empty:
        raise ValueError("El archivo CSV está vacío")

    # Calcular distancia euclidiana
    df["dist"] = ((df["area_vidrio"] - area_vidrio) ** 2 +
                  (df["tv"] - tv) ** 2) ** 0.5

    # Ordenar por distancia
    df_sorted = df.sort_values("dist")

    if df_sorted.empty:
        raise ValueError("No se encontró un punto de predicción válido.")

    # Tomar el punto más cercano
    fila = df_sorted.iloc[0]
    return float(fila["yhat"]), float(fila["area_vidrio"]), float(fila["tv"])


def get_data_stats():
    """Obtiene estadísticas básicas del dataset"""
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            f"No se encontró el archivo CSV en: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

    return {
        "total_records": len(df),
        "csv_path": CSV_PATH,
        "columns": list(df.columns),
        "area_vidrio_range": {
            "min": float(df["area_vidrio"].min()),
            "max": float(df["area_vidrio"].max()),
            "mean": float(df["area_vidrio"].mean())
        },
        "tv_range": {
            "min": float(df["tv"].min()),
            "max": float(df["tv"].max()),
            "mean": float(df["tv"].mean())
        },
        "yhat_range": {
            "min": float(df["yhat"].min()),
            "max": float(df["yhat"].max()),
            "mean": float(df["yhat"].mean())
        }
    }

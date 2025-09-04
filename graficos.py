import os
import pandas as pd
import numpy as np
from functools import lru_cache

CSV_FILENAME = "datos_sudi_limpio.csv"  # tu dataset


def _csv_path() -> str:
    return os.path.join(os.path.dirname(__file__), CSV_FILENAME)


@lru_cache(maxsize=1)
def _load_df() -> pd.DataFrame:
    path = _csv_path()
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    df = pd.read_csv(path)
    expected = {"area_vidrio", "tv", "yhat"}
    if not expected.issubset(df.columns):
        raise ValueError(
            f"CSV debe tener columnas {expected}, tiene {df.columns.tolist()}")
    return df.sort_values(["tv", "area_vidrio"]).reset_index(drop=True)


def get_heatmap_data():
    df = _load_df()
    return df[["area_vidrio", "tv", "yhat"]].values.tolist()


def predict_yhat_nearest(area_vidrio: float, tv: float) -> tuple[float, float, float]:
    df = _load_df()

    tv_min, tv_max = df["tv"].min(), df["tv"].max()
    av_min, av_max = df["area_vidrio"].min(), df["area_vidrio"].max()

    if not (tv_min <= tv <= tv_max):
        raise ValueError(f"tv fuera de rango [{tv_min}, {tv_max}]")
    if not (av_min <= area_vidrio <= av_max):
        raise ValueError(f"area_vidrio fuera de rango [{av_min}, {av_max}]")

    pts = df[["area_vidrio", "tv"]].values
    target = np.array([area_vidrio, tv])
    dists = np.linalg.norm(pts - target, axis=1)
    idx = int(np.argmin(dists))
    row = df.iloc[idx]

    return float(row["yhat"]), float(row["area_vidrio"]), float(row["tv"])

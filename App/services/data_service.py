import os
import base64
from typing import List, Tuple, Dict, Any
import pandas as pd
from app.config import get_settings

settings = get_settings()


class DataService:
    """Servicio para manejo de datos y archivos"""

    # Asociaciones de métricas con imágenes
    GRAPH_PATHS = {
        "DA": "Metrica-temporal-DA_heatmap (1).png",
        "UDI": "Metrica-temporal-UDI_heatmap (1).png",
        "sDA": "Metrica-espacial-sDA_heatmap (1).png",
        "sUDI": "Metrica-espacial-sUDI_heatmap (1).png",
        "DAv_zone": "Metricas-espaciales_temporales-Dav_zone (1).png"
    }

    def __init__(self):
        self.csv_path = self._get_csv_path()

    def _get_csv_path(self) -> str:
        """Detecta automáticamente la ruta del CSV"""
        possible_names = [
            settings.csv_filename,
            "datos_sUDI_limpio.csv"
        ]

        for name in possible_names:
            full_path = os.path.join(os.getcwd(), name)
            if os.path.exists(full_path):
                return full_path

        # Ruta por defecto
        return os.path.join(os.getcwd(), settings.csv_filename)

    def get_heatmap_data(self) -> List[List[float]]:
        """
        Obtiene datos del heatmap desde el CSV

        Returns:
            Lista de listas con [area_vidrio, tv, yhat]

        Raises:
            FileNotFoundError: Si no se encuentra el CSV
            ValueError: Si faltan columnas requeridas
        """
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(
                f"No se encontró el archivo CSV en: {self.csv_path}"
            )

        try:
            df = pd.read_csv(self.csv_path)
        except Exception as e:
            raise ValueError(f"Error leyendo el CSV: {str(e)}")

        # Verificar columnas necesarias
        required_cols = ["area_vidrio", "tv", "yhat"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Columnas faltantes en CSV: {missing_cols}")

        return df[required_cols].values.tolist()

    def predict_yhat_nearest(self, area_vidrio: float, tv: float) -> Tuple[float, float, float]:
        """
        Predice yhat usando el punto más cercano en el dataset

        Args:
            area_vidrio: Área de vidrio en m²
            tv: Transmitancia visible (0-1)

        Returns:
            Tuple: (yhat_predicho, area_vidrio_usado, tv_usado)

        Raises:
            FileNotFoundError: Si no se encuentra el CSV
            ValueError: Si el dataset está vacío o hay errores
        """
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(
                f"No se encontró el archivo CSV en: {self.csv_path}"
            )

        try:
            df = pd.read_csv(self.csv_path)
        except Exception as e:
            raise ValueError(f"Error leyendo el CSV: {str(e)}")

        # Verificar que el dataframe no esté vacío
        if df.empty:
            raise ValueError("El archivo CSV está vacío")

        # Verificar columnas necesarias
        required_cols = ["area_vidrio", "tv", "yhat"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Columnas faltantes en CSV: {missing_cols}")

        # Calcular distancia euclidiana
        df = df.copy()
        df["dist"] = ((df["area_vidrio"] - area_vidrio) ** 2 +
                      (df["tv"] - tv) ** 2) ** 0.5

        # Ordenar por distancia y tomar el más cercano
        df_sorted = df.sort_values("dist")

        if df_sorted.empty:
            raise ValueError("No se encontró un punto de predicción válido.")

        fila = df_sorted.iloc[0]
        return float(fila["yhat"]), float(fila["area_vidrio"]), float(fila["tv"])

    def get_model_sheet(self, metric: str) -> Dict[str, Any]:
        """
        Obtiene información de la métrica y su imagen en base64

        Args:
            metric: Nombre de la métrica (DA, UDI, etc.)

        Returns:
            Dict con información de la métrica
        """
        if metric not in self.GRAPH_PATHS:
            raise ValueError(
                f"Métrica inválida: {metric}. "
                f"Opciones válidas: {list(self.GRAPH_PATHS.keys())}"
            )

        filename = self.GRAPH_PATHS[metric]
        filepath = os.path.join(os.getcwd(), filename)

        # Si el archivo no existe, retornar error controlado
        if not os.path.exists(filepath):
            return {
                "metric": metric,
                "image_base64": None,
                "filename": filename,
                "error": f"Imagen no encontrada: {filename}",
                "description": self._get_metric_description(metric)
            }

        try:
            with open(filepath, "rb") as img_file:
                encoded_img = base64.b64encode(img_file.read()).decode("utf-8")

            return {
                "metric": metric,
                "image_base64": encoded_img,
                "filename": os.path.basename(filepath),
                "description": self._get_metric_description(metric)
            }

        except Exception as e:
            return {
                "metric": metric,
                "image_base64": None,
                "filename": filename,
                "error": f"Error al cargar imagen: {str(e)}",
                "description": self._get_metric_description(metric)
            }

    def _get_metric_description(self, metric: str) -> str:
        """Descripción amigable por cada métrica"""
        descriptions = {
            "DA": "Daylight Autonomy - Porcentaje de tiempo con nivel mínimo de luz natural.",
            "UDI": "Useful Daylight Illuminance - Luz útil entre 100 y 2000 lux.",
            "sDA": "Spatial Daylight Autonomy - Porcentaje del espacio que cumple DA.",
            "sUDI": "Spatial Useful Daylight Illuminance - UDI aplicada a superficie.",
            "DAv_zone": "DA combinada con superficie y zona - Enfoque híbrido de tiempo y espacio."
        }
        return descriptions.get(metric, f"Descripción de la métrica {metric}")

    def get_data_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas básicas del dataset

        Returns:
            Dict con estadísticas del CSV
        """
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(
                f"No se encontró el archivo CSV en: {self.csv_path}"
            )

        try:
            df = pd.read_csv(self.csv_path)
        except Exception as e:
            raise ValueError(f"Error leyendo el CSV: {str(e)}")

        if df.empty:
            return {
                "total_records": 0,
                "csv_path": self.csv_path,
                "error": "El archivo CSV está vacío"
            }

        stats = {
            "total_records": len(df),
            "csv_path": self.csv_path,
            "columns": list(df.columns)
        }

        # Agregar estadísticas de columnas específicas si existen
        if "area_vidrio" in df.columns:
            stats["area_vidrio_range"] = {
                "min": float(df["area_vidrio"].min()),
                "max": float(df["area_vidrio"].max()),
                "mean": float(df["area_vidrio"].mean())
            }

        if "tv" in df.columns:
            stats["tv_range"] = {
                "min": float(df["tv"].min()),
                "max": float(df["tv"].max()),
                "mean": float(df["tv"].mean())
            }

        if "yhat" in df.columns:
            stats["yhat_range"] = {
                "min": float(df["yhat"].min()),
                "max": float(df["yhat"].max()),
                "mean": float(df["yhat"].mean())
            }

        return stats

    def list_available_images(self) -> Dict[str, Dict]:
        """Devuelve información de disponibilidad de imágenes en disco"""
        result = {}
        current_dir = os.getcwd()

        for metric, filename in self.GRAPH_PATHS.items():
            full_path = os.path.join(current_dir, filename)
            result[metric] = {
                "filename": filename,
                "exists": os.path.exists(full_path),
                "path": full_path
            }

        return result

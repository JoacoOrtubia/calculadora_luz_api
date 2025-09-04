import os
import base64

GRAPH_PATHS = {
    "DA": "Metrica-temporal-DA_heatmap (1).png",
    "UDI": "Metrica-temporal-UDI_heatmap (1).png",
    "sDA": "Metrica-espacial-sDA_heatmap (1).png",
    "sUDI": "Metrica-espacial-sUDI_heatmap (1).png",
    "DAv_zone": "Metricas-espaciales_temporales-Dav_zone (1).png"
}


def get_model_sheet(metric: str) -> dict:
    """
    Obtiene la información del modelo y la imagen asociada

    Args:
        metric: La métrica solicitada (DA, UDI, sDA, sUDI, DAv_zone)

    Returns:
        dict: Información del modelo con imagen en base64
    """
    if metric not in GRAPH_PATHS:
        raise ValueError(
            f"Métrica inválida: {metric}. Opciones válidas: {list(GRAPH_PATHS.keys())}")

    filepath = os.path.join(os.path.dirname(__file__), GRAPH_PATHS[metric])

    # Si el archivo de imagen no existe, devolver info sin imagen
    if not os.path.exists(filepath):
        return {
            "metric": metric,
            "image_base64": None,
            "filename": GRAPH_PATHS[metric],
            "error": f"Imagen no encontrada: {GRAPH_PATHS[metric]}",
            "description": get_metric_description(metric)
        }

    try:
        with open(filepath, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")

        return {
            "metric": metric,
            "image_base64": encoded,
            "filename": os.path.basename(filepath),
            "description": get_metric_description(metric)
        }

    except Exception as e:
        return {
            "metric": metric,
            "image_base64": None,
            "filename": GRAPH_PATHS[metric],
            "error": f"Error al cargar imagen: {str(e)}",
            "description": get_metric_description(metric)
        }


def get_metric_description(metric: str) -> str:
    """Devuelve descripción de la métrica"""
    descriptions = {
        "DA": "Daylight Autonomy - Porcentaje del tiempo que se cumple el nivel mínimo de iluminación",
        "UDI": "Useful Daylight Illuminance - Iluminancia útil entre 100-2000 lux",
        "sDA": "Spatial Daylight Autonomy - DA espacial en el 50% del espacio",
        "sUDI": "Spatial Useful Daylight Illuminance - UDI espacial",
        "DAv_zone": "Daylight Autonomy por zona - DA promedio por zona espacial"
    }
    return descriptions.get(metric, f"Descripción de métrica {metric}")


def list_available_images() -> dict:
    """Lista las imágenes disponibles en el directorio"""
    current_dir = os.path.dirname(__file__)
    available = {}

    for metric, filename in GRAPH_PATHS.items():
        filepath = os.path.join(current_dir, filename)
        available[metric] = {
            "filename": filename,
            "exists": os.path.exists(filepath),
            "path": filepath
        }

    return available

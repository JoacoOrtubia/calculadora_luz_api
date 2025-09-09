import os
import base64

# Asociaciones de métricas con imágenes
GRAPH_PATHS = {
    "DA": "Metrica-temporal-DA_heatmap (1).png",
    "UDI": "Metrica-temporal-UDI_heatmap (1).png",
    "sDA": "Metrica-espacial-sDA_heatmap (1).png",
    "sUDI": "Metrica-espacial-sUDI_heatmap (1).png",
    "DAv_zone": "Metricas-espaciales_temporales-Dav_zone (1).png"
}


def get_model_sheet(metric: str) -> dict:
    """
    Devuelve un diccionario con la información de la métrica y la imagen en base64.

    Args:
        metric (str): Una de las métricas: DA, UDI, sDA, sUDI, DAv_zone

    Returns:
        dict: Contenido de la hoja del modelo
    """
    if metric not in GRAPH_PATHS:
        raise ValueError(
            f"Métrica inválida: {metric}. Opciones válidas: {list(GRAPH_PATHS.keys())}")

    filepath = os.path.join(os.path.dirname(__file__), GRAPH_PATHS[metric])

    # Si el archivo no existe, retorna un error controlado
    if not os.path.exists(filepath):
        return {
            "metric": metric,
            "image_base64": None,
            "filename": GRAPH_PATHS[metric],
            "error": f"Imagen no encontrada: {GRAPH_PATHS[metric]}",
            "description": get_metric_description(metric)
        }

    try:
        with open(filepath, "rb") as img_file:
            encoded_img = base64.b64encode(img_file.read()).decode("utf-8")

        return {
            "metric": metric,
            "image_base64": encoded_img,
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
    """Descripción amigable por cada métrica"""
    descriptions = {
        "DA": "Daylight Autonomy - Porcentaje de tiempo con nivel mínimo de luz natural.",
        "UDI": "Useful Daylight Illuminance - Luz útil entre 100 y 2000 lux.",
        "sDA": "Spatial Daylight Autonomy - Porcentaje del espacio que cumple DA.",
        "sUDI": "Spatial Useful Daylight Illuminance - UDI aplicada a superficie.",
        "DAv_zone": "DA combinada con superficie y zona - Enfoque híbrido de tiempo y espacio."
    }
    return descriptions.get(metric, f"Descripción de la métrica {metric}")


def list_available_images() -> dict:
    """Devuelve info de disponibilidad de imágenes en disco"""
    current_dir = os.path.dirname(__file__)
    result = {}

    for metric, filename in GRAPH_PATHS.items():
        full_path = os.path.join(current_dir, filename)
        result[metric] = {
            "filename": filename,
            "exists": os.path.exists(full_path),
            "path": full_path
        }

    return result

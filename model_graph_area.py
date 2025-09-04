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
    if metric not in GRAPH_PATHS:
        raise ValueError(f"Métrica inválida: {metric}")

    filepath = os.path.join(os.path.dirname(__file__), GRAPH_PATHS[metric])
    if not os.path.exists(filepath):
        raise ValueError(f"No se encontró la imagen: {filepath}")

    with open(filepath, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")

    return {
        "metric": metric,
        "image_base64": encoded,
        "filename": os.path.basename(filepath)
    }

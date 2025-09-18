"""
Módulo para manejo de colores según métricas y porcentajes.
Cada métrica tiene su propia paleta de colores basada en rangos específicos.
"""


def obtener_color_da(percent: float) -> str:
    """Color para métrica DA (Daylight Autonomy)"""
    if percent < 50:
        return "#3C8EEA"  # Azul
    elif 50 <= percent < 60:
        return "#75D766"  # Verde
    elif 60 <= percent < 70:
        return "#C8A443"  # Amarillo
    elif 70 <= percent < 80:
        return "#E07060"  # Naranja claro
    elif 80 <= percent < 90:
        return "#E74847"  # Rojo
    else:  # >= 90
        return "#DA3DA5"  # Magenta


def obtener_color_udi(percent: float) -> str:
    """Color para métrica UDI (Useful Daylight Illuminance)"""
    if percent < 50:
        return "#3C8EEA"  # Azul
    elif 50 <= percent < 60:
        return "#75D766"  # Verde
    elif 60 <= percent < 70:
        return "#C8A443"  # Amarillo
    elif 70 <= percent < 80:
        return "#E07060"  # Naranja claro
    elif 80 <= percent < 90:
        return "#E74847"  # Rojo
    else:  # >= 90
        return "#DA3DA5"  # Magenta


def obtener_color_sda(percent: float) -> str:
    """Color para métrica sDA (Spatial Daylight Autonomy)"""
    if percent < 55:
        return "#3C8EEA"  # Azul
    elif 55 <= percent < 75:
        return "#C8A443"  # Amarillo
    else:  # >= 75
        return "#E04196"  # Rosa/Magenta


def obtener_color_sudi(percent: float) -> str:
    """Color para métrica sUDI (Spatial Useful Daylight Illuminance)"""
    if percent < 75:
        return "#31ADD7"  # Cian
    elif 75 <= percent < 95:
        return "#E74847"  # Rojo
    elif percent >= 95:
        return "#D33AB4"  # Magenta
    return "#D5D5D5"  # Gris por defecto


def obtener_color_dav_zone(percent: float) -> str:
    """Color para métrica DAv_zone"""
    # Usa la misma lógica que sUDI por ahora
    return obtener_color_sudi(percent)


def obtener_color_hex(metrica: str, porcentaje: float) -> str:
    """
    Devuelve el color HEX correspondiente según la métrica y porcentaje.

    Args:
        metrica: Nombre de la métrica (DA, UDI, sDA, sUDI, DAv_zone)
        porcentaje: Valor porcentual de la métrica

    Returns:
        String con el color en formato hexadecimal
    """
    metrica_lower = metrica.lower()

    color_functions = {
        "da": obtener_color_da,
        "udi": obtener_color_udi,
        "sda": obtener_color_sda,
        "sudi": obtener_color_sudi,
        "dav_zone": obtener_color_dav_zone
    }

    color_func = color_functions.get(metrica_lower)
    if color_func:
        return color_func(porcentaje)

    return "#CCCCCC"  # Color por defecto para métricas no reconocidas


def get_color_legend(metrica: str) -> dict:
    """
    Obtiene la leyenda de colores para una métrica específica

    Args:
        metrica: Nombre de la métrica

    Returns:
        Dict con rangos y colores correspondientes
    """
    legends = {
        "DA": [
            {"rango": "< 50%", "color": "#3C8EEA", "descripcion": "Insuficiente"},
            {"rango": "50-59%", "color": "#75D766", "descripcion": "Aceptable"},
            {"rango": "60-69%", "color": "#C8A443", "descripcion": "Bueno"},
            {"rango": "70-79%", "color": "#E07060", "descripcion": "Muy bueno"},
            {"rango": "80-89%", "color": "#E74847", "descripcion": "Excelente"},
            {"rango": "≥ 90%", "color": "#DA3DA5", "descripcion": "Excesivo"}
        ],
        "UDI": [
            {"rango": "< 50%", "color": "#3C8EEA", "descripcion": "Insuficiente"},
            {"rango": "50-59%", "color": "#75D766", "descripcion": "Aceptable"},
            {"rango": "60-69%", "color": "#C8A443", "descripcion": "Bueno"},
            {"rango": "70-79%", "color": "#E07060", "descripcion": "Muy bueno"},
            {"rango": "80-89%", "color": "#E74847", "descripcion": "Excelente"},
            {"rango": "≥ 90%", "color": "#DA3DA5", "descripcion": "Excesivo"}
        ],
        "sDA": [
            {"rango": "< 55%", "color": "#3C8EEA", "descripcion": "Insuficiente"},
            {"rango": "55-74%", "color": "#C8A443", "descripcion": "Aceptable"},
            {"rango": "≥ 75%", "color": "#E04196", "descripcion": "Óptimo"}
        ],
        "sUDI": [
            {"rango": "< 75%", "color": "#31ADD7", "descripcion": "Insuficiente"},
            {"rango": "75-94%", "color": "#E74847", "descripcion": "Aceptable"},
            {"rango": "≥ 95%", "color": "#D33AB4", "descripcion": "Excesivo"}
        ],
        "DAv_zone": [
            {"rango": "< 75%", "color": "#31ADD7", "descripcion": "Insuficiente"},
            {"rango": "75-94%", "color": "#E74847", "descripcion": "Aceptable"},
            {"rango": "≥ 95%", "color": "#D33AB4", "descripcion": "Excesivo"}
        ]
    }

    return legends.get(metrica, [])


def obtener_color_heatmap(yhat_value: float) -> str:
    """
    Genera color para el heatmap basado en el valor yhat.

    Args:
        yhat_value: Valor yhat del punto del heatmap

    Returns:
        String con el color en formato hexadecimal
    """
    if yhat_value < 10:
        return "#0D47A1"  # Azul muy oscuro
    elif yhat_value < 20:
        return "#1565C0"  # Azul oscuro
    elif yhat_value < 30:
        return "#1976D2"  # Azul
    elif yhat_value < 40:
        return "#2196F3"  # Azul claro
    elif yhat_value < 50:
        return "#42A5F5"  # Azul muy claro
    elif yhat_value < 60:
        return "#FFC107"  # Amarillo
    elif yhat_value < 70:
        return "#FF9800"  # Naranja
    elif yhat_value < 80:
        return "#FF5722"  # Naranja oscuro
    elif yhat_value < 90:
        return "#F44336"  # Rojo
    else:  # >= 90
        return "#B71C1C"  # Rojo muy oscuro


def generar_colores_heatmap(heatmap_data: list) -> list:
    """
    Genera array de colores para cada punto del heatmap.

    Args:
        heatmap_data: Lista de listas con [area_vidrio, tv, yhat]

    Returns:
        Lista de colores hexadecimales correspondientes a cada punto
    """
    colores = []
    for punto in heatmap_data:
        if len(punto) >= 3:
            yhat_value = punto[2]  # El tercer elemento es yhat
            color = obtener_color_heatmap(yhat_value)
            colores.append(color)
        else:
            colores.append("#CCCCCC")  # Color por defecto si no hay yhat

    return colores

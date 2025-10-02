"""
Módulo para manejo de colores según métricas y porcentajes.
Cada métrica tiene su propia paleta de colores basada en rangos específicos.
"""


def obtener_color_da(percent: float) -> str:
    """Color para métrica DA (Daylight Autonomy) - Métricas Temporales"""
    if percent < 50:
        return "#735FF1"  # Violeta - < 50%
    elif 50 <= percent < 60:
        return "#339CE5"  # Azul - [50%, 60%)
    elif 60 <= percent < 70:
        return "#42DA97"  # Verde - [60%, 70%)
    elif 70 <= percent < 80:
        return "#9EB054"  # Amarillo-verde - [70%, 80%)
    elif 80 <= percent < 90:
        return "#C8A443"  # Amarillo - [80%, 90%)
    else:  # >= 90
        return "#E74487"  # Magenta - >= 90%


def obtener_color_udi(percent: float) -> str:
    """Color para métrica UDI (Useful Daylight Illuminance) - Métricas Temporales"""
    if percent < 50:
        return "#735FF1"  # Violeta - < 50%
    elif 50 <= percent < 60:
        return "#339CE5"  # Azul - [50%, 60%)
    elif 60 <= percent < 70:
        return "#42DA97"  # Verde - [60%, 70%)
    elif 70 <= percent < 80:
        return "#9EB054"  # Amarillo-verde - [70%, 80%)
    elif 80 <= percent < 90:
        return "#C8A443"  # Amarillo - [80%, 90%)
    else:  # >= 90
        return "#E74487"  # Magenta - >= 90%


def obtener_color_sda(percent: float) -> str:
    """Color para métrica sDA (Spatial Daylight Autonomy) - Métricas Espaciales"""
    if percent < 55:
        return "#735FF1"  # Violeta - < 55%
    elif 55 <= percent < 75:
        return "#42DA97"  # Verde - [55%, 75%)
    else:  # >= 75
        return "#C8A443"  # Amarillo - >= 75%


def obtener_color_sudi(percent: float) -> str:
    """Color para métrica sUDI (Spatial Useful Daylight Illuminance) - Métricas Espaciales"""
    if percent < 75:
        return "#735FF1"  # Violeta - < 75%
    elif 75 <= percent < 95:
        return "#E74487"  # Magenta - [75%, 95%)
    elif percent >= 95:
        return "#D33AB4"  # Magenta oscuro - >= 95%
    return "#D5D5D5"  # Gris - Hybrid zone


def obtener_color_dav_zone(percent: float) -> str:
    """Color para métrica DAv_zone (zonas de disponibilidad)"""
    # Availability zones basadas en el gráfico de referencia
    # Usar gradiente continuo de verde claro a verde oscuro
    if percent < 50:  # Availability 1
        return "#B8D68B"  # Verde claro - Availability 1
    elif 50 <= percent < 75:  # Availability 2
        return "#42DA97"  # Verde - Availability 2
    else:  # Conditional availability
        return "#D5D5D5"  # Gris - Conditional availability


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
            {"rango": "< 50%", "color": "#735FF1", "descripcion": "Insuficiente"},
            {"rango": "[50%, 60%)", "color": "#339CE5", "descripcion": "Aceptable"},
            {"rango": "[60%, 70%)", "color": "#42DA97", "descripcion": "Bueno"},
            {"rango": "[70%, 80%)", "color": "#9EB054", "descripcion": "Muy bueno"},
            {"rango": "[80%, 90%)", "color": "#C8A443", "descripcion": "Excelente"},
            {"rango": ">= 90%", "color": "#E74487", "descripcion": "Excesivo"}
        ],
        "UDI": [
            {"rango": "< 50%", "color": "#735FF1", "descripcion": "Insuficiente"},
            {"rango": "[50%, 60%)", "color": "#339CE5", "descripcion": "Aceptable"},
            {"rango": "[60%, 70%)", "color": "#42DA97", "descripcion": "Bueno"},
            {"rango": "[70%, 80%)", "color": "#9EB054", "descripcion": "Muy bueno"},
            {"rango": "[80%, 90%)", "color": "#C8A443", "descripcion": "Excelente"},
            {"rango": ">= 90%", "color": "#E74487", "descripcion": "Excesivo"}
        ],
        "sDA": [
            {"rango": "< 55%", "color": "#735FF1", "descripcion": "Insuficiente"},
            {"rango": "[55%, 75%)", "color": "#42DA97", "descripcion": "Aceptable"},
            {"rango": ">= 75%", "color": "#C8A443", "descripcion": "Óptimo"}
        ],
        "sUDI": [
            {"rango": "< 75%", "color": "#735FF1", "descripcion": "Insuficiente"},
            {"rango": "[75%, 95%)", "color": "#E74487", "descripcion": "Aceptable"},
            {"rango": ">= 95%", "color": "#D33AB4", "descripcion": "Excesivo"},
            {"rango": "Hybrid zone", "color": "#D5D5D5", "descripcion": "Zona híbrida"}
        ],
        "DAv_zone": [
            {"rango": "Availability 1", "color": "#B8D68B", "descripcion": "Disponibilidad 1"},
            {"rango": "Availability 2", "color": "#42DA97", "descripcion": "Disponibilidad 2"},
            {"rango": "Conditional availability", "color": "#D5D5D5", "descripcion": "Disponibilidad condicional"}
        ]
    }

    return legends.get(metrica, [])


def generar_colores_por_rangos(metrica: str, valores: list) -> list:
    """
    Genera array de colores usando rangos discretos para métricas individuales

    Args:
        metrica: Nombre de la métrica (DA, UDI, sDA, sUDI)
        valores: Lista de valores de la métrica

    Returns:
        Lista de colores según rangos discretos
    """
    colores = []
    for valor in valores:
        color = obtener_color_hex(metrica, valor)
        colores.append(color)
    return colores


def generar_colores_metrica_heatmap(metrica: str, valores: list) -> list:
    """Genera colores específicos para heatmap de métricas"""
    return generar_colores_por_rangos(metrica, valores)


def generar_colores_heatmap(valores: list) -> list:
    """Genera colores para heatmap general"""
    # Usar una métrica por defecto o colores graduales
    return ["#735FF1"] * len(valores)
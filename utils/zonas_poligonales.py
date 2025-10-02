"""
Módulo para definición de zonas poligonales según especificación del cliente.
Basado en model_graph-area.py proporcionado por el cliente.
"""

from utils.colores import obtener_color_hex


def get_da_zones():
    """Zonas poligonales para DA (Daylight Autonomy)"""
    areas_puntos = [
        [(0.25, 0.1), (0.25, 0.9), (0.55, 0.9), (0.55, 0.45), (1.5, 0.45), (1.5, 0.35), (3.3, 0.35), (3.3, 0.15), (5.9, 0.15), (5.9, 0.1)],  # DA < 50%
        [(0.55, 0.45), (0.55, 0.9), (1.5, 0.9), (1.5, 0.45)],  # DA 50%-60%
        [(5.9, 0.15), (12, 0.15), (12, 0.1), (5.9, 0.1)],  # DA 60%-70%
        [(1.5, 0.35), (1.5, 0.9), (3.3, 0.9), (3.3, 0.35)],  # DA 70%-80%
        [(3.3, 0.15), (3.3, 0.35), (12, 0.35), (12, 0.15)],  # DA 80%-90%
        [(3.3, 0.15), (3.3, 0.35), (12, 0.35), (12, 0.15)],  # DA 80%-90% (duplicado en original)
        [(3.3, 0.35), (3.3, 0.9), (12, 0.9), (12, 0.35)],  # DA >= 90%
    ]
    metric_values = [30, 55, 65, 75, 85, 85, 91]

    zones = []
    for polygon, value in zip(areas_puntos, metric_values):
        zones.append({
            "polygon": polygon,
            "value": value,
            "color": obtener_color_hex("DA", value)
        })
    return zones


def get_udi_zones():
    """Zonas poligonales para UDI (Useful Daylight Illuminance)"""
    areas_puntos = [
        [(0.25, 0.1), (0.25, 0.9), (1.1, 0.9), (1.1, 0.35), (2, 0.35), (2, 0.25), (3, 0.25), (3, 0.15), (5.9, 0.15), (5.9, 0.1)],  # UDI < 50%
        [(6.1, 0.65), (6.1, 0.9), (12, 0.9), (12, 0.55), (8, 0.55), (8, 0.65)],  # UDI < 50%
        [(1.1, 0.35), (1.1, 0.65), (2, 0.65), (2, 0.35)],  # UDI 50%-60%
        [(5.9, 0.1), (5.9, 0.15), (12, 0.15), (12, 0.1)],  # UDI 50%-60%
        [(2, 0.25), (2, 0.55), (12, 0.55), (12, 0.15), (3, 0.15), (3, 0.25)],  # UDI 60%-70%
        [(1.1, 0.65), (1.1, 0.9), (6.1, 0.9), (6.1, 0.65)],  # UDI 60%-70%
        [(2, 0.55), (2, 0.65), (8, 0.65), (8.0, 0.55)]  # UDI 70%-80%
    ]
    metric_values = [25, 25, 55, 55, 65, 65, 75]

    zones = []
    for polygon, value in zip(areas_puntos, metric_values):
        zones.append({
            "polygon": polygon,
            "value": value,
            "color": obtener_color_hex("UDI", value)
        })
    return zones


def get_sda_zones():
    """Zonas poligonales para sDA (Spatial Daylight Autonomy)"""
    areas_puntos = [
        [(0.25, 0.1), (0.25, 0.9), (0.95, 0.9), (0.95, 0.55), (1.5, 0.55), (1.5, 0.35), (3, 0.35), (3, 0.15), (8, 0.15), (8, 0.1)],  # sDA < 55%
        [(0.95, 0.9), (0.95, 0.55), (1.5, 0.55), (1.5, 0.35), (3, 0.35), (3, 0.15), (8, 0.15), (8, 0.1), (12, 0.1), (12, 0.9)],  # sDA >= 75%
    ]
    metric_values = [25, 80]

    zones = []
    for polygon, value in zip(areas_puntos, metric_values):
        zones.append({
            "polygon": polygon,
            "value": value,
            "color": obtener_color_hex("sDA", value)
        })
    return zones


def get_sudi_zones():
    """Zonas poligonales para sUDI (Spatial Useful Daylight Illuminance)"""
    areas_puntos = [
        [(4.7, 0.75), (4.7, 0.9), (12, 0.9), (12, 0.45), (6.1, 0.45), (6.1, 0.75)],  # sUDI < 75%
        [(0.25, 0.1), (0.25, 0.9), (1.1, 0.9), (1.1, 0.45), (2.5, 0.45), (2.5, 0.25), (6.1, 0.25), (6.1, 0.15), (9.1, 0.15), (9.1, 0.1)],  # sUDI < 75%
        [(1.1, 0.45), (1.1, 0.9), (4.7, 0.9), (4.7, 0.75), (6.1, 0.75), (6.1, 0.45)],  # sUDI 75%-95%
        [(9.1, 0.1), (9.1, 0.15), (12, 0.15), (12, 0.1)],  # sUDI 75%-95%
        [(6.1, 0.35), (6.1, 0.45), (8.6, 0.45), (8.6, 0.35)],  # sUDI 75%-95%
        [(6.1, 0.15), (6.1, 0.25), (12, 0.25), (12, 0.15)],  # sUDI >= 95%
        [(2.5, 0.25), (2.5, 0.45), (6.1, 0.45), (6.1, 0.25)],  # Hybrid zone
        [(6.1, 0.25), (6.1, 0.35), (12, 0.35), (12, 0.25)],  # Hybrid zone
        [(8.6, 0.35), (8.6, 0.45), (12, 0.45), (12, 0.35)],  # Hybrid zone
    ]
    metric_values = [37, 37, 85, 85, 85, 97, 99, 99, 99]

    zones = []
    for polygon, value in zip(areas_puntos, metric_values):
        zones.append({
            "polygon": polygon,
            "value": value,
            "color": obtener_color_hex("sUDI", value)
        })
    return zones


def get_dav_zone_zones():
    """Zonas poligonales para DAv_zone (Zona mínima de disponibilidad)"""
    areas_puntos = [
        [(1.1, 0.45), (1.1, 0.9), (6.1, 0.9), (6.1, 0.65), (8, 0.65), (8, 0.55), (12, 0.55), (12, 0.1), (5.9, 0.1), (5.9, 0.15), (3.3, 0.15), (3.3, 0.35), (1.5, 0.35), (1.5, 0.45)],  # Availability 1
        [(1.1, 0.55), (1.1, 0.9), (4.7, 0.9), (4.7, 0.75), (6.1, 0.75), (6.1, 0.45), (12, 0.45), (12, 0.1), (8.6, 0.1), (8.6, 0.15), (6.1, 0.15), (6.1, 0.25), (3.3, 0.25), (3.3, 0.35), (2.5, 0.35), (2.5, 0.45), (1.5, 0.45), (1.5, 0.55)],  # Availability 2
        [(8.6, 0.35), (8.6, 0.45), (12, 0.45), (12, 0.35)],  # Conditional availability
    ]
    metric_values = [49, 61, 71]

    zones = []
    for polygon, value in zip(areas_puntos, metric_values):
        zones.append({
            "polygon": polygon,
            "value": value,
            "color": obtener_color_hex("DAv_zone", value)
        })
    return zones


def get_zones_by_metric(metric: str):
    """
    Obtiene las zonas poligonales para una métrica específica

    Args:
        metric: Nombre de la métrica (DA, UDI, sDA, sUDI, DAv_zone)

    Returns:
        Lista de zonas con polígonos, valores y colores
    """
    metric_lower = metric.lower()

    zone_functions = {
        "da": get_da_zones,
        "udi": get_udi_zones,
        "sda": get_sda_zones,
        "sudi": get_sudi_zones,
        "dav_zone": get_dav_zone_zones
    }

    zone_func = zone_functions.get(metric_lower)
    if zone_func:
        return zone_func()

    return []

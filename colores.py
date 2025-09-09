# colores.py

def obtener_color_da(percent: float) -> str:
    if percent < 50:
        return "#3C8EEA"
    elif 50 <= percent < 60:
        return "#75D766"
    elif 60 <= percent < 70:
        return "#C8A443"
    elif 70 <= percent < 80:
        return "#E07060"
    elif 80 <= percent < 90:
        return "#E74847"
    else:  # >= 90
        return "#DA3DA5"


def obtener_color_udi(percent: float) -> str:
    if percent < 50:
        return "#3C8EEA"
    elif 50 <= percent < 60:
        return "#75D766"
    elif 60 <= percent < 70:
        return "#C8A443"
    elif 70 <= percent < 80:
        return "#E07060"
    elif 80 <= percent < 90:
        return "#E74847"
    else:  # >= 90
        return "#DA3DA5"


def obtener_color_sda(percent: float) -> str:
    if percent < 55:
        return "#3C8EEA"
    elif 55 <= percent < 75:
        return "#C8A443"
    else:  # >= 75
        return "#E04196"


def obtener_color_sudi(percent: float) -> str:
    if percent < 75:
        return "#31ADD7"
    elif 75 <= percent < 95:
        return "#E74847"
    elif percent >= 95:
        return "#D33AB4"
    return "#D5D5D5"  # Hybrid zone fallback


def obtener_color_dav_zone(percent: float) -> str:
    # Por ahora vamos a usar misma lógica que sUDI
    return obtener_color_sudi(percent)


def obtener_color_hex(metrica: str, porcentaje: float) -> str:
    """
    Devuelve el color HEX correspondiente según la métrica y porcentaje.
    """
    metrica = metrica.lower()

    if metrica == "da":
        return obtener_color_da(porcentaje)
    elif metrica == "udi":
        return obtener_color_udi(porcentaje)
    elif metrica == "sda":
        return obtener_color_sda(porcentaje)
    elif metrica == "sudi":
        return obtener_color_sudi(porcentaje)
    elif metrica == "dav_zone":
        return obtener_color_dav_zone(porcentaje)
    else:
        return "#CCCCCC"  # Color por defecto

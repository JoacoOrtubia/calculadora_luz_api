# colores.py

def obtener_color_da(percent):
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


def obtener_color_udi(percent):
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


def obtener_color_sda(percent):
    if percent < 55:
        return "#3C8EEA"
    elif 55 <= percent < 75:
        return "#C8A443"
    else:  # >= 75
        return "#E04196"


def obtener_color_sudi(percent):
    if percent < 75:
        return "#31ADD7"
    elif 75 <= percent < 95:
        return "#E74847"
    elif percent >= 95:
        return "#D33AB4"
    return "#D5D5D5"  # Hybrid zone (por si se aplica manualmente)

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
    Usa degradé suave de 21 colores de violeta a magenta.

    Args:
        yhat_value: Valor yhat del punto del heatmap

    Returns:
        String con el color en formato hexadecimal
    """
    if yhat_value < 5:
        return "#8555F0"  # 0% - Violeta base
    elif yhat_value < 10:
        return "#7B4FE8"  # 5% - Violeta intermedio
    elif yhat_value < 15:
        return "#6B47DF"  # 10% - Violeta-azul
    elif yhat_value < 20:
        return "#5A3FD7"  # 15% - Azul-violeta
    elif yhat_value < 25:
        return "#4937CE"  # 20% - Azul base
    elif yhat_value < 30:
        return "#3B3BC8"  # 25% - Azul intermedio
    elif yhat_value < 35:
        return "#2D4FC2"  # 30% - Azul-cian
    elif yhat_value < 40:
        return "#1F63BC"  # 35% - Cian-azul
    elif yhat_value < 45:
        return "#31A0D7"  # 40% - Cian base
    elif yhat_value < 50:
        return "#2FB5C9"  # 45% - Cian-verde
    elif yhat_value < 55:
        return "#2DCABB"  # 50% - Verde-cian
    elif yhat_value < 60:
        return "#3BE0A5"  # 55% - Verde intermedio
    elif yhat_value < 65:
        return "#48F177"  # 60% - Verde base
    elif yhat_value < 70:
        return "#5EED6F"  # 65% - Verde-amarillo
    elif yhat_value < 75:
        return "#74E968"  # 70% - Amarillo-verde
    elif yhat_value < 80:
        return "#8AE560"  # 75% - Amarillo base
    elif yhat_value < 85:
        return "#A0E158"  # 80% - Amarillo-naranja
    elif yhat_value < 90:
        return "#C4DC4F"  # 85% - Naranja-amarillo
    elif yhat_value < 95:
        return "#E07060"  # 90% - Naranja base
    elif yhat_value < 100:
        return "#E85B85"  # 95% - Naranja-magenta
    else:  # >= 100
        return "#D33AB4"  # 100% - Magenta base


def obtener_color_heatmap_normalizado(valor_normalizado: float) -> str:
    """
    Genera color para el heatmap basado en valor normalizado 0-100.
    Distribuye los 21 colores uniformemente en el rango 0-100.

    Args:
        valor_normalizado: Valor entre 0 y 100

    Returns:
        String con el color en formato hexadecimal
    """
    # Asegurar que el valor esté en el rango 0-100
    valor = max(0, min(100, valor_normalizado))

    # Los 21 colores del degradé completo
    colores_degrade = [
        "#8555F0",  # 0% - Violeta base
        "#7B4FE8",  # 5% - Violeta intermedio
        "#6B47DF",  # 10% - Violeta-azul
        "#5A3FD7",  # 15% - Azul-violeta
        "#4937CE",  # 20% - Azul base
        "#3B3BC8",  # 25% - Azul intermedio
        "#2D4FC2",  # 30% - Azul-cian
        "#1F63BC",  # 35% - Cian-azul
        "#31A0D7",  # 40% - Cian base
        "#2FB5C9",  # 45% - Cian-verde
        "#2DCABB",  # 50% - Verde-cian
        "#3BE0A5",  # 55% - Verde intermedio
        "#48F177",  # 60% - Verde base
        "#5EED6F",  # 65% - Verde-amarillo
        "#74E968",  # 70% - Amarillo-verde
        "#8AE560",  # 75% - Amarillo base
        "#A0E158",  # 80% - Amarillo-naranja
        "#C4DC4F",  # 85% - Naranja-amarillo
        "#E07060",  # 90% - Naranja base
        "#E85B85",  # 95% - Naranja-magenta
        "#D33AB4"   # 100% - Magenta base
    ]

    # Calcular índice del color basado en el valor normalizado
    # Distribuir uniformemente los 21 colores en el rango 0-100
    indice = int((valor / 100) * (len(colores_degrade) - 1))
    indice = max(0, min(len(colores_degrade) - 1, indice))

    return colores_degrade[indice]


def generar_colores_heatmap(heatmap_data: list) -> list:
    """
    Genera array de colores para cada punto del heatmap usando el rango real de datos.
    Distribuye los 21 colores uniformemente sobre el rango min-max de valores yhat.

    Args:
        heatmap_data: Lista de listas con [area_vidrio, tv, yhat]

    Returns:
        Lista de colores hexadecimales correspondientes a cada punto
    """
    # Extraer todos los valores yhat válidos
    valores_yhat = []
    for punto in heatmap_data:
        if len(punto) >= 3:
            valores_yhat.append(punto[2])

    if not valores_yhat:
        return ["#CCCCCC"] * len(heatmap_data)

    # Calcular rango real de los datos
    min_yhat = min(valores_yhat)
    max_yhat = max(valores_yhat)

    # Evitar división por cero
    if max_yhat == min_yhat:
        return [obtener_color_heatmap_normalizado(50)] * len(heatmap_data)

    colores = []
    for punto in heatmap_data:
        if len(punto) >= 3:
            yhat_value = punto[2]
            # Normalizar al rango 0-100 según min-max real
            valor_normalizado = ((yhat_value - min_yhat) / (max_yhat - min_yhat)) * 100
            color = obtener_color_heatmap_normalizado(valor_normalizado)
            colores.append(color)
        else:
            colores.append("#CCCCCC")

    return colores

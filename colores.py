def get_color_for_metric(metric: str, percent: int) -> str:
    """
    Retorna el color HEX correspondiente a una métrica y su valor en porcentaje.

    Args:
        metric (str): Puede ser 'DA', 'UDI', 'sDA', 'sUDI'
        percent (int): Valor entre 0 y 100

    Returns:
        str: Código de color HEX
    """
    if metric in ["DA", "UDI"]:
        if percent < 50:
            return "#3C8EEA"  # Azul
        elif percent < 60:
            return "#75D766"  # Verde
        elif percent < 70:
            return "#C8A443"  # Amarillo
        elif percent < 80:
            return "#E07060"  # Naranja
        elif percent < 90:
            return "#E74847"  # Rojo
        else:  # 90–100
            return "#DA3DA5"  # Magenta

    elif metric == "sDA":
        if percent < 55:
            return "#3C8EEA"  # Azul
        elif percent < 75:
            return "#C8A443"  # Amarillo
        else:  # 75–100
            return "#E04196"  # Fucsia

    elif metric == "sUDI":
        if percent < 75:
            return "#31ADD7"  # Azul claro
        elif percent < 95:
            return "#E74847"  # Rojo
        else:  # 95–100
            return "#D33AB4"  # Violeta

    elif metric == "energia":
        return "#F5D94C"  # Amarillo energía fijo

    # Fallback si no se reconoce la métrica
    return "#CCCCCC"

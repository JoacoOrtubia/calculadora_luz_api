"""
Módulo para manejo de orientaciones de ventanas.
Convierte entre nombres completos y códigos de orientación.
"""

from typing import Optional


def traducir_orientacion(sigla: str) -> str:
    """
    Convierte código de orientación a nombre completo

    Args:
        sigla: Código de orientación (N, S, E, O, etc.)

    Returns:
        Nombre completo de la orientación
    """
    nombres = {
        "N": "Norte",
        "S": "Sur",
        "E": "Este",
        "O": "Oeste",
        "NE": "Noreste",
        "NO": "Noroeste",
        "SE": "Sudeste",
        "SO": "Sudoeste"
    }
    return nombres.get(sigla.upper(), sigla)


def codificar_orientacion(nombre: str) -> Optional[str]:
    """
    Convierte nombre completo a código de orientación

    Args:
        nombre: Nombre completo de la orientación

    Returns:
        Código de orientación o None si no se encuentra
    """
    if not nombre:
        return None

    traducciones = {
        "Norte": "N",
        "Sur": "S",
        "Este": "E",
        "Oeste": "O",
        "Noreste": "NE",
        "Noroeste": "NO",
        "Sudeste": "SE",
        "Sudoeste": "SO"
    }
    return traducciones.get(nombre.strip(), None)


def obtener_orientaciones_disponibles() -> dict:
    """
    Obtiene lista de orientaciones disponibles

    Returns:
        Dict con códigos y nombres de orientaciones
    """
    return {
        "N": "Norte",
        "S": "Sur",
        "E": "Este",
        "O": "Oeste",
        "NE": "Noreste",
        "NO": "Noroeste",
        "SE": "Sudeste",
        "SO": "Sudoeste"
    }


def validar_orientacion(orientacion: str) -> bool:
    """
    Valida si una orientación es válida

    Args:
        orientacion: Nombre o código de orientación

    Returns:
        True si es válida, False en caso contrario
    """
    if not orientacion:
        return False

    orientaciones_validas = obtener_orientaciones_disponibles()

    # Verificar si es un código válido
    if orientacion.upper() in orientaciones_validas:
        return True

    # Verificar si es un nombre válido
    if orientacion in orientaciones_validas.values():
        return True

    return False

import os
from typing import Literal
from fastapi import APIRouter, HTTPException, Query
from schemas.luz_schemas import (
    VentanaInput,
    LuzNaturalResponse,
    ModelSheetResponse,
    DebugResponse
)
from services.luz_service import LuzNaturalService
from services.data_service import DataService
from utils.orientacion import obtener_orientaciones_disponibles

# Crear router
router = APIRouter(tags=["Cálculo de Luz Natural"])

# Instanciar servicios
luz_service = LuzNaturalService()
data_service = DataService()


@router.post(
    "/calcular_luz",
    response_model=LuzNaturalResponse,
    summary="Calcular métricas de luz natural",
    description="""
    Calcula las métricas de iluminación natural para una ventana específica.
    
    Métricas calculadas:
    - **DA**: Daylight Autonomy
    - **UDI**: Useful Daylight Illuminance  
    - **sDA**: Spatial Daylight Autonomy
    - **sUDI**: Spatial Useful Daylight Illuminance
    - **DAv_zone**: DA combinada con superficie y zona
    
    También genera datos para heatmap compatible con ECharts.
    """
)
def calcular_luz(data: VentanaInput):
    """
    Endpoint principal para cálculo de luz natural
    """
    try:
        resultado = luz_service.procesar_calculo_luz(data)
        return LuzNaturalResponse(**resultado)

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=500, detail=f"Error cargando datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get(
    "/model_sheet",
    response_model=ModelSheetResponse,
    summary="Obtener gráfico de métrica",
    description="Devuelve la imagen del gráfico correspondiente a una métrica específica en formato base64."
)
def get_model_sheet(
    metric: Literal["DA", "UDI", "sDA", "sUDI", "DAv_zone"] = Query(
        ...,
        description="Métrica de la cual obtener el gráfico"
    )
):
    """
    Obtiene el gráfico de una métrica específica
    """
    try:
        sheet_data = data_service.get_model_sheet(metric)
        return ModelSheetResponse(**sheet_data)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get(
    "/orientaciones",
    summary="Obtener orientaciones disponibles",
    description="Lista todas las orientaciones válidas con sus códigos correspondientes."
)
def get_orientaciones():
    """
    Obtiene lista de orientaciones disponibles
    """
    return {
        "orientaciones": obtener_orientaciones_disponibles(),
        "descripcion": "Orientaciones válidas para ventanas"
    }


@router.get(
    "/estadisticas",
    summary="Estadísticas del dataset",
    description="Obtiene información estadística del dataset utilizado para predicciones."
)
def get_estadisticas():
    """
    Obtiene estadísticas del dataset
    """
    try:
        stats = data_service.get_data_stats()
        return {
            "estadisticas": stats,
            "descripcion": "Estadísticas del dataset de entrenamiento"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")


@router.get(
    "/imagenes_disponibles",
    summary="Verificar imágenes disponibles",
    description="Lista el estado de disponibilidad de las imágenes de métricas."
)
def get_imagenes_disponibles():
    """
    Verifica qué imágenes están disponibles
    """
    return {
        "imagenes": data_service.list_available_images(),
        "descripcion": "Estado de disponibilidad de imágenes por métrica"
    }


@router.get(
    "/debug",
    response_model=DebugResponse,
    summary="Información de debug",
    description="Información técnica para debugging del sistema."
)
def debug_info():
    """
    Información de debug del sistema
    """
    current_dir = os.getcwd()
    files = os.listdir(current_dir)
    csv_path = data_service.csv_path
    csv_exists = os.path.exists(csv_path)

    # Obtener estadísticas si el CSV existe
    estadisticas_csv = None
    if csv_exists:
        try:
            estadisticas_csv = data_service.get_data_stats()
        except Exception as e:
            estadisticas_csv = {"error": str(e)}

    return DebugResponse(
        directorio_actual=current_dir,
        archivos=files,
        csv_existe=csv_exists,
        ruta_csv=csv_path if csv_exists else None,
        estadisticas_csv=estadisticas_csv
    )

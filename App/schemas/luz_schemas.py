from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator
from app.config import get_settings

settings = get_settings()


class VentanaInput(BaseModel):
    """Esquema para datos de entrada de ventana"""

    alto: Optional[float] = Field(
        default=None,
        ge=settings.min_altura,
        le=settings.max_altura,
        description="Altura de la ventana en metros"
    )
    ancho: Optional[float] = Field(
        default=None,
        ge=settings.min_ancho,
        le=settings.max_ancho,
        description="Ancho de la ventana en metros"
    )
    tv: float = Field(
        ...,
        ge=settings.min_tv,
        le=settings.max_tv,
        description="Transmitancia visible (0.1-0.9)"
    )
    orientation: Optional[str] = Field(
        default=None,
        description="Orientación de la ventana (Norte, Sur, Este, Oeste, etc.)"
    )
    ubicacion: Optional[str] = Field(
        default=None,
        description="Ubicación del proyecto"
    )
    nombre_espacio: Optional[str] = Field(
        default=None,
        description="Nombre del espacio o habitación"
    )

    @field_validator("tv")
    @classmethod
    def validar_tv(cls, v):
        if v is None:
            raise ValueError(
                "El campo 'tv' (transmitancia visible) es obligatorio.")
        return v

    def area_vidrio(self) -> Optional[float]:
        """Calcular área de vidrio"""
        if self.ancho and self.alto:
            return round(self.ancho * self.alto, 4)
        return None


class MetricaOutput(BaseModel):
    """Esquema para salida de una métrica individual"""

    key: str = Field(description="Clave de la métrica (DA, UDI, etc.)")
    percent: int = Field(description="Porcentaje calculado")
    hex: str = Field(description="Color hexadecimal correspondiente")
    sheet: Dict[str, Any] = Field(
        description="Información de la imagen/gráfico")


class PuntoUsado(BaseModel):
    """Punto del dataset utilizado para la predicción"""

    area_vidrio: float = Field(description="Área de vidrio utilizada (m²)")
    tv: float = Field(description="Transmitancia visible utilizada")


class LuzNaturalResponse(BaseModel):
    """Esquema completo de respuesta de cálculo de luz natural"""

    ok: bool = Field(description="Indica si el cálculo fue exitoso")
    mensaje: str = Field(description="Mensaje descriptivo del resultado")
    yhat_pred: Optional[float] = Field(description="Predicción yhat calculada")
    punto_usado: Optional[PuntoUsado] = Field(
        description="Punto del dataset usado")
    heatmap_data: List[List[float]] = Field(
        description="Datos para generar heatmap")
    metrics: List[MetricaOutput] = Field(
        description="Lista de métricas calculadas")
    energia_pct: Optional[int] = Field(
        description="Porcentaje de energía calculado")
    orientacion_texto: Optional[str] = Field(
        description="Orientación en texto completo")
    orientacion_codigo: Optional[str] = Field(
        description="Código de orientación")
    ubicacion: Optional[str] = Field(description="Ubicación del proyecto")
    nombre_espacio: Optional[str] = Field(description="Nombre del espacio")


class ModelSheetResponse(BaseModel):
    """Esquema para respuesta de model sheet"""

    metric: str = Field(description="Nombre de la métrica")
    image_base64: Optional[str] = Field(description="Imagen en base64")
    filename: str = Field(description="Nombre del archivo")
    description: str = Field(description="Descripción de la métrica")
    error: Optional[str] = Field(description="Error si no se pudo cargar")


class DebugResponse(BaseModel):
    """Esquema para información de debug"""

    directorio_actual: str
    archivos: List[str]
    csv_existe: bool
    ruta_csv: Optional[str]
    estadisticas_csv: Optional[Dict[str, Any]]

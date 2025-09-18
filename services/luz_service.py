from typing import Dict, List, Optional, Tuple
from schemas.luz_schemas import VentanaInput, MetricaOutput, PuntoUsado
from services.data_service import DataService
from utils.colores import obtener_color_hex, generar_colores_heatmap
from utils.orientacion import codificar_orientacion


class LuzNaturalService:
    """Servicio principal para cálculos de luz natural"""

    def __init__(self):
        self.data_service = DataService()

    def calcular_metricas_desde_yhat(self, yhat: float) -> Dict[str, int]:
        """
        Calcula todas las métricas a partir del valor yhat predicho

        Args:
            yhat: Valor predicho del modelo

        Returns:
            Dict con las métricas calculadas
        """
        y = max(0, min(100, yhat))

        return {
            "DA": int(y),
            "UDI": int(min(100, y + 8)),
            "sDA": int(max(0, y - 13)),
            "sUDI": int(min(100, y + 4)),
            "DAv_zone": int(y),
            "energia": int(max(0, 100 - y)),
        }

    def generar_metricas_output(self, metricas: Dict[str, int]) -> List[MetricaOutput]:
        """
        Genera la lista de métricas con colores y sheets

        Args:
            metricas: Dict con los valores calculados

        Returns:
            Lista de MetricaOutput
        """
        resultado = []
        metricas_principales = ["DA", "UDI", "sDA", "sUDI", "DAv_zone"]

        for key in metricas_principales:
            if key in metricas:
                try:
                    sheet = self.data_service.get_model_sheet(key)
                    color_hex = obtener_color_hex(key, metricas[key])

                    resultado.append(MetricaOutput(
                        key=key,
                        percent=metricas[key],
                        hex=color_hex,
                        sheet=sheet
                    ))

                except Exception as e:
                    # Si hay error con la imagen, devolver info básica
                    resultado.append(MetricaOutput(
                        key=key,
                        percent=metricas[key],
                        hex=obtener_color_hex(key, metricas[key]),
                        sheet={"error": f"Error cargando imagen: {str(e)}"}
                    ))

        return resultado

    def procesar_calculo_luz(self, data: VentanaInput) -> Dict:
        """
        Procesa el cálculo completo de luz natural

        Args:
            data: Datos de entrada validados

        Returns:
            Dict con toda la respuesta
        """
        # Validar área máxima
        area_v = data.area_vidrio()
        if area_v is not None and area_v > 12.0:
            raise ValueError("Área de ventana no puede superar 12 m²")

        # Obtener datos del heatmap
        heatmap_data = self.data_service.get_heatmap_data()

        # Generar colores para el heatmap
        heatmap_colors = generar_colores_heatmap(heatmap_data)

        # Inicializar variables de respuesta
        yhat_pred = None
        punto_usado = None
        metrics = []
        energia_pct = None

        # Codificar orientación
        orient_sigla = codificar_orientacion(
            data.orientation) if data.orientation else None

        # Si tenemos área, hacer predicción
        if area_v is not None:
            try:
                yhat_pred, av_used, tv_used = self.data_service.predict_yhat_nearest(
                    area_v, data.tv
                )
                punto_usado = PuntoUsado(
                    area_vidrio=float(av_used),
                    tv=float(tv_used)
                )
            except Exception as e:
                raise ValueError(f"Error en predicción: {str(e)}")

        # Si tenemos predicción, calcular métricas
        if yhat_pred is not None:
            metricas_dict = self.calcular_metricas_desde_yhat(yhat_pred)
            metrics = self.generar_metricas_output(metricas_dict)
            energia_pct = metricas_dict["energia"]

        # Generar mensaje
        mensaje = (
            "Cálculo completado exitosamente"
            if yhat_pred is not None
            else "Heatmap generado. Ingresa medidas de ventana para ver tu predicción."
        )

        return {
            "ok": True,
            "mensaje": mensaje,
            "yhat_pred": yhat_pred,
            "punto_usado": punto_usado.dict() if punto_usado else None,
            "heatmap_data": heatmap_data,
            "heatmap_colors": heatmap_colors,
            "metrics": [metric.dict() for metric in metrics],
            "energia_pct": energia_pct,
            "orientacion_texto": data.orientation,
            "orientacion_codigo": orient_sigla,
            "ubicacion": data.ubicacion,
            "nombre_espacio": data.nombre_espacio
        }

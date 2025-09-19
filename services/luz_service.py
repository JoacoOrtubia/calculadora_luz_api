from typing import Dict, List, Optional, Tuple
from schemas.luz_schemas import VentanaInput, MetricaOutput, PuntoUsado
from services.data_service import DataService
from utils.colores import obtener_color_hex, generar_colores_heatmap, generar_colores_metrica_heatmap
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

    def generar_echarts_data(self, heatmap_data: List, heatmap_colors: List) -> List[Dict]:
        """
        Genera datos pre-formateados para ECharts con colores exactos

        Args:
            heatmap_data: Lista de puntos [area, tv, yhat]
            heatmap_colors: Lista de colores hexadecimales

        Returns:
            Lista de objetos listos para ECharts
        """
        echarts_data = []

        for i, punto in enumerate(heatmap_data):
            if i < len(heatmap_colors):
                echarts_data.append({
                    "value": [punto[0], punto[1], punto[2]],  # [área, tv, yhat]
                    "itemStyle": {
                        "color": heatmap_colors[i]
                    }
                })
            else:
                # Fallback si no hay color disponible
                echarts_data.append({
                    "value": [punto[0], punto[1], punto[2]],
                    "itemStyle": {
                        "color": "#CCCCCC"
                    }
                })

        return echarts_data

    def generar_echarts_heatmap_data(self, heatmap_data: List, heatmap_colors: List) -> Dict:
        """
        Genera datos para ECharts heatmap con índices de grilla y configuración completa

        Args:
            heatmap_data: Lista de puntos [area, tv, yhat]
            heatmap_colors: Lista de colores hexadecimales

        Returns:
            Dict con datos de heatmap, configuración de ejes y grilla
        """
        # Configuración de la grilla
        x_grid_size = 24  # Divisiones en X (área)
        y_grid_size = 16  # Divisiones en Y (TV)

        x_min, x_max = 0.25, 12.0
        y_min, y_max = 0.1, 0.9

        x_step = (x_max - x_min) / (x_grid_size - 1)
        y_step = (y_max - y_min) / (y_grid_size - 1)

        # Generar etiquetas de ejes
        x_labels = [f"{(x_min + i * x_step):.1f}" for i in range(x_grid_size)]
        y_labels = [f"{(y_min + i * y_step):.2f}" for i in range(y_grid_size)]

        # Transformar datos a índices de grilla
        heatmap_grid_data = []
        for i, punto in enumerate(heatmap_data):
            if len(punto) >= 3:
                area, tv, yhat = punto[0], punto[1], punto[2]

                # Convertir coordenadas continuas a índices de grilla
                x_index = round((area - x_min) / x_step)
                y_index = round((tv - y_min) / y_step)

                # Asegurar que estén dentro del rango
                x_index = max(0, min(x_grid_size - 1, x_index))
                y_index = max(0, min(y_grid_size - 1, y_index))

                heatmap_grid_data.append([x_index, y_index, yhat])

        return {
            "heatmap_data": heatmap_grid_data,
            "x_labels": x_labels,
            "y_labels": y_labels,
            "x_grid_size": x_grid_size,
            "y_grid_size": y_grid_size,
            "x_range": {"min": x_min, "max": x_max},
            "y_range": {"min": y_min, "max": y_max}
        }

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

        # Generar datos pre-formateados para ECharts (scatter original)
        echarts_data = self.generar_echarts_data(heatmap_data, heatmap_colors)

        # Generar datos para heatmap verdadero con índices de grilla
        echarts_heatmap = self.generar_echarts_heatmap_data(heatmap_data, heatmap_colors)

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
            "echarts_data": echarts_data,  # Datos scatter originales
            "echarts_heatmap": echarts_heatmap,  # NUEVO: Datos para heatmap verdadero
            "metrics": [metric.dict() for metric in metrics],
            "energia_pct": energia_pct,
            "orientacion_texto": data.orientation,
            "orientacion_codigo": orient_sigla,
            "ubicacion": data.ubicacion,
            "nombre_espacio": data.nombre_espacio
        }

    def generar_datos_metrica_individual(self, metrica: str) -> Dict:
        """
        Genera datos de heatmap para una métrica individual usando colores violeta-magenta.

        Args:
            metrica: Nombre de la métrica (DA, UDI, sDA, sUDI, DAv_zone)

        Returns:
            Dict con datos y colores para la métrica específica
        """
        # Obtener datos base del heatmap
        heatmap_data = self.data_service.get_heatmap_data()

        if not heatmap_data:
            return {
                "metrica": metrica,
                "heatmap_data": [],
                "colores_metrica": [],
                "echarts_data": [],
                "error": "No hay datos disponibles"
            }

        # Calcular valores de la métrica para cada punto del heatmap
        valores_metrica = []
        for punto in heatmap_data:
            if len(punto) >= 3:
                yhat_value = punto[2]
                metricas_dict = self.calcular_metricas_desde_yhat(yhat_value)
                valor_metrica = metricas_dict.get(metrica, 0)
                valores_metrica.append(valor_metrica)
            else:
                valores_metrica.append(0)

        # Generar colores usando el degradé violeta-magenta
        colores_metrica = generar_colores_metrica_heatmap(metrica, valores_metrica)

        # Generar datos pre-formateados para ECharts scatter (original)
        echarts_data = []
        for i, punto in enumerate(heatmap_data):
            if i < len(valores_metrica) and i < len(colores_metrica):
                echarts_data.append({
                    "value": [punto[0], punto[1], valores_metrica[i]],  # [área, tv, valor_metrica]
                    "itemStyle": {
                        "color": colores_metrica[i]
                    }
                })
            else:
                echarts_data.append({
                    "value": [punto[0], punto[1], 0],
                    "itemStyle": {
                        "color": "#CCCCCC"
                    }
                })

        # Generar datos para heatmap verdadero con índices de grilla
        echarts_heatmap = self.generar_echarts_heatmap_data(heatmap_data, colores_metrica)

        return {
            "metrica": metrica,
            "heatmap_data": heatmap_data,
            "valores_metrica": valores_metrica,
            "colores_metrica": colores_metrica,
            "echarts_data": echarts_data,  # Datos scatter originales
            "echarts_heatmap": echarts_heatmap,  # NUEVO: Datos para heatmap verdadero
            "rango_valores": {
                "min": min(valores_metrica) if valores_metrica else 0,
                "max": max(valores_metrica) if valores_metrica else 0
            }
        }
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
import os

from graficos import get_heatmap_data, predict_yhat_nearest
from model_graph_area import get_model_sheet
from colores import (
    obtener_color_da,
    obtener_color_udi,
    obtener_color_sda,
    obtener_color_sudi
)

app = FastAPI(title="Calculadora Luz Natural", version="1.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

Orient = Literal["N", "S", "E", "O", "NE", "NO", "SE", "SO"]

orientacion_ampliada = {
    "N": "Norte",
    "S": "Sur",
    "E": "Este",
    "O": "Oeste",
    "NE": "Noreste",
    "NO": "Noroeste",
    "SE": "Sudeste",
    "SO": "Sudoeste"
}


class InputData(BaseModel):
    ancho: Optional[float] = Field(default=None, gt=0)
    largo: Optional[float] = Field(default=None, gt=0)
    altura: Optional[float] = Field(default=None, gt=0)
    orientation: Optional[Orient] = None

    tv: float = Field(..., ge=0.0, le=1.0)
    ventana_ancho: Optional[float] = Field(default=None, ge=0.25, le=4.0)
    ventana_alto: Optional[float] = Field(default=None, ge=0.25, le=3.0)

    @field_validator("tv")
    @classmethod
    def validar_tv(cls, v):
        if v is None:
            raise ValueError("El campo 'tv' es obligatorio.")
        return v

    def area_vidrio(self) -> Optional[float]:
        if self.ventana_ancho and self.ventana_alto:
            return self.ventana_ancho * self.ventana_alto
        return None


def calcular_metricas_desde_yhat(yhat: float) -> dict[str, int]:
    y = max(0, min(100, yhat))
    return {
        "DA": int(y),
        "UDI": int(min(100, y + 8)),
        "sDA": int(max(0, y - 13)),
        "sUDI": int(min(100, y + 4)),
        "DAv_zone": int(y),
        "energia": int(max(0, 100 - y)),
    }


@app.get("/")
def root():
    return {"message": "Calculadora Luz Natural API", "status": "running", "version": "1.0.1"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/calcular_luz")
def calcular_luz(data: InputData):
    area_v = data.area_vidrio()
    if area_v is not None and area_v > 12.0:
        raise HTTPException(
            status_code=422, detail="Área de ventana no puede superar 12 m²")

    try:
        heatmap = get_heatmap_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cargando CSV: {e}")

    yhat_pred = None
    punto_usado = None

    if area_v is not None:
        try:
            yhat_pred, av_used, tv_used = predict_yhat_nearest(area_v, data.tv)
            punto_usado = {"area_vidrio": float(av_used), "tv": float(tv_used)}
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error en predicción: {e}")

    metrics = []
    energia_pct = None

    if yhat_pred is not None:
        metricas = calcular_metricas_desde_yhat(yhat_pred)
        for key in ["DA", "UDI", "sDA", "sUDI", "DAv_zone"]:
            valor = metricas[key]
            hex_color = None

            if key == "DA":
                hex_color = obtener_color_da(valor)
            elif key == "UDI":
                hex_color = obtener_color_udi(valor)
            elif key == "sDA":
                hex_color = obtener_color_sda(valor)
            elif key == "sUDI":
                hex_color = obtener_color_sudi(valor)
            elif key == "DAv_zone":
                # usa el mismo rango que DA
                hex_color = obtener_color_da(valor)

            try:
                sheet = get_model_sheet(key)
            except Exception:
                sheet = {"error": "Imagen no encontrada"}

            metrics.append({
                "key": key,
                "percent": valor,
                "color": hex_color,
                "sheet": sheet
            })

        energia_pct = metricas["energia"]

    msg = "OK" if yhat_pred is not None else \
        "Heatmap generado. Ingresá medidas de ventana para ver tu predicción."

    return {
        "ok": True,
        "mensaje": msg,
        "yhat_pred": yhat_pred,
        "punto_usado": punto_usado,
        "heatmap_data": heatmap,
        "metrics": metrics,
        "energia_pct": energia_pct,
        "orientation_label": orientacion_ampliada.get(data.orientation, data.orientation)
    }


@app.get("/model_sheet")
def model_sheet(metric: Literal["DA", "UDI", "sDA", "sUDI", "DAv_zone"] = Query(...)):
    try:
        return get_model_sheet(metric)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/debug")
def debug_info():
    current_dir = os.getcwd()
    files = os.listdir(current_dir)
    return {
        "current_directory": current_dir,
        "files": files,
        "csv_exists": os.path.exists("datos_sudi_limpio.csv"),
        "csv_path": os.path.abspath("datos_sudi_limpio.csv") if os.path.exists("datos_sudi_limpio.csv") else None
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

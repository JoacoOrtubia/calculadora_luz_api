from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Literal
import os

from graficos import get_heatmap_data, predict_yhat_nearest
from model_graph_area import get_model_sheet  # fichas de modelo

app = FastAPI(title="Calculadora Luz Natural", version="1.2.0")

# CORS
_allowed = os.getenv("ALLOWED_ORIGINS", "*")
allow_origins = [o.strip() for o in _allowed.split(",")
                 ] if _allowed != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Orientaciones válidas
Orient = Literal["N", "S", "E", "O", "NE", "NO", "SE", "SO"]


class InputData(BaseModel):
    # Datos del recinto (opcionales)
    ancho: Optional[float] = Field(default=None, gt=0)
    largo: Optional[float] = Field(default=None, gt=0)
    altura: Optional[float] = Field(default=None, gt=0)
    orientation: Optional[Orient] = None

    # Ventana
    tv: float = Field(..., ge=0.0, le=1.0,
                      description="Transmitancia visible 0–1")
    ventana_ancho: Optional[float] = Field(
        default=None, ge=0.25, le=4.0, description="Ancho ventana en m (0.25–4.0)")
    ventana_alto: Optional[float] = Field(
        default=None, ge=0.25, le=3.0, description="Alto ventana en m (0.25–3.0)")

    @field_validator("tv")
    @classmethod
    def _tv_ok(cls, v: float) -> float:
        if v is None:
            raise ValueError("tv es obligatorio (0–1).")
        return v

    def area_vidrio(self) -> Optional[float]:
        if self.ventana_ancho and self.ventana_alto:
            return self.ventana_ancho * self.ventana_alto
        return None


# ---- helper: mapeo de yhat a porcentajes (ajustable a tus tablas)
def _metric_percents_from_yhat(v: float) -> dict[str, int]:
    v = max(0, min(100, v))
    return {
        "DA": int(v),
        "UDI": int(min(100, v + 8)),
        "sDA": int(max(0, v - 13)),
        "sUDI": int(min(100, v + 4)),
        "DAv_zone": int(v),
        "energia": int(max(0, 100 - v)),
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/calcular_luz")
def calcular_luz(data: InputData):
    """
    Respuesta:
    {
      ok, mensaje, yhat_pred, punto_usado,
      heatmap_data: [[area_vidrio,tv,yhat], ...],
      metrics: [{ key, percent, sheet }, ...],
      energia_pct
    }
    """
    # Validación extra: área vidrio máximo
    area_v = data.area_vidrio()
    if area_v is not None and area_v > 12.0:
        raise HTTPException(
            status_code=422,
            detail="El área de la ventana no puede superar 12 m² (máx. 4×3 m)."
        )

    # 1) Heatmap
    try:
        heatmap = get_heatmap_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cargando CSV: {e}")

    # 2) Predicción puntual
    yhat_pred = None
    punto_usado = None
    if area_v is not None:
        try:
            y, av_used, tv_used = predict_yhat_nearest(area_v, data.tv)
            yhat_pred = float(y)
            punto_usado = {"area_vidrio": float(av_used), "tv": float(tv_used)}
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error en predicción: {e}")

    # 3) Métricas
    metrics: List[Dict] = []
    energia_pct: Optional[int] = None
    if yhat_pred is not None:
        mp = _metric_percents_from_yhat(yhat_pred)
        for k in ["DA", "UDI", "sDA", "sUDI", "DAv_zone"]:
            metrics.append(
                {"key": k, "percent": mp[k], "sheet": get_model_sheet(k)})
        energia_pct = mp["energia"]

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
    }


@app.get("/model_sheet")
def model_sheet(metric: Literal["DA", "UDI", "sDA", "sUDI", "DAv_zone"] = Query(...)):
    try:
        return get_model_sheet(metric)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

from typing import Any, Dict, List, Literal, Tuple

Metric = Literal["DA", "UDI", "sDA", "sUDI", "DAv_zone"]


def _build_sheet(
    name: str,
    categorias: Dict[str, Dict[str, Any]],
    areas_puntos: List[List[Tuple[float, float]]],
    metric_values: List[int],
) -> Dict[str, Any]:
    """
    Convierte tu definición de polígonos + categorías en un JSON consumible por el front.
    Es tolerante: si un valor no calza en ningún rango, usa un estilo por defecto.
    """
    polygons: List[Dict[str, Any]] = []

    for pts, val in zip(areas_puntos, metric_values):
        cat_label: str | None = None
        cat_props: Dict[str, Any] | None = None

        # match por rango
        for label, props in categorias.items():
            lo, hi = props["rango"]
            if lo <= val < hi:
                cat_label, cat_props = label, props
                break

        # fallback si no matchea ningún rango
        if cat_props is None:
            cat_label = "unclassified"
            cat_props = {"color": "#CCCCCC"}

        style = {
            "fill": cat_props.get("color", "#CCCCCC"),
            "line": "punteada" if cat_props.get("linea") == "punteada" else "solida",
        }
        polygons.append(
            {"points": pts, "value": val, "category": cat_label, "style": style}
        )

    legend = [
        {
            "label": k,
            "fill": v.get("color", "#CCCCCC"),
            "line": "punteada" if v.get("linea") == "punteada" else "solida",
        }
        for k, v in categorias.items()
    ]

    return {
        "metric": name,
        "x_label": "Window Area (m2)",
        "y_label": "Visible Transmittance",
        "xlim": [0, 12],
        "ylim": [0.1, 0.9],
        "polygons": polygons,
        "legend": legend,
    }


# ====== FICHAS ======

def _sheet_DA() -> Dict[str, Any]:
    categorias = {
        " < 50%": {"rango": (0, 50), "color": "#5E4FA2"},
        " [50%, 60%)": {"rango": (51, 60), "color": "#3288BD"},
        " [60%, 70%)": {"rango": (61, 70), "color": "#66C2A5"},
        " [70%, 80%)": {"rango": (71, 80), "color": "#ABE095"},
        " [80%, 90%)": {"rango": (81, 90), "color": "#E6F598"},
        " >= 90%": {"rango": (91, 100), "color": "#FEE08B"},
    }
    areas_puntos = [
        [(0.25, 0.1), (0.25, 0.9), (0.55, 0.9), (0.55, 0.45), (1.5, 0.45),
         (1.5, 0.35), (3.3, 0.35), (3.3, 0.15), (5.9, 0.15), (5.9, 0.1)],
        [(0.55, 0.45), (0.55, 0.9), (1.5, 0.9), (1.5, 0.45)],
        [(5.9, 0.15), (12, 0.15), (12, 0.1), (5.9, 0.1)],
        [(1.5, 0.35), (1.5, 0.9), (3.3, 0.9), (3.3, 0.35)],
        [(3.3, 0.15), (3.3, 0.35), (12, 0.35), (12, 0.15)],
        [(3.3, 0.15), (3.3, 0.35), (12, 0.35), (12, 0.15)],
        [(3.3, 0.35), (3.3, 0.9), (12, 0.9), (12, 0.35)],
    ]
    metric_values = [30, 55, 65, 75, 85, 85, 91]
    return _build_sheet("DA", categorias, areas_puntos, metric_values)


def _sheet_UDI() -> Dict[str, Any]:
    categorias = {
        " < 50%": {"rango": (0, 50), "color": "#5E4FA2"},
        " [50%, 60%)": {"rango": (51, 60), "color": "#3288BD"},
        " [60%, 70%)": {"rango": (61, 70), "color": "#66C2A5"},
        " [70%, 80%)": {"rango": (71, 80), "color": "#ABE095"},
        " [80%, 90%)": {"rango": (81, 90), "color": "#E6F598"},
        " >= 90%": {"rango": (91, 100), "color": "#FEE08B"},
    }
    areas_puntos = [
        [(0.25, 0.1), (0.25, 0.9), (1.1, 0.9), (1.1, 0.35), (2, 0.35),
         (2, 0.25), (3, 0.25), (3, 0.15), (5.9, 0.15), (5.9, 0.1)],
        [(6.1, 0.65), (6.1, 0.9), (12, 0.9), (12, 0.55), (8, 0.55), (8, 0.65)],
        [(1.1, 0.35), (1.1, 0.65), (2, 0.65), (2, 0.35)],
        [(5.9, 0.1), (5.9, 0.15), (12, 0.15), (12, 0.1)],
        [(2, 0.25), (2, 0.55), (12, 0.55), (12, 0.15), (3, 0.15), (3, 0.25)],
        [(1.1, 0.65), (1.1, 0.9), (6.1, 0.9), (6.1, 0.65)],
        [(2, 0.55), (2, 0.65), (8, 0.65), (8.0, 0.55)],
    ]
    metric_values = [25, 25, 55, 55, 65, 65, 75]
    return _build_sheet("UDI", categorias, areas_puntos, metric_values)


def _sheet_sDA() -> Dict[str, Any]:
    categorias = {
        " < 55%": {"rango": (0, 55), "color": "#5E4FA2"},
        " [55%, 75%)": {"rango": (55, 75), "color": "#66C2A5"},
        " >= 75%": {"rango": (76, 100), "color": "#E6F598"},
    }
    areas_puntos = [
        [(0.25, 0.1), (0.25, 0.9), (0.95, 0.9), (0.95, 0.55), (1.5, 0.55),
         (1.5, 0.35), (3, 0.35), (3, 0.15), (8, 0.15), (8, 0.1)],
        [(0.25, 0.9), (0.95, 0.9), (0.95, 0.55), (1.5, 0.55), (1.5, 0.35),
         (3, 0.35), (3, 0.15), (8, 0.15), (8, 0.1), (12, 0.1), (12, 0.9)],
    ]
    metric_values = [25, 80]
    return _build_sheet("sDA", categorias, areas_puntos, metric_values)


def _sheet_sUDI() -> Dict[str, Any]:
    categorias = {
        " < 75%": {"rango": (0, 75), "color": "#5E4FA2"},
        " [75%, 95%)": {"rango": (76, 95), "color": "#66C2A5"},
        " >= 95%": {"rango": (96, 98), "color": "#E6F598"},
        " Hybrid zone": {"rango": (99, 100), "color": "#d3d3d3"},
    }
    areas_puntos = [
        [(4.7, 0.75), (4.7, 0.9), (12, 0.9), (12, 0.45), (6.1, 0.45), (6.1, 0.75)],
        [(0.25, 0.1), (0.25, 0.9), (1.1, 0.9), (1.1, 0.45), (2.5, 0.45),
         (2.5, 0.25), (6.1, 0.25), (6.1, 0.15), (9.1, 0.15), (9.1, 0.1)],
        [(1.1, 0.45), (1.1, 0.9), (4.7, 0.9),
         (4.7, 0.75), (6.1, 0.75), (6.1, 0.45)],
        [(9.1, 0.1), (9.1, 0.15), (12, 0.15), (12, 0.1)],
        [(6.1, 0.35), (6.1, 0.45), (8.6, 0.45), (8.6, 0.35)],
        [(6.1, 0.15), (6.1, 0.25), (12, 0.25), (12, 0.15)],
        [(2.5, 0.25), (2.5, 0.45), (6.1, 0.45), (6.1, 0.25)],
        [(6.1, 0.25), (6.1, 0.35), (12, 0.35), (12, 0.25)],
        [(8.6, 0.35), (8.6, 0.45), (12, 0.45), (12, 0.35)],
    ]
    metric_values = [37, 37, 85, 85, 85, 97, 99, 99, 99]
    return _build_sheet("sUDI", categorias, areas_puntos, metric_values)


def _sheet_DAv_zone() -> Dict[str, Any]:
    categorias = {
        " Availability 1": {"rango": (0, 50), "color": "#a1c781"},
        " Availability 2": {"rango": (60, 62), "color": "#81C784", "linea": "punteada"},
        " Conditional availability": {"rango": (70, 72), "color": "#d3d3d3", "linea": "punteada"},
    }
    areas_puntos = [
        [(1.1, 0.45), (1.1, 0.9), (6.1, 0.9), (6.1, 0.65), (8, 0.65), (8, 0.55), (12, 0.55),
         (12, 0.1), (5.9, 0.1), (5.9, 0.15), (3.3, 0.15), (3.3, 0.35), (1.5, 0.35), (1.5, 0.45)],
        [(1.1, 0.55), (1.1, 0.9), (4.7, 0.9), (4.7, 0.75), (6.1, 0.75), (6.1, 0.45), (12, 0.45), (12, 0.1), (8.6, 0.1),
         (8.6, 0.15), (6.1, 0.15), (6.1, 0.25), (3.3, 0.25), (3.3, 0.35), (2.5, 0.35), (2.5, 0.45), (1.5, 0.45), (1.5, 0.55)],
        [(8.6, 0.35), (8.6, 0.45), (12, 0.45), (12, 0.35)],
    ]
    metric_values = [49, 61, 71]
    return _build_sheet("DAv_zone", categorias, areas_puntos, metric_values)


def get_model_sheet(metric: Metric) -> Dict[str, Any]:
    if metric == "DA":
        return _sheet_DA()
    if metric == "UDI":
        return _sheet_UDI()
    if metric == "sDA":
        return _sheet_sDA()
    if metric == "sUDI":
        return _sheet_sUDI()
    if metric == "DAv_zone":
        return _sheet_DAv_zone()
    raise ValueError("Métrica no soportada")

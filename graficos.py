import csv


def obtener_datos_grafico_sudi():
    datos = {
        "x": [],  # area_vidrio
        "y": [],  # tv
        "z": []   # yhat
    }

    with open("datos_sudi.txt", newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            datos["x"].append(float(fila["area_vidrio"]))
            datos["y"].append(float(fila["tv"]))
            datos["z"].append(float(fila["yhat"]))

    return datos

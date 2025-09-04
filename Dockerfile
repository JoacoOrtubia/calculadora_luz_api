# Usa una imagen base de Python estable
FROM python:3.11-slim

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia y instala las dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de tu proyecto
COPY . .

# Expone el puerto en el que corre tu aplicación
EXPOSE 10000

# Comando para iniciar la API con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]

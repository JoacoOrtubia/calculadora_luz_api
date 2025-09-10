# Usa una imagen base de Python estable
FROM python:3.11-slim

# Configurar variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema si son necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia y instala las dependencias de Python
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos del proyecto
COPY . .

# Crear directorio para logs si es necesario
RUN mkdir -p /app/logs

# Expone el puerto en el que corre la aplicación
EXPOSE 10000

# Comando para iniciar la API con Uvicorn usando python -m
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
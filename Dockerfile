# Imagen base oficial de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements primero para cachear instalaciones si no hay cambios
COPY requirements.txt .

# Instalar dependencias del sistema necesarias para pandas y compilación
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    git \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar el resto de la aplicación al contenedor
COPY . .

# Exponer el puerto que usará Uvicorn (Render usa el env $PORT automáticamente)
EXPOSE 8000

# Comando de inicio para producción en Render
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

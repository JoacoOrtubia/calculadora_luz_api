# Imagen base con Python 3.11 (compatible con pandas)
FROM python:3.11-slim

# Setea el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala dependencias del sistema necesarias para pandas/numpy
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala las dependencias del proyecto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto que usará Uvicorn
EXPOSE 8000

# Comando de arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

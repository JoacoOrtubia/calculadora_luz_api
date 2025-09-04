# Usa una imagen compatible con pandas
FROM python:3.11-slim

# Define el directorio de trabajo
WORKDIR /app

# Instala las dependencias
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto de los archivos
COPY . .

# Expone el puerto si lo necesitás (opcional)
EXPOSE 10000

# Comando por defecto para iniciar la API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]

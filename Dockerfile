# Usar imagen base de Python oficial
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para PyTorch y transformers
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio para modelos de transformers (cache)
RUN mkdir -p /root/.cache/huggingface

# Exponer el puerto que usa la aplicación
EXPOSE 5003

# Variables de entorno para optimizar PyTorch
ENV PYTHONUNBUFFERED=1
ENV TOKENIZERS_PARALLELISM=false

# Comando para ejecutar la aplicación
CMD ["python", "entrauma_bot.py"]

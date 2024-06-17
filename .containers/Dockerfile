# Usar la imagen oficial de Python 3.9 slim
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /api

# Copiar el archivo de requerimientos al contenedor
COPY Floppotron-API/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación en el contenedor
COPY Floppotron-API/ .

# Ejecutar la aplicación
CMD ["python", "main.py"]
# Usa la imagen oficial de Python 3.11
FROM python:3.12-bullseye

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el contenido actual del directorio al contenedor en /app
COPY . /app

# Instala las dependencias, si es necesario
RUN pip install --no-cache-dir -r requirements.txt

# Especifica el comando a ejecutar al iniciar el contenedor
CMD ["python", "./src/main.py"]

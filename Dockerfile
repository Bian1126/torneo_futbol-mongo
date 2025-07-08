# Imagen base con Python 3.13 y Alpine Linux
FROM python:3.13-alpine AS base

LABEL maintainer="Tu Nombre <tuemail@example.com>"

# Establece directorio de trabajo
WORKDIR /code

# Instala herramientas y librerías necesarias
RUN apk --no-cache add \
    bash gcc musl-dev libffi-dev \
    python3-dev build-base \
    jpeg-dev zlib-dev \
    postgresql-dev \
    pango ttf-freefont \
    curl

# Copia e instala dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Configuracion de zona horaria
RUN ln -sf /usr/share/zoneinfo/America/Argentina/Cordoba /etc/localtime

# Expone el puerto del servidor Django
EXPOSE 8000

# Comando por defecto para producción
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "app.wsgi"]

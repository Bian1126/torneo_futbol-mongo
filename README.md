
# Tutorial: Despliegue de "Torneo Fútbol" en Django con Docker + MongoDB v2

Práctico de Mapeo Objeto-Relacional para la materia Bases de Datos, Ingeniería en Sistemas, UTN FRVM.

**Stack:**  
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Docker Desktop](https://img.shields.io/badge/Docker%20Desktop-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/products/docker-desktop)
[![Django 5.1.11](https://img.shields.io/badge/Django%205.1.11-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Alpine Linux](https://img.shields.io/badge/Alpine%20Linux-0D597F?style=for-the-badge&logo=alpinelinux&logoColor=white)](https://alpinelinux.org/)
[![Python 3.13](https://img.shields.io/badge/Python%203.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL 15](https://img.shields.io/badge/PostgreSQL%2015-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![MongoDB 7](https://img.shields.io/badge/MongoDB%207-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![MongoEngine 0.29](https://img.shields.io/badge/MongoEngine%200.29-4FAA41?style=for-the-badge&logo=python&logoColor=white)](https://mongoengine.org/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)](https://gunicorn.org/)
[![MongoDB Compass](https://img.shields.io/badge/MongoDB%20Compass-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/products/compass)

## **Mantenido por Grupo 03**  
### **Integrantes:**
- Bergas, Victoria
- Corti, Elba
- Giovanardi Blanco, Felipe
- Lattanzi, Simona
- Peliza, Matías
- Petrucci, Bianca
- Porporatto, Lázaro
- Rubio Falcon, Carolina Inés

## **Descargo de Responsabilidad:**  
El código proporcionado se ofrece "tal cual", sin garantía de ningún tipo, expresa o implícita. En ningún caso los autores o titulares de derechos de autor serán responsables de cualquier reclamo, daño u otra responsabilidad.

## Introducción
Este proyecto tiene como finalidad aplicar los contenidos vistos en la Cátedra de Bases de Datos mediante el desarrollo de un sistema de gestión de torneos de fútbol. Integra PostgreSQL y MongoDB para practicar conceptos de modelado y persistencia de datos en modelos relacionales y no relacionales.

---

## Requisitos Previos
- Docker y Docker Compose instalados en tu sistema. Puedes consultar la [documentación oficial de Docker](https://docs.docker.com/get-started/get-docker/) para la instalación.
- Recomendado: Docker Desktop instalado y en ejecución (recomendado para manejar visualmente los contenedores y facilitar la administración). [Descargar Docker Desktop](https://www.docker.com/products/docker-desktop/) 
- Recomendado: MongoDB Compass instalado para poder visualizar y administrar fácilmente la base de datos MongoDB. [Descargar MongoDB Compass](https://www.mongodb.com/products/compass)
- Conocimientos básicos de Python, Django y MongoDB (no excluyente, el tutorial es autoexplicativo).

## Recursos Útiles
- [Tutorial oficial de Django](https://docs.djangoproject.com/en/5.0/intro/tutorial01/)
- [Cómo crear un entorno virtual en Python](https://docs.python.org/3/tutorial/venv.html)
- [Iniciar en MongoDB](https://www.mongodb.com/docs/manual/tutorial/getting-started/)
- [Documentación oficial de Docker](https://docs.docker.com/get-started/)
- [Guía rápida de Docker Compose](https://docs.docker.com/compose/gettingstarted/)
- [MongoDB Compass — Herramienta GUI oficial](https://www.mongodb.com/products/compass)
- [Introducción a MongoEngine (ODM para MongoDB en Python)](https://docs.mongoengine.org/)

---

## **Instrucciones para levantar el proyecto**

### 1. Clonar el repositorio
> *Puedes copiar todo este bloque y pegarlo directamente en tu terminal.*

```bash
git clone https://github.com/Bian1126/torneo_futbol-mongo.git
cd TORNEO-FUTBOL-mongoDB
```

### 2. Configuración de Variables de Entorno
En el archivo `.env.db` utilizado para almacenar las variables de entorno necesarias para la conexión a las bases de datos, configurarlo de la siguiente manera:

> *Puedes copiar todo este bloque y pegarlo directamente en tu archivo `.env.db`. (no es necesario si se clona el repositorio)*

```conf
# PostgreSQL
DATABASE_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_INITDB_ARGS=--auth-host=md5 --auth-local=trust
LANG=es_AR.utf8

# MongoDB
MONGO_DB=torneo
MONGO_URI=mongodb://root:example@mongo:27017/torneo?authSource=admin
MONGO_URI_LOCAL=mongodb://root:example@localhost:27019/torneo?authSource=admin
MONGO_USER=root
MONGO_PASS=example
MONGO_HOST=mongo
MONGO_PORT=27017

# Django
SECRET_KEY=clave-insegura-para-dev-torneo
DEBUG=True
ALLOWED_HOSTS=*
```

### 3. Levantar el proyecto
> *Desde la terminal, levantar el proyecto con los siguientes comandos:*

```bash
docker-compose up --build  # Si aún no se levantó el proyecto, aún así se puede implementar si ya se levantó también.
#Nota, con este comando aparecerán los logs en el terminal en tiempo real, sirve paara chequear errores, si no se quiere, hacer el siguiente:

docker-compose up --build -d #De esta forma se carga todo en segundo plano y se habilita la misma terminal.

docker-compose run --rm manage makemigrations  # Genera archivos de migraciones a partir de los modelos

docker-compose run --rm manage migrate  # Realiza migraciones en Postgres

docker-compose run --rm manage createsuperuser  # (Si aún no se creó)
```

### 4. Carga de datos inicial: 
> *Puedes hacer la carga de datos a las bases de batos con los siguientes comandos:*

```bash

docker-compose exec backend bash #Para ejecutar comandos dentro del entorno del contenedor llamado backend.
# Esto te mete “adentro” del contenedor que está corriendo Django, como si estuvieras usando una terminal en esa máquina virtual aislada.

python load_and_sync.py #Ejecuta el script de carga y sincronizacion de datos que está en la raíz del proyecto dentro del contenedor backend.
```

### 5. Detener el proyecto:
> *Puedes hacerlo si ya terminaste con tu trabajo*
 
```bash
# Opción 1: Si usaste el comando docker-compose up --build tenes que volver a esa terminal.
ctrl + c
# Opción 2: Si usaste el comando docker-compose up --build -d
docker-compose stop

# Opción 3: Si usaste el comando docker-compose up --build -d
docker-compose down

#Diferencias: Opción 1 y 2 dejan los contenedores en docker desktop visibles pero detenidos, Opción 3 los borra aunque
#cuando se vuelven a crear se mantiene la persistencia de datos (ya que no estamos borrando los volúmenes)
```

---
### 6. Acceso a la aplicación

- **Admin Django:** [http://localhost:8000/admin/](http://localhost:8000/admin/)
> *Una vez adentro poner el usuario y contraseña del superusuario creado al levantar el proyecto.*

---

### 7. Opciones de conexión

- **Desde el backend Django (dentro de Docker):**
  - Host: `mongo`
  - Puerto: `27017`
  - URI interna:
    ```
    mongodb://root:example@mongo:27017/torneo?authSource=admin
    ```
- **Desde tu máquina local (por ejemplo, usando MongoDB Compass):**
  - Host: `localhost`
  - Puerto: `27019`
  - URI externa:
    ```
    mongodb://root:example@localhost:27019/torneo?authSource=admin
    ```


### 8. Verifica los datos

> *Puedes usar MongoDB Compass y conectarte con la URI externa para ver las colecciones y documentos cargados.*
*También puedes chequearlo en la base de datos de postgres desde en algun terminal. Se recomienda el terminal del Docker Desktop.*

---

## Servicios Definidos en Docker Compose

### 1. **postgres**
> Contenedor de PostgreSQL.

- Imagen: `postgres:15-alpine`
- Volumen persistente: `postgres-data`
- Variables de entorno: definidas en `.env.db`
- Puerto interno: 5432, expuesto en 5433 en tu máquina

### 2. **mongo**
> Contenedor de MongoDB.

- Imagen: `mongo:7`
- Volumen persistente: `mongo-data:/data/db`
- Variables de entorno para inicializacion (MONGO_INITDB_*): definidas directamente en `docker-compose.yml`
- Variables de entorno adicionales (MONGO_URI, MONGO_USER, etc.): definidas en `.env.db`
- Puerto interno: 27017, expuesto en 27019 en tu máquina


### 3. **backend**
> Servidor de desarrollo Django.

- Comando: `python3 manage.py runserver 0.0.0.0:8000`
- Puerto expuesto: 8000
- Código montado desde `./src`
- Depende de: `postgres` y `mongo`

### 4. **manage**
> Ejecuta comandos `manage.py` desde Docker.

- Entrypoint: `python manage.py`
- Ideal para migraciones, creación de superusuario, carga de datos, etc.
- Depende de: `postgres` y `mongo`

---

## Estructura del Proyecto

```
TORNEO-FUTBOL-mongoDB/
├── src/                        # Código fuente de la aplicación
│   ├── app/                    # Proyecto Django (configuración global)
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py         # Configuración global del proyecto
│   │   ├── urls.py             # Rutas principales del proyecto
│   │   └── wsgi.py
│   │
│   ├── torneo/                 # Aplicación principal (lógica de negocio)
│   │   ├── __init__.py
│   │   ├── admin.py            # Registro de modelos en el panel de administración
│   │   ├── apps.py             # Configuración de la app y registro de señales
│   │   ├── fixtures/           # Datos de ejemplo para loaddata
│   │   │   └── initial_data.json
│   │   ├── migrations/         # Migraciones de base de datos relacional
│   │   │   └── __init__.py
│   │   ├── models.py           # Modelos SQL (Postgres)
│   │   ├── models_mongo.py     # Modelos NoSQL (MongoDB)
│   │   ├── signals.py          # Señales conectadas a eventos del ORM
│   │   ├── tests.py
│   │   ├── views.py
│   │   └── ...
│   │
│   ├── manage.py               # CLI de Django
│   └── initial_loader.py       # Script para poblar MongoDB desde Postgres
│
├── .env.db                     # Variables de entorno para Postgres, MongoDB y Django
├── docker-compose.yml          # Definición de servicios Docker
├── Dockerfile                  # Imagen personalizada del backend
├── init.ps1                    # Script de inicio rápido (PowerShell)
├── README.md                   # Documentación del proyecto
└── requirements.txt            # Dependencias Python para el entorno
```

---

## Créditos

Trabajo realizado para la materia Bases de Datos, UTN FRVM, Grupo 03.

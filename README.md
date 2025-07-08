
# Tutorial: Despliegue de "Torneo Futbol" en Django con Docker + MongoDB v2

Práctico de Mapeo Objeto-Relacional para la materia Bases de Datos, Ingeniería en Sistemas, UTN FRVM.

**Stack:**  
Docker · Django 5.x · Alpine Linux · Python 3.13 · PostgreSQL 15 · Mongo 7 · Mongoengine 0.29 · Gunicorn · MongoDB Compass

---

## Referencia Rápida

**Mantenido por Grupo 03**  
**Integrantes:**
- Bergas, Victoria
- Corti, Elba
- Giovanardi Blanco, Felipe
- Lattanzi, Simona
- Peliza, Matías
- Petrucci, Bianca
- Porporatto, Lázaro
- Rubio Falcon, Carolina Inés

**Descargo de Responsabilidad:**  
El código proporcionado se ofrece "tal cual", sin garantía de ningún tipo, expresa o implícita. En ningún caso los autores o titulares de derechos de autor serán responsables de cualquier reclamo, daño u otra responsabilidad.

---

## Introducción

Este proyecto implementa la gestión de un torneo de fútbol, integrando PostgreSQL y MongoDB para practicar conceptos de modelado y persistencia de datos relacional y no relacional.

---

## Requisitos Previos

- Docker y Docker Compose instalados en tu sistema. Puedes consultar la [documentación oficial de Docker](https://docs.docker.com/get-started/get-docker/) para la instalación.
- Conocimientos básicos de Python, Django y MongoDB (no excluyente, el tutorial es autoexplicativo).

---

## Recursos Útiles

- [Tutorial oficial de Django](https://docs.djangoproject.com/en/5.0/intro/tutorial01/)
- [Cómo crear un entorno virtual en Python](https://docs.python.org/3/tutorial/venv.html)
- [Iniciar en MongoDB](https://www.mongodb.com/docs/manual/tutorial/getting-started/)

---

## Instrucciones para levantar el proyecto

### 1. Clonar el repositorio
> Puedes copiar todo este bloque y pegarlo directamente en tu terminal.

```bash
git clone https://github.com/Bian1126/torneo_futbol-mongo.git
cd TORNEO-FUTBOL-mongoDB
```

### 2. Configuración de Variables de Entorno
En el archivo `.env.db` utilizado para almacenar las variables de entorno necesarias para la conexión a las bases de datos, configurarlo de la siguiente manera:

>Puedes copiar todo este bloque y pegarlo directamente en tu archivo `.env.db`.

```env
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

# Django
SECRET_KEY=clave-insegura-para-dev-torneo
DEBUG=True
ALLOWED_HOSTS=*
```

### 3. Levantar el proyecto
Desde la terminal, levantar el proyecto con los siguientes comandos:

```bash
docker-compose up --build  # Si aún no se levantó el proyecto

docker-compose run --rm manage makemigrations  # Genera archivos de migraciones a partir de los modelos

docker-compose run --rm manage migrate  # Realiza migraciones en Postgres

docker-compose run --rm manage createsuperuser  # (Si aún no se creó)
```

---

## Carga de datos en MongoDB

### Opciones de conexión

- **Desde el backend (dentro de Docker):**
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

### Carga automática de datos

Para cargar los datos de ejemplo en MongoDB, sigue estos pasos:

1. **Levanta los servicios (si no están corriendo):**
   ```bash
   docker-compose up -d
   ```

2. **Ejecuta el script de carga desde el contenedor:**
   ```bash
   docker exec -it django-backend python initial_loader.py
   ```

Verás mensajes de "Insertado: ..." por cada registro cargado.

### Verifica los datos

Puedes usar MongoDB Compass y conectarte con la URI externa para ver las colecciones y documentos cargados.

---

## Acceso a la aplicación

- **Admin Django:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## Servicios Definidos en Docker Compose

### 1. **db**
> Contenedor de PostgreSQL.

- Imagen: `postgres:alpine`
- Volumen persistente: `postgres-db`
- Variables de entorno: definidas en `.env.db`
- Healthcheck incluido

### 2. **mongo**
> Contenedor de MongoDB.

- Imagen: `mongo:7`
- Volumen persistente: `mongo-data:/data/db`
- Variables de entorno: definidas en `.env.db`

### 3. **backend**
> Servidor de desarrollo Django.

- Comando: `python3 manage.py runserver 0.0.0.0:8000`
- Puerto expuesto: 8000
- Código montado desde `./src`
- Depende de: `db` y `mongo`

### 4. **generate**
> Servicio opcional para crear el proyecto Django si no existe.

- Ejecuta: `django-admin startproject app src`
- Útil al iniciar el proyecto por primera vez
- Usa permisos de root para crear carpetas

### 5. **manage**
> Ejecuta comandos `manage.py` desde Docker.

- Entrypoint: `python3 manage.py`
- Ideal para migraciones, creación de superusuario, carga de datos, etc.
- Depende de: `db` y `mongo`

---

## Estructura del Proyecto

```
TORNEO-FUTBOL-mongoDB/
├── src/                        # Código fuente de la aplicación
│   ├── app/                    # Proyecto Django
│   │   ├── settings.py         # Configuración global del proyecto
│   │   ├── urls.py             # Rutas principales del proyecto
│   │   └── ...
│   ├── torneo/                 # Aplicación principal (lógica de negocio)
│   │   ├── fixtures/           # Datos de ejemplo (carga inicial con loaddata)
│   │   │   └── initial_data.json
│   │   ├── migrations/         # Migraciones de base de datos
│   │   ├── admin.py            # Registro de modelos en el panel de administración
│   │   ├── apps.py             # Configuración de la app
│   │   ├── models.py           # Modelos SQL
│   │   ├── models_mongo.py     # Modelos NoSQL (MongoDB)
│   │   ├── tests.py
│   │   ├── views.py
│   │   └── ...
│   ├── manage.py               # CLI de Django
│   └── initial_loader.py       # Script de carga Mongo desde Postgres
├── .env.db                     # Variables de entorno
├── docker-compose.yml          # Definición de servicios
├── Dockerfile                  # Imagen personalizada del backend
├── init.sh                     # Script de inicio rápido (bash)
├── init.ps1                    # Script de inicio rápido (PowerShell)
└── README.md                   # Documentación del proyecto
```

---

## Créditos

Trabajo realizado para la materia Bases de Datos, UTN FRVM.

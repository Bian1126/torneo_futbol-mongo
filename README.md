# Tutorial: Despliegue de "Torneo Futbol" en Django con Dcoker + MongoDB v2

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

- Docker y Docker Compose instalados en tu sistema. Puedes consultar la **documentación oficial de Docker** (https://docs.docker.com/get-started/get-docker/) para la instalación.
- Conocimientos básicos de Python, Django y mongodb (no excluyente, el tutorial es autoexplicativo).

---

## Recursos Útiles

- [Tutorial oficial de Django](https://docs.djangoproject.com/en/2.0/intro/tutorial01/)
- [Cómo crear un entorno virtual en Python](https://docs.djangoproject.com/en/2.0/intro/contributing/)
- [Iniciar en mongodb](https://www.mongodb.com/docs/manual/tutorial/getting-started/)

---

## Instrucciones para levantar el proyecto

### 1. Clonar el repositorio
> Puedes copiar todo este bloque y pegarlo directamente en tu terminal.

```bash
git clone https://github.com/Bian1126/torneo_futbol-mongo.git
cd TORNEO-FUTBOL-mongoDB
```

### 2. Configuración de Variables de Entorno
En el archivo .env.db utilizado para almacenar las variables de entorno necesarias para la conexión a la base de datos configurarlo de la siguiente manera:

>Puedes copiar todo este bloque y pegarlo directamente en tu archivo .env.db.

```
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
Desde la terminal levantar el proyecto con los siguiente comando
```
-docker-compose up --build (si aun no se levanto el proyecto)

-docker-compose run --rm manage makemigrations (genera archivos de migraciones a partir de los modelos)

-docker-compose run --rm manage migrate (realiza migraciones en postgres)

-docker-compose run --rm manage createsuperuser(si aún no se creo)
```
Para hacer la carga de datos a las base de batos con los siguiente comando

```
-docker-compose run --rm manage loaddata initial_data (archivo json para inicializar los datos con djjango en postgres)

-python manage.py shell (abrir la terminal para cargar los datos a mongodb)

-exec(open("initial_loader.py", encoding="utf-8").read()) (realiza la carga de los datos a mongodb con el archivo initial_loader)
```

---

## Acceso a la aplicación

- **Admin Django:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## Servicios Definidos en Docker Compose

### 1. **db**
> Contenedor de PostgreSQL.

- Imagen: postgres:alpine
- Volumen persistente: postgres-db
- Variables de entorno: definidas en .env.db
- Healthcheck incluido (espera a que el servicio esté listo)

### 2. **mongo**
> Contenedor de Mongo.

- Imagen: mongo:7
- Volumen persistente: mongo-data:/data/db
- Variables de entorno: definidas en .env.db

### 3. **backend**
> Servidor de desarrollo Django.

- Comando: python3 manage.py runserver 0.0.0.0:8000
- Puerto expuesto: 8000
- Código montado desde ./src
- Depende de: db (espera a que esté saludable) mongo

### 4. **generate**
>Servicio opcional para crear el proyecto Django si no existe.

- Ejecuta: django-admin startproject app src
- Útil al iniciar el proyecto por primera vez
- Usa permisos de root para crear carpetas

### 4. **manage**
>Ejecuta comandos manage.py desde Docker.

- Entrypoint: python3 manage.py
- Ideal para migraciones, superusuario, etc.
- Depende de: db (espera a que esté saludable)
- Depende de: mongo


## Estructura del Proyecto

```
TORNEO-FUTBOL-mongoDB/
├── src/                        # Código fuente de la aplicación
│   ├── app/                    # Proyecto Django
│   │   ├── settings.py         # Configuración global del proyecto (bases, apps, etc)
│   │   ├── urls.py             # Rutas principales del proyecto
│   │   └── ...                 # Otros archivos de configuración
│   ├── torneo/                 # Aplicación principal (lógica de negocio)
│   │   ├── fixtures/           # Datos de ejemplo (carga inicial con loaddata)
│   │   │   └── initial_data.json
│   │   ├── migrations/         # Migraciones de base de datos
│   │   ├── admin.py            # Registro de modelos en el panel de administración
│   │   ├── apps.py             # Configuración de la app
│   │   ├── models.py           # Definición de modelos SQL (estructura de la BD relacional)
│   │   ├── models_mongo.py     # Definición de modelos NoSQL (estructura de la BD en MongoDB)
│   │   ├── tests.py            # Pruebas automáticas
│   │   ├── views.py            # Vistas (lógica del backend)
│   │   └── ...
│   └── manage.py               # Herramienta CLI de Django
│   └── initial_loader.py  #Archivo de carga para pasar los datos de postgres a mongodb
├── .env.db                     # Variables de entorno de la base de datos
├── docker-compose.yml          # Definición de servicios Docker
├── Dockerfile                  # Imagen personalizada del backend
├── init.sh                     # Script de inicio rápido (bash)
├── init.ps1                    # Script de inicio rápido (PowerShell)
└── README.md                   # Documentación del proyecto
```

---

## Créditos

Trabajo realizado para la materia Bases de Datos, UTN FRVM.

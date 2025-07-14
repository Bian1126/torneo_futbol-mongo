# init.ps1 - Inicialización del proyecto (PowerShell para Windows)
# -------------------------------------------
# Este script se debe ejecutar la primera vez que se levanta el proyecto.
# Ejecutar desde PowerShell con: .\init.ps1
# -------------------------------------------

# Detener y eliminar contenedores, volúmenes e imágenes huérfanas
docker-compose down -v --remove-orphans --rmi all

# Construir imágenes y levantar contenedores postgres, mongo y backend en segundo plano
docker-compose up --build -d postgres mongo backend

# Esperar 10 segundos para asegurar que los servicios estén disponibles
Start-Sleep -Seconds 10

# Generar migraciones a partir de los modelos Django
docker-compose run --rm manage makemigrations

# Aplicar las migraciones a la base de datos PostgreSQL
docker-compose run --rm manage migrate

# Crear superusuario admin sin interacción (usuario: admin, email: admin@example.com)
docker-compose run --rm manage createsuperuser --noinput --username admin --email admin@example.com

# Establecer contraseña 'admin' para el superusuario creado
docker-compose run --rm manage shell -c `
"from django.contrib.auth import get_user_model; User = get_user_model(); u, created = User.objects.get_or_create(username='admin', 
defaults={'email': 'admin@example.com'}); u.set_password('admin'); u.save()"


# Cargar datos iniciales desde fixture JSON
docker-compose run --rm manage loaddata initial_data

# Ejecutar script para cargar y sincronizar datos con MongoDB
docker-compose exec backend python load_and_sync.py

# Mensaje final para informar que el proceso terminó
echo "El proyecto se levanto correctamente. Podes acceder al admin en http://localhost:8000/admin con usuario 'admin' y contraseña 'admin'."



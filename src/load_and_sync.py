# src/load_and_sync.py

import os
import django
from django.core.management import call_command

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

# Importar modelos
from torneo.models import Ciudad, TipoDocumento, Categoria, Equipo, Jugador, Cancha, Torneo, Inscripcion, Partido

print("📥 Cargando datos en PostgreSQL desde el fixture...")
call_command('loaddata', 'torneo/fixtures/initial_data.json')

print("🔄 Sincronizando datos en MongoDB vía signals...")
modelos = [
    Ciudad,
    TipoDocumento,
    Categoria,
    Equipo,
    Jugador,
    Cancha,
    Torneo,
    Inscripcion,
    Partido
]

for modelo in modelos:
    nombre_modelo = modelo.__name__
    objetos = modelo.objects.all()
    print(f"  • {nombre_modelo}: {objetos.count()} objetos")
    for obj in objetos:
        obj.save()  # Esto dispara los signals definidos en signals.py

print("✅ Sincronización completada.")

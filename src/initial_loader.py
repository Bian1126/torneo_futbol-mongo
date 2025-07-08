
import json
from pathlib import Path
from mongoengine import connect

connect(
    db="torneo",
    username="root",
    password="example",
    host="mongo",
    port=27017,
    authentication_source="admin"
)

from torneo.models_mongo import *

json_path = Path("torneo/fixtures/initial_data.json").resolve()

with open(json_path, encoding='utf-8') as f:
    data = json.load(f)

model_map = {
    "torneo.tipodocumento": TipoDocumento,
    "torneo.categoria": Categoria,
    "torneo.equipo": Equipo,
    "torneo.jugador": Jugador,
    "torneo.cancha": Cancha,
    "torneo.torneo": Torneo,
    "torneo.inscripcion": Inscripcion,
    "torneo.partido": Partido
}

for entry in data:
    model_label = entry["model"]
    pk = entry["pk"]
    fields = entry["fields"]
    fields["postgres_id"] = pk
    
    model_class = model_map.get(model_label)
    if not model_class:
        print(f"Modelo no encontrado: {model_label}")
        continue

    try:
        obj = model_class(**fields)
        obj.save()
        print(f"Insertado: {model_label} (postgres_id={pk})")
    except Exception as e:
        print(f"Error insertando {model_label} (postgres_id={pk}): {e}")
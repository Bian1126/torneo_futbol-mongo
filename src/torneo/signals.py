from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Equipo, Torneo, Jugador, Partido, Inscripcion
from .models_mongo import (
    Equipo as EquipoDoc,
    Torneo as TorneoDoc,
    Jugador as JugadorDoc,
    Partido as PartidoDoc,
    Inscripcion as InscripcionDoc,
    Categoria as CategoriaDoc,
    Cancha as CanchaDoc,
)

from mongoengine import connect, disconnect
import os

# ================================
# Conexión MongoDB
# ================================
mongo_host = os.getenv("MONGO_HOST", "localhost")
mongo_port = os.getenv("MONGO_PORT", "27017")

disconnect(alias="default")

connect(
    db='torneo',
    host=f'mongodb://root:example@{mongo_host}:{mongo_port}/torneo?authSource=admin',
    alias="default"
)

# ================================
# EQUIPO
# ================================
@receiver(post_save, sender=Equipo)
def sync_equipo_to_mongo(sender, instance, **kwargs):
    try:
        EquipoDoc.objects(postgres_id=instance.id).update_one(
            set__nombre=instance.nombre,
            set__ciudad=instance.ciudad,
            set__fechaDeFundacion=instance.fechaDeFundacion,
            upsert=True
        )
    except Exception as e:
        print(f"[ERROR EN SYNC_EQUIPO_TO_MONGO] {e}")

@receiver(post_delete, sender=Equipo)
def delete_equipo_from_mongo(sender, instance, **kwargs):
    try:
        EquipoDoc.objects(postgres_id=instance.id).delete()
    except Exception as e:
        print(f"[ERROR EN DELETE_EQUIPO_FROM_MONGO] {e}")

# ================================
# TORNEO
# ================================
@receiver(post_save, sender=Torneo)
def sync_torneo_to_mongo(sender, instance, **kwargs):
    try:
        categoria_doc = CategoriaDoc.objects(postgres_id=instance.categoria.id).first() if instance.categoria else None

        TorneoDoc.objects(postgres_id=instance.id).update_one(
            set__nombre=instance.nombre,
            set__fechaInicio=instance.fechaInicio,
            set__fechaFin=instance.fechaFin,
            set__categoria=categoria_doc,
            upsert=True
        )
    except Exception as e:
        print(f"[ERROR EN SYNC_TORNEO_TO_MONGO] {e}")

@receiver(post_delete, sender=Torneo)
def delete_torneo_from_mongo(sender, instance, **kwargs):
    try:
        TorneoDoc.objects(postgres_id=instance.id).delete()
    except Exception as e:
        print(f"[ERROR EN DELETE_TORNEO_FROM_MONGO] {e}")

# ================================
# JUGADOR
# ================================
@receiver(post_save, sender=Jugador)
def sync_jugador_to_mongo(sender, instance, **kwargs):
    try:
        print(f"[SIGNAL] Sincronizando jugador '{instance.nombre}' (ID: {instance.id}) a MongoDB...")

        equipo_doc = EquipoDoc.objects(postgres_id=instance.equipo.id).first() if instance.equipo else None

        JugadorDoc.objects(postgres_id=instance.id).update_one(
            set__nombre=instance.nombre,
            set__apellido=instance.apellido,
            set__sexo=instance.sexo,
            set__numeroDocumento=instance.numeroDocumento,
            set__fechaNacimiento=instance.fechaNacimiento,
            set__nroCamiseta=instance.nroCamiseta,
            set__posicion=instance.posicion,
            set__equipo=equipo_doc,
            upsert=True
        )
    except Exception as e:
        print(f"[ERROR EN SYNC_JUGADOR_TO_MONGO] {e}")

@receiver(post_delete, sender=Jugador)
def delete_jugador_from_mongo(sender, instance, **kwargs):
    try:
        JugadorDoc.objects(postgres_id=instance.id).delete()
    except Exception as e:
        print(f"[ERROR EN DELETE_JUGADOR_FROM_MONGO] {e}")

# ================================
# PARTIDO
# ================================
@receiver(post_save, sender=Partido)
def sync_partido_to_mongo(sender, instance, **kwargs):
    try:
        torneo_doc = TorneoDoc.objects(postgres_id=instance.torneo.id).first() if instance.torneo else None
        equipo1_doc = EquipoDoc.objects(postgres_id=instance.equipo1.id).first() if instance.equipo1 else None
        equipo2_doc = EquipoDoc.objects(postgres_id=instance.equipo2.id).first() if instance.equipo2 else None
        cancha_doc = CanchaDoc.objects(postgres_id=instance.cancha.id).first() if instance.cancha else None

        PartidoDoc.objects(postgres_id=instance.id).update_one(
            set__fechaPartido=instance.fecha,
            set__horaPartido=instance.hora,
            set__resultado=instance.resultado,
            set__torneo=torneo_doc,
            set__equipo1=equipo1_doc,
            set__equipo2=equipo2_doc,
            set__cancha=cancha_doc,
            upsert=True
        )
    except Exception as e:
        print(f"[ERROR EN SYNC_PARTIDO_TO_MONGO] {e}")

@receiver(post_delete, sender=Partido)
def delete_partido_from_mongo(sender, instance, **kwargs):
    try:
        PartidoDoc.objects(postgres_id=instance.id).delete()
    except Exception as e:
        print(f"[ERROR EN DELETE_PARTIDO_FROM_MONGO] {e}")

# ================================
# INSCRIPCION
# ================================
@receiver(post_save, sender=Inscripcion)
def sync_inscripcion_to_mongo(sender, instance, **kwargs):
    try:
        equipo_doc = EquipoDoc.objects(postgres_id=instance.equipo.id).first() if instance.equipo else None
        torneo_doc = TorneoDoc.objects(postgres_id=instance.torneo.id).first() if instance.torneo else None
        categoria_doc = CategoriaDoc.objects(postgres_id=instance.categoria.id).first() if instance.categoria else None

        InscripcionDoc.objects(postgres_id=instance.id).update_one(
            set__equipo=equipo_doc,
            set__torneo=torneo_doc,
            set__categoria=categoria_doc,
            set__fechaInscripcion=instance.fecha_inscripcion,
            upsert=True
        )
    except Exception as e:
        print(f"[ERROR EN SYNC_INSCRIPCION_TO_MONGO] {e}")

@receiver(post_delete, sender=Inscripcion)
def delete_inscripcion_from_mongo(sender, instance, **kwargs):
    try:
        InscripcionDoc.objects(postgres_id=instance.id).delete()
    except Exception as e:
        print(f"[ERROR EN DELETE_INSCRIPCION_FROM_MONGO] {e}")

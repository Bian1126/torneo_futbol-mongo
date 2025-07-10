from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import (
    Equipo, Torneo, Jugador, Partido, Inscripcion,
    Cancha, Categoria, TipoDocumento, Ciudad
)
from .models_mongo import (
    Equipo as EquipoDoc,
    Torneo as TorneoDoc,
    Jugador as JugadorDoc,
    Partido as PartidoDoc,
    Inscripcion as InscripcionDoc,
    Cancha as CanchaDoc,
    Categoria as CategoriaDoc,
    TipoDocumento as TipoDocumentoDoc,
    Ciudad as CiudadDoc,
)

from mongoengine import connect, disconnect
import os

# Conectar a MongoDB
mongo_host = os.getenv("MONGO_HOST", "localhost")
mongo_port = os.getenv("MONGO_PORT", "27017")

disconnect(alias="default")

connect(
    db='torneo',
    host=f'mongodb://root:example@{mongo_host}:{mongo_port}/torneo?authSource=admin',
    alias="default"
)

# ================================
# TIPO DOCUMENTO
# ================================
@receiver(post_save, sender=TipoDocumento)
def sync_tipo_documento(sender, instance, **kwargs):
    try:
        TipoDocumentoDoc.objects(postgres_id=instance.id).update_one(
            set__nombre=instance.nombre.upper(),
            set__descripcion=instance.descripcion,
            upsert=True
        )
    except Exception as e:
        print(f"[ERROR EN SYNC_TIPO_DOCUMENTO] {e}")

@receiver(post_delete, sender=TipoDocumento)
def delete_tipo_documento(sender, instance, **kwargs):
    try:
        TipoDocumentoDoc.objects(postgres_id=instance.id).delete()
    except Exception as e:
        print(f"[ERROR EN DELETE_TIPO_DOCUMENTO] {e}")

# ================================
# CATEGORIA
# ================================
@receiver(post_save, sender=Categoria)
def sync_categoria(sender, instance, **kwargs):
    try:
        CategoriaDoc.objects(postgres_id=instance.id).update_one(
            set__nombre=instance.nombre.upper(),
            set__descripcion=instance.descripcion,
            upsert=True
        )
    except Exception as e:
        print(f"[ERROR EN SYNC_CATEGORIA] {e}")

@receiver(post_delete, sender=Categoria)
def delete_categoria(sender, instance, **kwargs):
    try:
        CategoriaDoc.objects(postgres_id=instance.id).delete()
    except Exception as e:
        print(f"[ERROR EN DELETE_CATEGORIA] {e}")

# ================================
# CANCHA
# ================================
@receiver(post_save, sender=Cancha)
def sync_cancha(sender, instance, **kwargs):
    try:
        CanchaDoc.objects(postgres_id=instance.id).update_one(
            set__nombre=instance.nombre,
            set__ubicacion=instance.ubicacion,
            upsert=True
        )
    except Exception as e:
        print(f"[ERROR EN SYNC_CANCHA] {e}")

@receiver(post_delete, sender=Cancha)
def delete_cancha(sender, instance, **kwargs):
    try:
        CanchaDoc.objects(postgres_id=instance.id).delete()
    except Exception as e:
        print(f"[ERROR EN DELETE_CANCHA] {e}")

# ================================
# EQUIPO
# ================================
@receiver(post_save, sender=Equipo)
def sync_equipo(sender, instance, **kwargs):
    try:
        ciudad_doc = CiudadDoc.objects(postgres_id=instance.ciudad.id).first()
        if ciudad_doc:
            EquipoDoc.objects(postgres_id=instance.id).update_one(
                set__nombre=instance.nombre,
                set__ciudad=ciudad_doc,
                set__ciudad_nombre=instance.ciudad.nombreCiudad if instance.ciudad else "",
                set__fechaDeFundacion=instance.fechaDeFundacion,
                upsert=True
            )
    except Exception as e:
        print(f"[ERROR EN SYNC_EQUIPO] {e}")


@receiver(post_delete, sender=Equipo)
def delete_equipo(sender, instance, **kwargs):
    try:
        EquipoDoc.objects(postgres_id=instance.id).delete()
    except Exception as e:
        print(f"[ERROR EN DELETE_EQUIPO] {e}")

# ================================
# CIUDAD
# ================================
@receiver(post_save, sender=Ciudad)
def sync_ciudad(sender, instance, **kwargs):
    try:
        CiudadDoc.objects(postgres_id=instance.id).update_one(
            set__nombreCiudad=instance.nombreCiudad,
            set__codigoPostal=instance.codigoPostal,
            set__provincia=instance.provincia,
            upsert=True
        )
    except Exception as e:
        print(f"[ERROR EN SYNC_CIUDAD] {e}")

@receiver(post_delete, sender=Ciudad)
def delete_ciudad(sender, instance, **kwargs):
    try:
        CiudadDoc.objects(postgres_id=instance.id).delete()
    except Exception as e:
        print(f"[ERROR EN DELETE_CIUDAD] {e}")

# ================================
# TORNEO
# ================================
@receiver(post_save, sender=Torneo)
def sync_torneo(sender, instance, **kwargs):
    try:
        categoria_doc = CategoriaDoc.objects(postgres_id=instance.categoria.id).first()
        if categoria_doc:
            TorneoDoc.objects(postgres_id=instance.id).update_one(
                set__nombre=instance.nombre,
                set__fechaInicio=instance.fechaInicio,
                set__fechaFin=instance.fechaFin,
                set__categoria=categoria_doc,
                upsert=True
            )
    except Exception as e:
        print(f"[ERROR EN SYNC_TORNEO] {e}")

@receiver(post_delete, sender=Torneo)
def delete_torneo(sender, instance, **kwargs):
    try:
        TorneoDoc.objects(postgres_id=instance.id).delete()
    except Exception as e:
        print(f"[ERROR EN DELETE_TORNEO] {e}")

# ================================
# JUGADOR
# ================================
@receiver(post_save, sender=Jugador)
def sync_jugador(sender, instance, **kwargs):
    try:
        equipo_doc = EquipoDoc.objects(postgres_id=instance.equipo.id).first()
        tipo_doc = TipoDocumentoDoc.objects(postgres_id=instance.tipoDocumento.id).first()
        if equipo_doc and tipo_doc:
            JugadorDoc.objects(postgres_id=instance.id).update_one(
                set__nombre=instance.nombre,
                set__apellido=instance.apellido,
                set__sexo=instance.sexo,
                set__numeroDocumento=instance.numeroDocumento,
                set__fechaNacimiento=instance.fechaNacimiento,
                set__nroCamiseta=instance.nroCamiseta,
                set__posicion=instance.posicion,
                set__equipo=equipo_doc,
                set__tipoDocumento=tipo_doc,
                upsert=True
            )
    except Exception as e:
        print(f"[ERROR EN SYNC_JUGADOR] {e}")

@receiver(post_delete, sender=Jugador)
def delete_jugador(sender, instance, **kwargs):
    try:
        JugadorDoc.objects(postgres_id=instance.id).delete()
    except Exception as e:
        print(f"[ERROR EN DELETE_JUGADOR] {e}")

# ================================
# PARTIDO
# ================================

@receiver(post_save, sender=Partido)
def sync_partido(sender, instance, **kwargs):
    try:
        equipo1_doc = EquipoDoc.objects(postgres_id=instance.equipo1.id).first()
        equipo2_doc = EquipoDoc.objects(postgres_id=instance.equipo2.id).first()
        torneo_doc = TorneoDoc.objects(postgres_id=instance.torneo.id).first()
        cancha_doc = CanchaDoc.objects(postgres_id=instance.cancha.id).first()

        if equipo1_doc and equipo2_doc and torneo_doc and cancha_doc:
            PartidoDoc.objects(postgres_id=instance.id).update_one(
                set__fechaPartido=instance.fechaPartido,
                set__horaPartido=str(instance.horaPartido),
                set__resultado=instance.resultado,
                set__equipo1=equipo1_doc,
                set__equipo1_nombre=instance.equipo1.nombre if instance.equipo1 else "",
                set__equipo2=equipo2_doc,
                set__equipo2_nombre=instance.equipo2.nombre if instance.equipo2 else "",
                set__cancha=cancha_doc,
                set__cancha_nombre=instance.cancha.nombre if instance.cancha else "",
                set__torneo=torneo_doc,
                set__torneo_nombre=instance.torneo.nombre if instance.torneo else "",
                upsert=True
            )
    except Exception as e:
        print(f"[ERROR EN SYNC_PARTIDO] {e}")

@receiver(post_delete, sender=Partido)
def delete_partido(sender, instance, **kwargs):
    try:
        PartidoDoc.objects(postgres_id=instance.id).delete()
    except Exception as e:
        print(f"[ERROR EN DELETE_PARTIDO] {e}")
# ================================
# INSCRIPCION
# ================================
@receiver(post_save, sender=Inscripcion)
def sync_inscripcion(sender, instance, **kwargs):
    try:
        equipo_doc = EquipoDoc.objects(postgres_id=instance.equipo.id).first()
        torneo_doc = TorneoDoc.objects(postgres_id=instance.torneo.id).first()
        categoria_doc = CategoriaDoc.objects(postgres_id=instance.categoria.id).first()

        if equipo_doc and torneo_doc and categoria_doc:
           InscripcionDoc.objects(postgres_id=instance.id).update_one(
               set__equipo=equipo_doc,
               set__equipo_nombre=instance.equipo.nombre if instance.equipo else "",
               set__categoria=categoria_doc,
               set__categoria_nombre=instance.categoria.nombre if instance.categoria else "",
               set__torneo=torneo_doc,
               set__torneo_nombre=instance.torneo.nombre if instance.torneo else "",
               set__fechaInscripcion=instance.fechaInscripcion,
               upsert=True
               )

    except Exception as e:
        print(f"[ERROR EN SYNC_INSCRIPCION] {e}")

@receiver(post_delete, sender=Inscripcion)
def delete_inscripcion(sender, instance, **kwargs):
    try:
        InscripcionDoc.objects(postgres_id=instance.id).delete()
    except Exception as e:
        print(f"[ERROR EN DELETE_INSCRIPCION] {e}")

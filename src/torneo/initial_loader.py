#!/usr/bin/env python
"""
Archivo de carga para pasar los datos de PostgreSQL a MongoDB
Basado en la estructura que usan tus compañeros
"""
import os
import sys
import django
from datetime import datetime

# Configurar Django - ajustar el path para encontrar el módulo app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

# Importar modelos de PostgreSQL y MongoDB
from torneo.models import (
    TipoDocumento as TipoDocumentoSQL,
    Categoria as CategoriaSQL,
    Equipo as EquipoSQL,
    Jugador as JugadorSQL,
    Cancha as CanchaSQL,
    Torneo as TorneoSQL,
    Inscripcion as InscripcionSQL,
    Partido as PartidoSQL
)

from torneo.models_mongo import (
    TipoDocumento as TipoDocumentoMongo,
    Categoria as CategoriaMongo,
    Equipo as EquipoMongo,
    Jugador as JugadorMongo,
    Cancha as CanchaMongo,
    Torneo as TorneoMongo,
    Inscripcion as InscripcionMongo,
    Partido as PartidoMongo
)


def clear_mongo_collections():
    """Limpiar todas las colecciones de MongoDB"""
    print("🗑️ Limpiando colecciones de MongoDB...")
    TipoDocumentoMongo.drop_collection()
    CategoriaMongo.drop_collection()
    EquipoMongo.drop_collection()
    JugadorMongo.drop_collection()
    CanchaMongo.drop_collection()
    TorneoMongo.drop_collection()
    InscripcionMongo.drop_collection()
    PartidoMongo.drop_collection()
    print("✅ Colecciones limpiadas")


def migrate_tipo_documento():
    """Migrar tipos de documento de PostgreSQL a MongoDB"""
    print("📄 Migrando tipos de documento...")
    for tipo_sql in TipoDocumentoSQL.objects.all():
        TipoDocumentoMongo(
            postgres_id=tipo_sql.id,
            nombre=tipo_sql.nombre,
            descripcion=tipo_sql.descripcion or ""
        ).save()
    print(f"✅ {TipoDocumentoSQL.objects.count()} tipos de documento migrados")


def migrate_categoria():
    """Migrar categorías de PostgreSQL a MongoDB"""
    print("📋 Migrando categorías...")
    for categoria_sql in CategoriaSQL.objects.all():
        CategoriaMongo(
            postgres_id=categoria_sql.id,
            nombre=categoria_sql.nombre,
            descripcion=categoria_sql.descripcion or ""
        ).save()
    print(f"✅ {CategoriaSQL.objects.count()} categorías migradas")


def migrate_equipo():
    """Migrar equipos de PostgreSQL a MongoDB"""
    print("⚽ Migrando equipos...")
    for equipo_sql in EquipoSQL.objects.all():
        EquipoMongo(
            postgres_id=equipo_sql.id,
            nombre=equipo_sql.nombre,
            ciudad=equipo_sql.ciudad,
            fechaDeFundacion=equipo_sql.fechaDeFundacion
        ).save()
    print(f"✅ {EquipoSQL.objects.count()} equipos migrados")


def migrate_cancha():
    """Migrar canchas de PostgreSQL a MongoDB"""
    print("🏟️ Migrando canchas...")
    for cancha_sql in CanchaSQL.objects.all():
        CanchaMongo(
            postgres_id=cancha_sql.id,
            nombre=cancha_sql.nombre,
            ubicacion=cancha_sql.ubicacion
        ).save()
    print(f"✅ {CanchaSQL.objects.count()} canchas migradas")


def migrate_torneo():
    """Migrar torneos de PostgreSQL a MongoDB"""
    print("🏆 Migrando torneos...")
    for torneo_sql in TorneoSQL.objects.all():
        categoria_mongo = CategoriaMongo.objects.get(postgres_id=torneo_sql.categoria.id)
        
        TorneoMongo(
            postgres_id=torneo_sql.id,
            nombre=torneo_sql.nombre,
            fechaInicio=torneo_sql.fechaInicio,
            fechaFin=torneo_sql.fechaFin,
            categoria=categoria_mongo
        ).save()
    print(f"✅ {TorneoSQL.objects.count()} torneos migrados")


def migrate_jugador():
    """Migrar jugadores de PostgreSQL a MongoDB"""
    print("👤 Migrando jugadores...")
    for jugador_sql in JugadorSQL.objects.all():
        tipo_doc_mongo = TipoDocumentoMongo.objects.get(postgres_id=jugador_sql.tipoDocumento.id)
        equipo_mongo = EquipoMongo.objects.get(postgres_id=jugador_sql.equipo.id)
        
        JugadorMongo(
            postgres_id=jugador_sql.id,
            nombre=jugador_sql.nombre,
            apellido=jugador_sql.apellido,
            sexo=jugador_sql.sexo,
            numeroDocumento=jugador_sql.numeroDocumento,
            fechaNacimiento=jugador_sql.fechaNacimiento,
            nroCamiseta=jugador_sql.nroCamiseta,
            posicion=jugador_sql.posicion,
            tipoDocumento=tipo_doc_mongo,
            equipo=equipo_mongo
        ).save()
    print(f"✅ {JugadorSQL.objects.count()} jugadores migrados")


def migrate_inscripcion():
    """Migrar inscripciones de PostgreSQL a MongoDB"""
    print("📝 Migrando inscripciones...")
    for inscripcion_sql in InscripcionSQL.objects.all():
        equipo_mongo = EquipoMongo.objects.get(postgres_id=inscripcion_sql.equipo.id)
        categoria_mongo = CategoriaMongo.objects.get(postgres_id=inscripcion_sql.categoria.id)
        torneo_mongo = TorneoMongo.objects.get(postgres_id=inscripcion_sql.torneo.id)
        
        InscripcionMongo(
            postgres_id=inscripcion_sql.id,
            fechaInscripcion=inscripcion_sql.fechaInscripcion,
            equipo=equipo_mongo,
            categoria=categoria_mongo,
            torneo=torneo_mongo
        ).save()
    print(f"✅ {InscripcionSQL.objects.count()} inscripciones migradas")


def migrate_partido():
    """Migrar partidos de PostgreSQL a MongoDB"""
    print("🥅 Migrando partidos...")
    for partido_sql in PartidoSQL.objects.all():
        equipo1_mongo = EquipoMongo.objects.get(postgres_id=partido_sql.equipo1.id)
        equipo2_mongo = EquipoMongo.objects.get(postgres_id=partido_sql.equipo2.id)
        cancha_mongo = CanchaMongo.objects.get(postgres_id=partido_sql.cancha.id)
        torneo_mongo = TorneoMongo.objects.get(postgres_id=partido_sql.torneo.id)
        
        PartidoMongo(
            postgres_id=partido_sql.id,
            fechaPartido=partido_sql.fechaPartido,
            horaPartido=str(partido_sql.horaPartido),  # Convertir TimeField a string
            resultado=partido_sql.resultado or "",
            equipo1=equipo1_mongo,
            equipo2=equipo2_mongo,
            cancha=cancha_mongo,
            torneo=torneo_mongo
        ).save()
    print(f"✅ {PartidoSQL.objects.count()} partidos migrados")


def main():
    """Función principal de migración"""
    print("=" * 50)
    print("🚀 INICIANDO MIGRACIÓN DE POSTGRESQL A MONGODB")
    print("=" * 50)
    
    try:
        # Limpiar MongoDB
        clear_mongo_collections()
        print()
        
        # Migrar en orden de dependencias
        migrate_tipo_documento()
        migrate_categoria()
        migrate_equipo()
        migrate_cancha()
        migrate_torneo()
        migrate_jugador()
        migrate_inscripcion()
        migrate_partido()
        
        print()
        print("🎉 ¡MIGRACIÓN COMPLETADA EXITOSAMENTE!")
        print("📊 Resumen de datos migrados:")
        print(f"   - Tipos de documento: {TipoDocumentoMongo.objects.count()}")
        print(f"   - Categorías: {CategoriaMongo.objects.count()}")
        print(f"   - Equipos: {EquipoMongo.objects.count()}")
        print(f"   - Canchas: {CanchaMongo.objects.count()}")
        print(f"   - Torneos: {TorneoMongo.objects.count()}")
        print(f"   - Jugadores: {JugadorMongo.objects.count()}")
        print(f"   - Inscripciones: {InscripcionMongo.objects.count()}")
        print(f"   - Partidos: {PartidoMongo.objects.count()}")
        print()
        print("🔍 Ahora puedes ver los datos en MongoDB Compass:")
        print("   URI: mongodb://root:example@localhost:27019/torneo?authSource=admin")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

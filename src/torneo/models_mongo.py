from mongoengine import (
    Document, EmbeddedDocument,
    StringField, DecimalField, IntField, DateField, DateTimeField,
    ReferenceField, ListField, EmbeddedDocumentField, CASCADE
)


# Clases abstractas
class NombreAbstract(Document):
    meta = {
        'abstract': True,
        'ordering': ['nombre']
    }

    nombre = StringField(required=True, max_length=200)

    def clean(self):
        if self.nombre:
            self.nombre = self.nombre.upper()

    def __str__(self):
        return self.nombre


class BaseModel(Document):
    meta = {'abstract': True}


# -------------------------
# MODELOS PRINCIPALES MONGODB
# -------------------------

# Tipo de documento para el jugador
class TipoDocumento(NombreAbstract):
    postgres_id = IntField(required=True, unique=True)
    nombre = StringField(required=True, max_length=200)
    descripcion = StringField(required=False)


# Equipo que participa en los torneos
class Equipo(Document):
    postgres_id = IntField(required=True, unique=True)
    nombre = StringField(required=True, max_length=100)
    ciudad = StringField(required=True, max_length=100)
    fechaDeFundacion = DateField(required=True)

    def __str__(self):
        return self.nombre


# Jugador que pertenece a un equipo
class Jugador(Document):
    postgres_id = IntField(required=True, unique=True)
    nombre = StringField(required=True, max_length=100)
    apellido = StringField(required=True, max_length=100)
    sexo = StringField(required=True, max_length=10)
    numeroDocumento = IntField(required=True)
    fechaNacimiento = DateField(required=True)
    nroCamiseta = IntField(required=True)
    posicion = StringField(required=True, max_length=50)

    tipoDocumento = ReferenceField(TipoDocumento, reverse_delete_rule=CASCADE)
    equipo = ReferenceField(Equipo, reverse_delete_rule=CASCADE)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


# Cancha donde se juegan los partidos
class Cancha(Document):
    postgres_id = IntField(required=True, unique=True)
    nombre = StringField(required=True, max_length=100)
    ubicacion = StringField(required=True, max_length=200)

    def __str__(self):
        return self.nombre


# Categoría del torneo
class Categoria(NombreAbstract):
    postgres_id = IntField(required=True, unique=True)
    nombre = StringField(required=True, max_length=200)
    descripcion = StringField(required=False)


# Torneo organizado
class Torneo(Document):
    postgres_id = IntField(required=True, unique=True)
    nombre = StringField(required=True, max_length=100)
    fechaInicio = DateField(required=True)
    fechaFin = DateField(required=True)

    categoria = ReferenceField(Categoria, reverse_delete_rule=CASCADE)

    def __str__(self):
        return self.nombre


# Relación entre equipo y torneo (inscripción)
class Inscripcion(Document):
    postgres_id = IntField(required=True, unique=True)
    fechaInscripcion = DateField(required=True)

    equipo = ReferenceField(Equipo, reverse_delete_rule=CASCADE)
    categoria = ReferenceField(Categoria, reverse_delete_rule=CASCADE)
    torneo = ReferenceField(Torneo, reverse_delete_rule=CASCADE)

    def __str__(self):
        return f'{self.equipo.nombre} - {self.torneo.nombre} ({self.categoria.nombre})'


# Partido jugado entre dos equipos
class Partido(Document):
    postgres_id = IntField(required=True, unique=True)
    fechaPartido = DateField(required=True)
    horaPartido = StringField(required=True)  # Guardamos como string para simplicidad
    resultado = StringField(required=False, max_length=50)

    equipo1 = ReferenceField(Equipo, reverse_delete_rule=CASCADE)
    equipo2 = ReferenceField(Equipo, reverse_delete_rule=CASCADE)
    cancha = ReferenceField(Cancha, reverse_delete_rule=CASCADE)
    torneo = ReferenceField(Torneo, reverse_delete_rule=CASCADE)

    def __str__(self):
        return f'{self.equipo1.nombre} vs {self.equipo2.nombre}'
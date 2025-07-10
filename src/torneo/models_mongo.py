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


# Ciudad del equipo
class Ciudad(Document):
    postgres_id = IntField(required=True, unique=True)
    nombreCiudad = StringField(required=True, max_length=100)
    codigoPostal = StringField(required=True, max_length=10)
    provincia = StringField(required=True, max_length=100)

    def __str__(self):
        return self.nombreCiudad


# Equipo que participa en los torneos
class Equipo(Document):
    postgres_id = IntField(required=True, unique=True)
    nombre = StringField(required=True, max_length=100)
    ciudad = ReferenceField(Ciudad, reverse_delete_rule=CASCADE)
    ciudad_nombre = StringField()
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

    # Campos nuevos para mostrar en texto
    equipo_nombre = StringField()
    tipo_documento_nombre = StringField()

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

    # Campos nuevos para mostrar en texto
    categoria_nombre = StringField()

    def __str__(self):
        return self.nombre


# Relación entre equipo y torneo (inscripción)
class Inscripcion(Document):
    postgres_id = IntField(required=True, unique=True)
    fechaInscripcion = DateField(required=True)

    equipo = ReferenceField(Equipo, reverse_delete_rule=CASCADE)
    categoria = ReferenceField(Categoria, reverse_delete_rule=CASCADE)
    torneo = ReferenceField(Torneo, reverse_delete_rule=CASCADE)

    # Campos nuevos para mostrar en texto
    equipo_nombre = StringField()
    categoria_nombre = StringField()
    torneo_nombre = StringField()



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

    # NUEVOS CAMPOS DE TEXTO
    equipo1_nombre = StringField()
    equipo2_nombre = StringField()
    cancha_nombre = StringField()
    torneo_nombre = StringField()

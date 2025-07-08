from django.db import models
from django.utils.translation import gettext_lazy as _

# -------------------------
# CLASES ABSTRACTAS BASE
# -------------------------

# Reutilizable para cualquier modelo que tenga solo un campo "nombre"
class NombreAbstract(models.Model):
    nombre = models.CharField(
        _('Nombre'),
        help_text=_('Nombre descriptivo'),
        max_length=200,
    )

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        abstract = True
        ordering = ['nombre']

# Base general para heredar si hace falta en el futuro
class BaseModel(models.Model):
    class Meta:
        abstract = True


# -------------------------
# MODELOS PRINCIPALES
# -------------------------

# Tipo de documento para el jugador
class TipoDocumento(NombreAbstract):
    descripcion = models.TextField(_('Descripción'), blank=True, null=True)

    class Meta:
        verbose_name = 'Tipo de documento'
        verbose_name_plural = 'Tipos de documento'


# Equipo que participa en los torneos
class Equipo(models.Model):
    nombre = models.CharField(_('Nombre del equipo'), max_length=100)
    ciudad = models.CharField(_('Ciudad'), max_length=100)
    fechaDeFundacion = models.DateField(_('Fecha de fundación'))

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'


# Jugador que pertenece a un equipo
class Jugador(models.Model):
    nombre = models.CharField(_('Nombre'), max_length=100)
    apellido = models.CharField(_('Apellido'), max_length=100)
    sexo = models.CharField(_('Sexo'), max_length=10)
    numeroDocumento = models.BigIntegerField(_('Número de documento'))
    fechaNacimiento = models.DateField(_('Fecha de nacimiento'))
    nroCamiseta = models.IntegerField(_('Número de camiseta'))
    posicion = models.CharField(_('Posición'), max_length=50)

    tipoDocumento = models.ForeignKey(
        TipoDocumento,
        on_delete=models.PROTECT,
        verbose_name=_('Tipo de documento')
    )
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        verbose_name=_('Equipo')
    )

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    class Meta:
        verbose_name = 'Jugador'
        verbose_name_plural = 'Jugadores'


# Cancha donde se juegan los partidos
class Cancha(models.Model):
    nombre = models.CharField(_('Nombre de la cancha'), max_length=100)
    ubicacion = models.CharField(_('Ubicación'), max_length=200)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Cancha'
        verbose_name_plural = 'Canchas'


# Categoría del torneo (ej: Infantil, Juvenil, Libre, etc.)
class Categoria(NombreAbstract):
    descripcion = models.TextField(_('Descripción'), blank=True, null=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'


# Torneo organizado
class Torneo(models.Model):
    nombre = models.CharField(_('Nombre del torneo'), max_length=100)
    fechaInicio = models.DateField(_('Fecha de inicio'))
    fechaFin = models.DateField(_('Fecha de fin'))

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        verbose_name=_('Categoría')
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Torneo'
        verbose_name_plural = 'Torneos'


# Relación entre equipo y torneo (inscripción)
class Inscripcion(models.Model):
    fechaInscripcion = models.DateField(_('Fecha de inscripción'))

    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        verbose_name=_('Equipo')
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        verbose_name=_('Categoría'),
        default=1  # Categoría por defecto temporal
    )
    torneo = models.ForeignKey(
        Torneo,
        on_delete=models.CASCADE,
        verbose_name=_('Torneo')
    )

    def __str__(self):
        return f'{self.equipo.nombre} - {self.torneo.nombre} ({self.categoria.nombre})'

    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'


# Partido jugado entre dos equipos
class Partido(models.Model):
    fechaPartido = models.DateField(_('Fecha del partido'))
    horaPartido = models.TimeField(_('Hora del partido'))
    resultado = models.CharField(_('Resultado'), max_length=50, blank=True)

    equipo1 = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name='partidos_equipo1',
        verbose_name=_('Equipo 1')
    )
    equipo2 = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name='partidos_equipo2',
        verbose_name=_('Equipo 2')
    )
    cancha = models.ForeignKey(
        Cancha,
        on_delete=models.PROTECT,
        verbose_name=_('Cancha')
    )
    torneo = models.ForeignKey(
        Torneo,
        on_delete=models.CASCADE,
        verbose_name=_('Torneo')
    )

    def __str__(self):
        return f'{self.equipo1.nombre} vs {self.equipo2.nombre}'

    class Meta:
        verbose_name = 'Partido'
        verbose_name_plural = 'Partidos'
        ordering = ['fechaPartido', 'horaPartido']

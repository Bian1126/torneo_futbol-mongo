from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from torneo.models import *


# -------------------------------
# TIPO DOCUMENTO
# -------------------------------
@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ['nombre']


# -------------------------------
# EQUIPO
# -------------------------------
@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad', 'fechaDeFundacion')
    search_fields = ['nombre', 'ciudad']
    list_filter = ['ciudad']


# -------------------------------
# JUGADOR
# -------------------------------
@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'equipo', 'numeroDocumento', 'posicion')
    search_fields = ['nombre', 'apellido', 'numeroDocumento']
    list_filter = ['equipo', 'posicion', 'tipoDocumento']


# -------------------------------
# CANCHA
# -------------------------------
@admin.register(Cancha)
class CanchaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion')
    search_fields = ['nombre']


# -------------------------------
# CATEGORÍA
# -------------------------------
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ['nombre']


# -------------------------------
# INLINE INSCRIPCIÓN (Dentro del Torneo)
# -------------------------------

class InscripcionInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        equipos = []
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                equipo = form.cleaned_data.get('equipo')
                if equipo in equipos:
                    raise ValidationError("Un equipo no puede inscribirse más de una vez al mismo torneo.")
                equipos.append(equipo)

class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    extra = 0
    formset = InscripcionInlineFormset
    verbose_name = "Inscripción de equipo"
    verbose_name_plural = "Inscripciones de equipos"


# -------------------------------
# INLINE PARTIDOS (Dentro del Torneo)
# -------------------------------

class PartidoInline(admin.TabularInline):
    model = Partido
    extra = 0
    verbose_name = "Partido del torneo"
    verbose_name_plural = "Partidos del torneo"


# -------------------------------
# TORNEO
# -------------------------------
@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fechaInicio', 'fechaFin', 'categoria', 'total_partidos')
    list_filter = ['categoria']
    search_fields = ['nombre']
    inlines = [InscripcionInline, PartidoInline]
    ordering = ['fechaInicio']

    def total_partidos(self, obj):
        return obj.partido_set.count()
    total_partidos.short_description = 'Cantidad de partidos'


# -------------------------------
# INSCRIPCIÓN (por fuera también)
# -------------------------------
@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'torneo', 'fechaInscripcion')
    search_fields = ['equipo__nombre', 'torneo__nombre']
    list_filter = ['torneo', 'equipo']


# -------------------------------
# PARTIDO
# -------------------------------
@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ('fechaPartido', 'horaPartido', 'equipo1', 'equipo2', 'resultado', 'torneo', 'cancha')
    list_filter = ['torneo', 'cancha']
    search_fields = ['equipo1__nombre', 'equipo2__nombre']
    ordering = ['fechaPartido', 'horaPartido']

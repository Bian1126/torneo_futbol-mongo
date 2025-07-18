# Generated by Django 5.2.4 on 2025-07-07 22:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cancha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre de la cancha')),
                ('ubicacion', models.CharField(max_length=200, verbose_name='Ubicación')),
            ],
            options={
                'verbose_name': 'Cancha',
                'verbose_name_plural': 'Canchas',
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Nombre descriptivo', max_length=200, verbose_name='Nombre')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
            },
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del equipo')),
                ('ciudad', models.CharField(max_length=100, verbose_name='Ciudad')),
                ('fechaDeFundacion', models.DateField(verbose_name='Fecha de fundación')),
            ],
            options={
                'verbose_name': 'Equipo',
                'verbose_name_plural': 'Equipos',
            },
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Nombre descriptivo', max_length=200, verbose_name='Nombre')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Tipo de documento',
                'verbose_name_plural': 'Tipos de documento',
            },
        ),
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=100, verbose_name='Apellido')),
                ('sexo', models.CharField(max_length=10, verbose_name='Sexo')),
                ('numeroDocumento', models.BigIntegerField(verbose_name='Número de documento')),
                ('fechaNacimiento', models.DateField(verbose_name='Fecha de nacimiento')),
                ('nroCamiseta', models.IntegerField(verbose_name='Número de camiseta')),
                ('posicion', models.CharField(max_length=50, verbose_name='Posición')),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='torneo.equipo', verbose_name='Equipo')),
                ('tipoDocumento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='torneo.tipodocumento', verbose_name='Tipo de documento')),
            ],
            options={
                'verbose_name': 'Jugador',
                'verbose_name_plural': 'Jugadores',
            },
        ),
        migrations.CreateModel(
            name='Torneo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del torneo')),
                ('fechaInicio', models.DateField(verbose_name='Fecha de inicio')),
                ('fechaFin', models.DateField(verbose_name='Fecha de fin')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='torneo.categoria', verbose_name='Categoría')),
            ],
            options={
                'verbose_name': 'Torneo',
                'verbose_name_plural': 'Torneos',
            },
        ),
        migrations.CreateModel(
            name='Partido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaPartido', models.DateField(verbose_name='Fecha del partido')),
                ('horaPartido', models.TimeField(verbose_name='Hora del partido')),
                ('resultado', models.CharField(blank=True, max_length=50, verbose_name='Resultado')),
                ('cancha', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='torneo.cancha', verbose_name='Cancha')),
                ('equipo1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partidos_equipo1', to='torneo.equipo', verbose_name='Equipo 1')),
                ('equipo2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partidos_equipo2', to='torneo.equipo', verbose_name='Equipo 2')),
                ('torneo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='torneo.torneo', verbose_name='Torneo')),
            ],
            options={
                'verbose_name': 'Partido',
                'verbose_name_plural': 'Partidos',
                'ordering': ['fechaPartido', 'horaPartido'],
            },
        ),
        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaInscripcion', models.DateField(verbose_name='Fecha de inscripción')),
                ('categoria', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='torneo.categoria', verbose_name='Categoría')),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='torneo.equipo', verbose_name='Equipo')),
                ('torneo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='torneo.torneo', verbose_name='Torneo')),
            ],
            options={
                'verbose_name': 'Inscripción',
                'verbose_name_plural': 'Inscripciones',
            },
        ),
    ]

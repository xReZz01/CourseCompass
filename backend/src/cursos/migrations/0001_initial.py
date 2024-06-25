# Generated by Django 5.0.6 on 2024-06-24 20:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('año', models.PositiveIntegerField()),
                ('horario', models.CharField(max_length=50)),
                ('contraseña_matriculacion', models.CharField(max_length=50)),
                ('profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cursos', to='accounts.profesor')),
            ],
            options={
                'ordering': ['año', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha_entrega', models.DateTimeField()),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tareas', to='cursos.curso')),
            ],
            options={
                'ordering': ['fecha_entrega'],
            },
        ),
        migrations.CreateModel(
            name='Entrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='entregas/')),
                ('comentario', models.TextField(blank=True, null=True)),
                ('fecha_entrega', models.DateTimeField(auto_now_add=True)),
                ('calificacion', models.FloatField(blank=True, null=True)),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entregas', to='accounts.alumno')),
                ('tarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entregas', to='cursos.tarea')),
            ],
            options={
                'ordering': ['fecha_entrega'],
            },
        ),
        migrations.CreateModel(
            name='InscripcionMateria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inscripcion', models.DateField()),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.alumno')),
            ],
            options={
                'db_table': 'inscripciones_estudiantes',
                'unique_together': {('estudiante', 'curso')},
            },
        ),
    ]

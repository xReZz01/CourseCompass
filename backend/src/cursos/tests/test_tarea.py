from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from cursos.models.curso import Curso
from cursos.models.tarea import Tarea
from cursos.models.entrega import Entrega
from accounts.models.profesor import Profesor
from accounts.models.alumno import Alumno
from django.utils.timezone import make_aware
import datetime

class TareaTestCase(TestCase):
    def setUp(self):
        self.user_profesor = get_user_model().objects.create_user(
            dni='12345678',
            nombre='ProfesorNombre',
            apellido='ProfesorApellido',
            correo='profesor@example.com',
            fecha_nacimiento='1980-01-01',
            password='password'
        )
        self.profesor = Profesor.objects.create(
            usuario=self.user_profesor,
            legajo_profesor=124
        )
        self.curso = Curso.objects.create(
            nombre='Curso de Prueba',
            descripcion='Descripción de prueba',
            año=2024,
            horario='Lunes 10:00 - 20:00',
            contraseña_matriculacion='testpass',
            profesor=self.profesor
        )
        self.user_alumno = get_user_model().objects.create_user(
            dni='87654321',
            nombre='AlumnoNombre',
            apellido='AlumnoApellido',
            correo='alumno@example.com',
            fecha_nacimiento='2000-01-01',
            password='password'
        )
        self.alumno = Alumno.objects.create(
            usuario=self.user_alumno,
            legajo_alumno=123
        )
        self.tarea = Tarea.objects.create(
            curso=self.curso,
            titulo='Tarea de Prueba',
            descripcion='Descripción de la tarea',
            fecha_entrega=make_aware(datetime.datetime(2024, 7, 8, 17, 0, 0))
        )
    def test_crear_tarea(self):
        self.client.login(dni='12345678', password='password')
        response = self.client.post(reverse('crear_tarea', kwargs={'curso_id': self.curso.id}), {
        'titulo': 'Nueva Tarea',
        'descripcion': 'Descripción de la nueva tarea',
        'fecha_entrega': '2024-08-07 20:00:00',
        })
        if response.status_code == 400:
            print(response.json())  # Imprimir el contenido de la respuesta en caso de error
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Tarea.objects.filter(titulo='Nueva Tarea').exists())

    def test_entregar_tarea(self):
        self.client.login(dni='87654321', password='password')
        with open('cursos/tests/fixtures/test_file.txt', 'w') as f:
            f.write('contenido de prueba')
        with open('cursos/tests/fixtures/test_file.txt', 'rb') as f:
            response = self.client.post(reverse('entregar_tarea', kwargs={'tarea_id': self.tarea.id}), {
                'archivo': f,
                'comentario': 'Comentario de prueba'
            })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Entrega.objects.filter(tarea=self.tarea, estudiante=self.alumno).exists())

    def test_tarea_detalle(self):
        self.client.login(dni='12345678', password='password')
        response = self.client.get(reverse('tarea_detalle', kwargs={'tarea_id': self.tarea.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tarea.titulo)
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from datetime import time

# ===============================
# USUARIO
# ===============================

class Usuario(AbstractUser):

    ROLE_CHOICES = [
        ('alumno', 'Alumno'),
        ('profesor', 'Profesor'),
        ('administrador', 'Administrador'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


# ===============================
# CARRERA
# ===============================

class Carrera(models.Model):

    nombre = models.CharField(max_length=150)

    clave = models.CharField(max_length=10, unique=True, null=True, blank=True)

    def __str__(self):
        return self.nombre


# ===============================
# GRUPO
# ===============================

class Grupo(models.Model):

    nombre = models.CharField(max_length=20)

    cuatrimestre = models.IntegerField(
        choices=[(i, i) for i in range(1, 11)],
        null=True,
        blank=True
    )

    carrera = models.ForeignKey(
        Carrera,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nombre


# ===============================
# PROFESOR
# ===============================

class Profesor(models.Model):

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    numero_empleado = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    especialidad = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    nombre = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.nombre if self.nombre else "Profesor"


# ===============================
# ALUMNO
# ===============================

class Alumno(models.Model):

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    matricula = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    nombre = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    carrera = models.ForeignKey(
        Carrera,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.matricula if self.matricula else "Alumno"


# ===============================
# MATERIA
# ===============================

class Materia(models.Model):

    nombre = models.CharField(max_length=150)

    clave = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    carrera = models.ForeignKey(
        Carrera,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nombre


# ===============================
# AULA
# ===============================

class Aula(models.Model):

    nombre = models.CharField(max_length=20)

    edificio = models.CharField(max_length=20, null=True, blank=True)

    capacidad = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre


# ===============================
# HORARIO
# ===============================

class Horario(models.Model):

    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miercoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
    ]

    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)

    dia = models.CharField(max_length=10, choices=DIAS_SEMANA)

    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def clean(self):

        if self.hora_inicio >= self.hora_fin:
            raise ValidationError("La hora de inicio debe ser menor que la hora de fin")

        if self.hora_inicio < time(8, 0) or self.hora_fin > time(19, 0):
            raise ValidationError("Los horarios deben estar entre 08:00 y 19:00")

        conflicto_profesor = Horario.objects.filter(
            profesor=self.profesor,
            dia=self.dia
        ).exclude(id=self.id).filter(
            hora_inicio__lt=self.hora_fin,
            hora_fin__gt=self.hora_inicio
        )

        if conflicto_profesor.exists():
            raise ValidationError("El profesor ya tiene una clase en ese horario")

        conflicto_aula = Horario.objects.filter(
            aula=self.aula,
            dia=self.dia
        ).exclude(id=self.id).filter(
            hora_inicio__lt=self.hora_fin,
            hora_fin__gt=self.hora_inicio
        )

        if conflicto_aula.exists():
            raise ValidationError("El aula ya está ocupada en ese horario")

        conflicto_grupo = Horario.objects.filter(
            grupo=self.grupo,
            dia=self.dia
        ).exclude(id=self.id).filter(
            hora_inicio__lt=self.hora_fin,
            hora_fin__gt=self.hora_inicio
        )

        if conflicto_grupo.exists():
            raise ValidationError("El grupo ya tiene una materia en ese horario")

    def __str__(self):
        return f"{self.materia} - {self.grupo}"
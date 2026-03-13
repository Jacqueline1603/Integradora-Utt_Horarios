from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Horario, Alumno, Profesor, Aula


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            if user.role == "administrador":
                return redirect("admin_dashboard")

            elif user.role == "profesor":
                return redirect("horario_profesor")

            elif user.role == "alumno":
                return redirect("horario_alumno")

        else:
            return render(request, "horarios/login.html", {
                "error": "Usuario o contraseña incorrectos"
            })

    return render(request, "horarios/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")

def admin_dashboard(request):

    total_alumnos = Alumno.objects.count()
    total_profesores = Profesor.objects.count()
    total_horarios = Horario.objects.count()

    context = {
        "total_alumnos": total_alumnos,
        "total_profesores": total_profesores,
        "total_horarios": total_horarios,
    }

    return render(request, "horarios/admin_dashboard.html", context)


def profesor_dashboard(request):
    return render(request, "horarios/profesor_dashboard.html")


def alumno_dashboard(request):
    return render(request, "horarios/alumno_dashboard.html")

def lista_horarios(request):

    horarios = Horario.objects.all()

    profesor = request.GET.get("profesor")
    grupo = request.GET.get("grupo")
    dia = request.GET.get("dia")

    if profesor:
        horarios = horarios.filter(profesor__nombre__icontains=profesor)

    if grupo:
        horarios = horarios.filter(grupo__nombre__icontains=grupo)

    if dia:
        horarios = horarios.filter(dia=dia)

    context = {
        "horarios": horarios
    }

    return render(request, "horarios/lista_horarios.html", context)


def calendario(request):
    return render(request, "horarios/calendario.html")


def horario_alumno(request):

    alumno = Alumno.objects.get(usuario=request.user)

    horarios = Horario.objects.filter(grupo=alumno.grupo)

    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]

    horas = sorted(set([h.hora_inicio.strftime("%H:%M") for h in horarios]))

    tabla = {}

    for hora in horas:
        tabla[hora] = {}
        for dia in dias:
            tabla[hora][dia] = None

    for h in horarios:
        hora = h.hora_inicio.strftime("%H:%M")
        tabla[hora][h.dia] = h

    return render(request, "horarios/horario_semanal.html", {
        "tabla": tabla,
        "dias": dias
    })


def horario_profesor(request):

    profesor = Profesor.objects.get(usuario=request.user)

    horarios = Horario.objects.filter(profesor=profesor)

    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]

    horas = sorted(set([h.hora_inicio.strftime("%H:%M") for h in horarios]))

    tabla = {}

    for hora in horas:
        tabla[hora] = {}
        for dia in dias:
            tabla[hora][dia] = None

    for h in horarios:
        hora = h.hora_inicio.strftime("%H:%M")
        tabla[hora][h.dia] = h

    return render(request, "horarios/horario_semanal.html", {
        "tabla": tabla,
        "dias": dias
    })

def editar_aula(request, horario_id):

    horario = get_object_or_404(Horario, id=horario_id)

    aulas = Aula.objects.all()

    if request.method == "POST":

        aula_id = request.POST.get("aula")
        aula = Aula.objects.get(id=aula_id)

        horario.aula = aula
        horario.save()

        return redirect("horario_semanal")

    return render(request, "horarios/editar_aula.html", {
        "horario": horario,
        "aulas": aulas
    })

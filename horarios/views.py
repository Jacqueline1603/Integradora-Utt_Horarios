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
                return redirect("profesor_dashboard")

            elif user.role == "alumno":
                return redirect("alumno_dashboard")

        else:
            return render(request, "horarios/login.html", {
                "error": "Usuario o contraseña incorrectos"
            })

    return render(request, "horarios/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def admin_dashboard(request):
    return render(request, "horarios/admin_dashboard.html")


def profesor_dashboard(request):
    return render(request, "horarios/profesor_dashboard.html")


def alumno_dashboard(request):
    return render(request, "horarios/alumno_dashboard.html")


def lista_horarios(request):

    horarios = Horario.objects.all()

    return render(request, "horarios/lista_horarios.html", {
        "horarios": horarios
    })


def calendario(request):
    return render(request, "horarios/calendario.html")


def horario_semanal(request):

    horarios = Horario.objects.all()

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

    contexto = {
        "tabla": tabla,
        "dias": dias
    }

    return render(request, "horarios/horario_semanal.html", contexto)

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
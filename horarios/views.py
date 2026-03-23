from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Horario, Alumno, Profesor, Aula, Materia, Grupo, Carrera, Usuario
# from django.contrib.auth.models import User 

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

@login_required
def admin_dashboard(request):
    if request.user.role == "profesor":
        return redirect("profesor_dashboard")
    elif request.user.role == "alumno":
        return redirect("alumno_dashboard")

    if request.method == "POST":

        tipo = request.POST.get("tipo")

        # 🔹 PROFESOR
        if tipo == "profesor":
            nombre = request.POST.get("nombre")
            user = Usuario.objects.create_user(
                username=nombre,
                email= nombre + '@correo.com',
                password= nombre,
                role='profesor'
            )
            Profesor.objects.create(nombre=nombre, usuario=user)

        elif tipo == "editar_profesor":
            id = request.POST.get("id")
            nombre = request.POST.get("nombre")
            p = Profesor.objects.get(id=id)
            p.nombre = nombre
            p.save()

        elif tipo == "eliminar_profesor":
            id = request.POST.get("id")
            Profesor.objects.get(id=id).delete()

        # 🔹 MATERIA
        elif tipo == "materia":
            nombre = request.POST.get("nombre")
            Materia.objects.create(nombre=nombre)

        elif tipo == "editar_materia":
            id = request.POST.get("id")
            nombre = request.POST.get("nombre")
            m = Materia.objects.get(id=id)
            m.nombre = nombre
            m.save()

        elif tipo == "eliminar_materia":
            id = request.POST.get("id")
            Materia.objects.get(id=id).delete()

        # 🔹 GRUPO
        elif tipo == "grupo":
            print (request.POST)
            #id = request.POST.get("id")
            nombre = request.POST.get("nombre")
            cuatrimestre = request.POST.get("cuatrimestre")
            carrera_id = request.POST.get("carrera")

            g = Grupo() #.objects.get(id=id)
            g.nombre = nombre
            g.cuatrimestre = cuatrimestre
            g.carrera = Carrera.objects.get(id=carrera_id)
            g.save()
            
        # 🔹 AULA
        elif tipo == "aula":
            nombre = request.POST.get("nombre")
            Aula.objects.create(nombre=nombre)

        # 🔹 ALUMNO
        elif tipo == "alumno":
            print (request.POST)
            nombre = request.POST.get("nombre")
            matricula = request.POST.get("matricula")
            grupo = Grupo.objects.get(id=request.POST.get("grupo"))

            user = Usuario.objects.create_user(
                username=matricula,
                email= nombre + '@correo.com',
                password= matricula,
                role='alumno'
            )

            Alumno.objects.create(
                usuario = user, 
                nombre=nombre,
                matricula=matricula,
                grupo=grupo
             )
        elif tipo == "horario":
            print(request.POST)
            profesor = Profesor.objects.get(id=request.POST.get("profesor"))

            materia = Materia.objects.get(id=request.POST.get("materia"))
            grupo = Grupo.objects.get(id=request.POST.get("grupo"))
            aula = Aula.objects.get(id=request.POST.get("aula"))
            dia = request.POST.get("dia")
            hora_inicio = request.POST.get("inicio")
            hora_fin =request.POST.get("fin") 
            print(hora_fin, hora_inicio)
            horario = Horario(profesor=profesor, materia=materia, grupo=grupo, aula=aula, dia=dia, hora_inicio=hora_inicio, hora_fin=hora_fin)
            horario.save()
    # 🔹 DATOS PARA MOSTRAR
    context = {
        "profesores": Profesor.objects.all(),
        "materias": Materia.objects.all(),
        "grupos": Grupo.objects.all(),
        "aulas": Aula.objects.all(),
        "carreras": Carrera.objects.all(),
        "total_profesores": Profesor.objects.count(),
        "total_materias": Materia.objects.count(),
        "total_grupos": Grupo.objects.count(),
        "total_alumnos": Alumno.objects.count(),
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
        horarios = horarios.filter(profesor__usuario__first_name__icontains=profesor)

    if grupo:
        horarios = horarios.filter(grupo__nombre__icontains=grupo)

    if dia:
        horarios = horarios.filter(dia=dia)

    return render(request, "horarios/lista_horarios.html", {
        "horarios": horarios
    })

def calendario(request):
    return render(request, "horarios/calendario.html")

def editar_aula(request, id):

    horario = get_object_or_404(Horario, id=id)
    aulas = Aula.objects.all()

    if request.method == "POST":
        aula_id = request.POST.get("aula")
        aula = Aula.objects.get(id=aula_id)

        horario.aula = aula
        horario.save()

        return redirect("horario_profesor")  # o la vista que uses

    return render(request, "horarios/editar_aula.html", {
        "horario": horario,
        "aulas": aulas
    })

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

def lista_profesores(request):
    return render(request, 'horarios/lista_profesores.html')

def lista_alumnos(request):
    return render(request, 'horarios/lista_alumnos.html')

def lista_materias(request):
    return render(request, 'horarios/lista_materias.html')

def lista_aulas(request):
    return render(request, 'horarios/lista_aulas.html')
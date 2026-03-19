from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('profesor-dashboard/', views.profesor_dashboard, name='profesor_dashboard'),
    path('alumno-dashboard/', views.alumno_dashboard, name='alumno_dashboard'),

    path('calendario/', views.calendario, name='calendario'),

    path('editar-aula/<int:id>/', views.editar_aula, name='editar_aula'),

    path('horario-alumno/', views.horario_alumno, name='horario_alumno'),
    path('horario-profesor/', views.horario_profesor, name='horario_profesor'),

    # 🔥 AGREGA TODO AQUÍ DENTRO
    path('horarios/', views.lista_horarios, name='lista_horarios'),
     
    path('profesores/', views.lista_profesores, name='lista_profesores'),
path('alumnos/', views.lista_alumnos, name='lista_alumnos'),
path('materias/', views.lista_materias, name='lista_materias'),
path('aulas/', views.lista_aulas, name='lista_aulas'),
    # ⚠️ ESTAS SOLO SI EXISTEN EN views.py
    # Si no existen, mejor bórralas
    # path('horarios/crear/', views.crear_horario, name='crear_horario'),
    # path('horarios/editar/<int:id>/', views.editar_horario, name='editar_horario'),
    # path('horarios/eliminar/<int:id>/', views.eliminar_horario, name='eliminar_horario'),
]
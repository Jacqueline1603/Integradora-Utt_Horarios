from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('profesor-dashboard/', views.profesor_dashboard, name='profesor_dashboard'),
    path('alumno-dashboard/', views.alumno_dashboard, name='alumno_dashboard'),

    path('horarios/', views.lista_horarios, name='lista_horarios'),
    path('calendario/', views.calendario, name='calendario'),

    path('editar-aula/<int:id>/', views.editar_aula, name='editar_aula'),

    path('horario-alumno/', views.horario_alumno, name='horario_alumno'),
    path('horario-profesor/', views.horario_profesor, name='horario_profesor'),

]
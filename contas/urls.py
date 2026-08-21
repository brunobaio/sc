from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_cliente, name='login'),
    path('logout/', views.logout_cliente, name='logout'),
    path('perfil/', views.perfil, name='perfil'),

    # Recuperação de senha
    path('esqueci-senha/', views.esqueci_senha, name='esqueci_senha'),
]
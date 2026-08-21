from django.contrib import admin
from django.urls import include, path


urlpatterns = [

    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "",
        include("paginas.urls"),
    ),

    path(
        "contas/",
        include("contas.urls"),
    ),

    path(
        "agendamento/",
        include("agendamentos.urls"),
    ),

    path(
        "painel/funcionarios/",
        include("funcionarios.urls"),
    ),

    path(
        "painel/",
        include("painel.urls"),
    ),

]
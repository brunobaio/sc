from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.lista_funcionarios,
        name="lista_funcionarios",
    ),

    path(
        "cadastrar/",
        views.cadastrar_funcionario,
        name="cadastrar_funcionario",
    ),

    path(
        "<int:funcionario_id>/editar/",
        views.editar_funcionario,
        name="editar_funcionario",
    ),

    path(
        "<int:funcionario_id>/alterar-situacao/",
        views.alterar_situacao_funcionario,
        name="alterar_situacao_funcionario",
    ),

]
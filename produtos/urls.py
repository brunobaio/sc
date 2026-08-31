from django.urls import path

from . import views


urlpatterns = [

    # ======================================================
    # PÁGINA PÚBLICA
    # ======================================================

    path(
        "",
        views.lista_produtos,
        name="lista_produtos",
    ),


    # ======================================================
    # PAINEL ADMINISTRATIVO
    # ======================================================

    path(
        "painel/",
        views.painel_produtos,
        name="painel_produtos",
    ),

    path(
        "painel/novo/",
        views.cadastrar_produto,
        name="cadastrar_produto",
    ),

    path(
        "painel/<int:produto_id>/editar/",
        views.editar_produto,
        name="editar_produto",
    ),

    path(
        "painel/<int:produto_id>/status/",
        views.alterar_status_produto,
        name="alterar_status_produto",
    ),

    path(
        "painel/<int:produto_id>/excluir/",
        views.excluir_produto,
        name="excluir_produto",
    ),

]
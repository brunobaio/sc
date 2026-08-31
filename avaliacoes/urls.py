from django.urls import path

from . import views


urlpatterns = [

    # ======================================================
    # ÁREA PÚBLICA
    # ======================================================

    path(
        "",
        views.lista_avaliacoes,
        name="lista_avaliacoes",
    ),

    path(
        "nova/",
        views.cadastrar_avaliacao,
        name="cadastrar_avaliacao",
    ),


    # ======================================================
    # PAINEL ADMINISTRATIVO
    # ======================================================

    path(
        "painel/",
        views.painel_avaliacoes,
        name="painel_avaliacoes",
    ),

    path(
        "painel/<int:avaliacao_id>/aprovar/",
        views.aprovar_avaliacao,
        name="aprovar_avaliacao",
    ),

    path(
        "painel/<int:avaliacao_id>/desaprovar/",
        views.desaprovar_avaliacao,
        name="desaprovar_avaliacao",
    ),

    path(
        "painel/<int:avaliacao_id>/excluir/",
        views.excluir_avaliacao,
        name="excluir_avaliacao",
    ),
]
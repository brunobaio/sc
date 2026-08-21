from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.agendamento,
        name="agendamento",
    ),

    path(
        "funcionarios-disponiveis/",
        views.funcionarios_disponiveis,
        name="funcionarios_disponiveis",
    ),

    path(
        "horarios-disponiveis/",
        views.horarios_disponiveis,
        name="horarios_disponiveis",
    ),

    path(
        "datas-indisponiveis/",
        views.datas_indisponiveis,
        name="datas_indisponiveis",
    ),

    path(
        "cancelar/<int:agendamento_id>/",
        views.cancelar_agendamento,
        name="cancelar_agendamento",
    ),
]
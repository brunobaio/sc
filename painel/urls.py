from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.dashboard,
        name="painel_dashboard",
    ),

    path(
        "agendamentos/",
        views.lista_agendamentos,
        name="painel_agendamentos",
    ),

    path(
        "agendamentos/<int:agendamento_id>/alterar-status/",
        views.alterar_status_agendamento,
        name="painel_alterar_status",
    ),
]
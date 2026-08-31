from django.urls import path

from . import views


urlpatterns = [

    # ==========================================
    # DASHBOARD
    # ==========================================

    path(
        "",
        views.dashboard,
        name="painel_dashboard",
    ),


    # ==========================================
    # AGENDAMENTOS
    # ==========================================

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


    # ==========================================
    # RELATÓRIOS
    # ==========================================

    path(
        "relatorios/",
        views.relatorio_atendimentos,
        name="painel_relatorios",
    ),

]
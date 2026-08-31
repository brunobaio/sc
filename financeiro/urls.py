from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.dashboard_financeiro,
        name="financeiro_dashboard",
    ),

    path(
        "receita/<int:receita_id>/pagar/",
        views.registrar_pagamento,
        name="financeiro_registrar_pagamento",
    ),

    path(
        "receita/<int:receita_id>/pendente/",
        views.marcar_como_pendente,
        name="financeiro_marcar_pendente",
    ),
]
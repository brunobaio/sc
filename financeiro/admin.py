from django.contrib import admin

from .models import Receita


@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):

    list_display = (
        "agendamento",
        "valor",
        "forma_pagamento",
        "pago",
        "data_pagamento",
        "criado_em",
    )

    list_filter = (
        "pago",
        "forma_pagamento",
        "data_pagamento",
        "criado_em",
    )

    search_fields = (
        "agendamento__cliente__first_name",
        "agendamento__cliente__username",
        "agendamento__cliente__email",
        "agendamento__servico__nome",
        "agendamento__funcionario__nome",
    )

    ordering = (
        "-criado_em",
    )

    readonly_fields = (
        "criado_em",
        "atualizado_em",
    )

    fieldsets = (
        (
            "Atendimento",
            {
                "fields": (
                    "agendamento",
                    "valor",
                )
            },
        ),

        (
            "Pagamento",
            {
                "fields": (
                    "forma_pagamento",
                    "pago",
                    "data_pagamento",
                    "observacao",
                )
            },
        ),

        (
            "Controle",
            {
                "fields": (
                    "criado_em",
                    "atualizado_em",
                )
            },
        ),
    )
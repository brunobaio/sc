from django.contrib import admin

from .models import Avaliacao


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):

    list_display = (
        "cliente",
        "nota",
        "aprovado",
        "criado_em",
    )

    list_filter = (
        "aprovado",
        "nota",
        "criado_em",
    )

    search_fields = (
        "cliente__username",
        "cliente__first_name",
        "cliente__email",
        "comentario",
    )

    ordering = (
        "-criado_em",
    )

    list_editable = (
        "aprovado",
    )

    readonly_fields = (
        "cliente",
        "nota",
        "comentario",
        "criado_em",
        "atualizado_em",
    )

    fieldsets = (

        (
            "Cliente",
            {
                "fields": (
                    "cliente",
                )
            },
        ),

        (
            "Avaliação",
            {
                "fields": (
                    "nota",
                    "comentario",
                )
            },
        ),

        (
            "Publicação",
            {
                "fields": (
                    "aprovado",
                )
            },
        ),

        (
            "Datas",
            {
                "fields": (
                    "criado_em",
                    "atualizado_em",
                )
            },
        ),

    )
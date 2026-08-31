from django.contrib import admin

from .models import Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):

    list_display = (
        "nome",
        "preco",
        "estoque",
        "ativo",
        "criado_em",
        "atualizado_em",
    )

    list_filter = (
        "ativo",
        "criado_em",
    )

    search_fields = (
        "nome",
        "descricao",
    )

    ordering = (
        "nome",
    )

    list_editable = (
        "preco",
        "estoque",
        "ativo",
    )

    fieldsets = (

        (
            "Informações do produto",
            {
                "fields": (
                    "nome",
                    "descricao",
                    "imagem",
                )
            }
        ),

        (
            "Venda e disponibilidade",
            {
                "fields": (
                    "preco",
                    "estoque",
                    "ativo",
                )
            }
        ),

    )
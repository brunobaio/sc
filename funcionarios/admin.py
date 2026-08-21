from django.contrib import admin

from .models import Funcionario


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):

    list_display = (
        "nome",
        "cargo",
        "telefone",
        "ativo",
        "data_admissao",
    )

    list_filter = (
        "ativo",
        "cargo",
    )

    search_fields = (
        "nome",
        "cpf",
        "telefone",
        "email",
    )

    filter_horizontal = (
        "servicos",
    )

    ordering = (
        "nome",
    )
from django.contrib import admin

from .models import DataBloqueada, HorarioFuncionamento


@admin.register(HorarioFuncionamento)
class HorarioFuncionamentoAdmin(admin.ModelAdmin):

    list_display = (
        "dia_formatado",
        "aberto",
        "hora_abertura",
        "hora_fechamento",
    )

    list_editable = (
        "aberto",
        "hora_abertura",
        "hora_fechamento",
    )

    ordering = ("dia_semana",)

    def dia_formatado(self, obj):
        return obj.get_dia_semana_display()

    dia_formatado.short_description = "Dia da semana"


@admin.register(DataBloqueada)
class DataBloqueadaAdmin(admin.ModelAdmin):

    list_display = (
        "data",
        "dia_inteiro",
        "hora_inicio",
        "hora_fim",
        "motivo",
    )

    list_filter = (
        "dia_inteiro",
        "data",
    )

    search_fields = (
        "motivo",
    )

    ordering = ("data",)
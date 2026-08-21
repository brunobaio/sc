from django.contrib import admin
from django.contrib import messages

from .models import Agendamento


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):

    list_display = (
        "cliente",
        "servico",
        "funcionario",
        "data",
        "horario",
        "status",
        "criado_em",
    )

    list_filter = (
        "status",
        "data",
        "servico",
        "funcionario",
    )

    search_fields = (
        "cliente__username",
        "cliente__first_name",
        "cliente__email",
        "servico__nome",
        "funcionario__nome",
    )

    ordering = (
        "-data",
        "-horario",
    )

    readonly_fields = (
        "criado_em",
        "atualizado_em",
    )

    list_per_page = 30

    actions = [
        "confirmar_agendamentos",
        "marcar_como_concluido",
        "marcar_desistencia",
        "marcar_nao_compareceu",
        "cancelar_pelo_salao",
    ]

    fieldsets = (

        (
            "Dados do agendamento",
            {
                "fields": (
                    "cliente",
                    "servico",
                    "funcionario",
                    "data",
                    "horario",
                    "observacao",
                )
            },
        ),

        (
            "Situação do atendimento",
            {
                "fields": (
                    "status",
                    "motivo_status",
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

    @admin.action(
        description="Confirmar agendamentos selecionados"
    )
    def confirmar_agendamentos(
        self,
        request,
        queryset,
    ):

        quantidade = queryset.update(
            status=Agendamento.STATUS_CONFIRMADO,
            motivo_status=(
                "Agendamento confirmado pela administradora."
            ),
        )

        self.message_user(
            request,
            (
                f"{quantidade} agendamento(s) "
                "confirmado(s)."
            ),
            messages.SUCCESS,
        )

    @admin.action(
        description="Marcar como concluído"
    )
    def marcar_como_concluido(
        self,
        request,
        queryset,
    ):

        quantidade = queryset.update(
            status=Agendamento.STATUS_CONCLUIDO,
            motivo_status=(
                "Atendimento realizado e concluído."
            ),
        )

        self.message_user(
            request,
            (
                f"{quantidade} atendimento(s) "
                "concluído(s)."
            ),
            messages.SUCCESS,
        )

    @admin.action(
        description="Marcar desistência"
    )
    def marcar_desistencia(
        self,
        request,
        queryset,
    ):

        quantidade = queryset.update(
            status=Agendamento.STATUS_DESISTENCIA,
            motivo_status=(
                "Cliente informou a desistência."
            ),
        )

        self.message_user(
            request,
            (
                f"{quantidade} agendamento(s) "
                "marcado(s) como desistência."
            ),
            messages.WARNING,
        )

    @admin.action(
        description="Marcar como não compareceu"
    )
    def marcar_nao_compareceu(
        self,
        request,
        queryset,
    ):

        quantidade = queryset.update(
            status=Agendamento.STATUS_NAO_COMPARECEU,
            motivo_status=(
                "Cliente não compareceu ao atendimento."
            ),
        )

        self.message_user(
            request,
            (
                f"{quantidade} agendamento(s) "
                "marcado(s) como ausência."
            ),
            messages.WARNING,
        )

    @admin.action(
        description="Cancelar pelo salão"
    )
    def cancelar_pelo_salao(
        self,
        request,
        queryset,
    ):

        quantidade = queryset.update(
            status=Agendamento.STATUS_CANCELADO_ADMIN,
            motivo_status=(
                "Agendamento cancelado pelo salão."
            ),
        )

        self.message_user(
            request,
            (
                f"{quantidade} agendamento(s) "
                "cancelado(s)."
            ),
            messages.ERROR,
        )
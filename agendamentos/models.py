from django.conf import settings
from django.db import models

from funcionarios.models import Funcionario
from servicos.models import Servico


class Agendamento(models.Model):

    STATUS_PENDENTE = "PENDENTE"
    STATUS_CONFIRMADO = "CONFIRMADO"
    STATUS_CANCELADO_CLIENTE = "CANCELADO_CLIENTE"
    STATUS_CANCELADO_ADMIN = "CANCELADO_ADMIN"
    STATUS_DESISTENCIA = "DESISTENCIA"
    STATUS_NAO_COMPARECEU = "NAO_COMPARECEU"
    STATUS_CONCLUIDO = "CONCLUIDO"

    STATUS_CHOICES = [
        (
            STATUS_PENDENTE,
            "Pendente",
        ),
        (
            STATUS_CONFIRMADO,
            "Confirmado",
        ),
        (
            STATUS_CANCELADO_CLIENTE,
            "Cancelado pela cliente",
        ),
        (
            STATUS_CANCELADO_ADMIN,
            "Cancelado pelo salão",
        ),
        (
            STATUS_DESISTENCIA,
            "Desistência informada",
        ),
        (
            STATUS_NAO_COMPARECEU,
            "Não compareceu",
        ),
        (
            STATUS_CONCLUIDO,
            "Concluído",
        ),
    ]

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="agendamentos",
        verbose_name="Cliente",
    )

    servico = models.ForeignKey(
        Servico,
        on_delete=models.PROTECT,
        related_name="agendamentos",
        verbose_name="Serviço",
    )

    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.PROTECT,
        related_name="agendamentos",
        verbose_name="Profissional",
        null=True,
        blank=True,
    )

    data = models.DateField(
        verbose_name="Data",
    )

    horario = models.TimeField(
        verbose_name="Horário",
    )

    observacao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observação da cliente",
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_PENDENTE,
        verbose_name="Status",
    )

    motivo_status = models.TextField(
        blank=True,
        verbose_name="Motivo ou observação do status",
        help_text=(
            "Exemplo: cliente ligou informando que não poderá comparecer."
        ),
    )

    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em",
    )

    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em",
    )

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"

        ordering = [
            "-data",
            "-horario",
        ]

    def __str__(self):

        profissional = (
            self.funcionario.nome
            if self.funcionario
            else "Sem profissional"
        )

        return (
            f"{self.cliente} - "
            f"{self.servico} - "
            f"{profissional} - "
            f"{self.data:%d/%m/%Y} "
            f"{self.horario:%H:%M}"
        )

    @property
    def esta_cancelado(self):

        return self.status in {
            self.STATUS_CANCELADO_CLIENTE,
            self.STATUS_CANCELADO_ADMIN,
            self.STATUS_DESISTENCIA,
            self.STATUS_NAO_COMPARECEU,
        }

    @property
    def pode_cliente_cancelar(self):

        return self.status in {
            self.STATUS_PENDENTE,
            self.STATUS_CONFIRMADO,
        }

    @property
    def ocupa_horario(self):

        return self.status in {
            self.STATUS_PENDENTE,
            self.STATUS_CONFIRMADO,
        }
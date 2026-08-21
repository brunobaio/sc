from django.db import models

from agendamentos.models import Agendamento


class Receita(models.Model):

    FORMA_PIX = "PIX"
    FORMA_DINHEIRO = "DINHEIRO"
    FORMA_DEBITO = "DEBITO"
    FORMA_CREDITO = "CREDITO"
    FORMA_OUTRO = "OUTRO"

    FORMAS_PAGAMENTO = [
        (
            FORMA_PIX,
            "PIX",
        ),
        (
            FORMA_DINHEIRO,
            "Dinheiro",
        ),
        (
            FORMA_DEBITO,
            "Cartão de débito",
        ),
        (
            FORMA_CREDITO,
            "Cartão de crédito",
        ),
        (
            FORMA_OUTRO,
            "Outro",
        ),
    ]

    agendamento = models.OneToOneField(
        Agendamento,
        on_delete=models.CASCADE,
        related_name="receita",
        verbose_name="Agendamento",
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor",
    )

    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMAS_PAGAMENTO,
        blank=True,
        verbose_name="Forma de pagamento",
    )

    pago = models.BooleanField(
        default=False,
        verbose_name="Pago",
    )

    data_pagamento = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data do pagamento",
    )

    observacao = models.TextField(
        blank=True,
        verbose_name="Observação",
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
        verbose_name = "Receita"
        verbose_name_plural = "Receitas"

        ordering = [
            "-criado_em",
        ]

    def __str__(self):

        cliente = (
            self.agendamento.cliente.first_name
            or self.agendamento.cliente.username
        )

        return (
            f"{cliente} - "
            f"{self.agendamento.servico.nome} - "
            f"R$ {self.valor}"
        )
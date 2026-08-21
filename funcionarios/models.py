from django.db import models

from servicos.models import Servico


class Funcionario(models.Model):

    CARGO_CABELEIREIRA = "CABELEIREIRA"
    CARGO_MANICURE = "MANICURE"
    CARGO_MAQUIADORA = "MAQUIADORA"
    CARGO_DESIGNER_SOBRANCELHAS = "DESIGNER_SOBRANCELHAS"
    CARGO_ESTETICISTA = "ESTETICISTA"
    CARGO_RECEPCIONISTA = "RECEPCIONISTA"
    CARGO_OUTRO = "OUTRO"

    CARGOS = [
        (
            CARGO_CABELEIREIRA,
            "Cabeleireira",
        ),
        (
            CARGO_MANICURE,
            "Manicure e pedicure",
        ),
        (
            CARGO_MAQUIADORA,
            "Maquiadora",
        ),
        (
            CARGO_DESIGNER_SOBRANCELHAS,
            "Designer de sobrancelhas",
        ),
        (
            CARGO_ESTETICISTA,
            "Esteticista",
        ),
        (
            CARGO_RECEPCIONISTA,
            "Recepcionista",
        ),
        (
            CARGO_OUTRO,
            "Outro",
        ),
    ]

    nome = models.CharField(
        max_length=150,
        verbose_name="Nome completo",
    )

    cpf = models.CharField(
        max_length=14,
        unique=True,
        verbose_name="CPF",
    )

    telefone = models.CharField(
        max_length=20,
        verbose_name="Telefone",
    )

    email = models.EmailField(
        blank=True,
        verbose_name="E-mail",
    )

    cargo = models.CharField(
        max_length=40,
        choices=CARGOS,
        verbose_name="Cargo",
    )

    data_admissao = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de admissão",
    )

    servicos = models.ManyToManyField(
        Servico,
        blank=True,
        related_name="funcionarios",
        verbose_name="Serviços realizados",
    )

    ativo = models.BooleanField(
        default=True,
        verbose_name="Funcionário ativo",
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
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} - {self.get_cargo_display()}"
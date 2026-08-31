from django.conf import settings
from django.db import models


class Avaliacao(models.Model):

    NOTAS = [
        (1, "1 estrela"),
        (2, "2 estrelas"),
        (3, "3 estrelas"),
        (4, "4 estrelas"),
        (5, "5 estrelas"),
    ]

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="avaliacoes",
        verbose_name="Cliente",
    )

    nota = models.PositiveSmallIntegerField(
        "Nota",
        choices=NOTAS,
    )

    comentario = models.TextField(
        "Comentário",
        max_length=500,
    )

    aprovado = models.BooleanField(
        "Aprovado",
        default=False,
    )

    criado_em = models.DateTimeField(
        "Criado em",
        auto_now_add=True,
    )

    atualizado_em = models.DateTimeField(
        "Atualizado em",
        auto_now=True,
    )

    def __str__(self):
        return f"{self.cliente} - {self.nota} estrelas"

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        ordering = ["-criado_em"]
from django.db import models


class Produto(models.Model):

    nome = models.CharField(
        "Nome",
        max_length=120
    )

    descricao = models.TextField(
        "Descrição",
        blank=True
    )

    preco = models.DecimalField(
        "Preço",
        max_digits=8,
        decimal_places=2
    )

    estoque = models.PositiveIntegerField(
        "Estoque",
        default=0
    )

    imagem = models.ImageField(
        "Imagem",
        upload_to="produtos/",
        blank=True,
        null=True
    )

    ativo = models.BooleanField(
        "Disponível",
        default=True
    )

    criado_em = models.DateTimeField(
        "Criado em",
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        "Atualizado em",
        auto_now=True
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["nome"]
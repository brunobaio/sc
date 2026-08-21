from django.db import models

class Servico(models.Model):
    nome = models.CharField("Nome", max_length=100)
    descricao = models.TextField("Descrição", blank=True)
    preco = models.DecimalField("Preço", max_digits=8, decimal_places=2)
    duracao = models.PositiveIntegerField("Duração (minutos)")
    ativo = models.BooleanField("Disponível", default=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
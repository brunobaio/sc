from django.db import models


class HorarioFuncionamento(models.Model):

    DIAS_SEMANA = [
        (0, "Segunda-feira"),
        (1, "Terça-feira"),
        (2, "Quarta-feira"),
        (3, "Quinta-feira"),
        (4, "Sexta-feira"),
        (5, "Sábado"),
        (6, "Domingo"),
    ]

    dia_semana = models.PositiveSmallIntegerField(
        choices=DIAS_SEMANA,
        unique=True,
        verbose_name="Dia da semana",
    )

    aberto = models.BooleanField(
        default=True,
        verbose_name="Salão aberto",
    )

    hora_abertura = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Hora de abertura",
    )

    hora_fechamento = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Hora de fechamento",
    )

    class Meta:
        verbose_name = "Horário de funcionamento"
        verbose_name_plural = "Horários de funcionamento"
        ordering = ["dia_semana"]

    def __str__(self):

        if not self.aberto:
            return f"{self.get_dia_semana_display()} - Fechado"

        abertura = (
            self.hora_abertura.strftime("%H:%M")
            if self.hora_abertura
            else "Não definida"
        )

        fechamento = (
            self.hora_fechamento.strftime("%H:%M")
            if self.hora_fechamento
            else "Não definido"
        )

        return (
            f"{self.get_dia_semana_display()} - "
            f"{abertura} às {fechamento}"
        )


class DataBloqueada(models.Model):

    data = models.DateField(
        unique=True,
        verbose_name="Data bloqueada",
    )

    motivo = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Motivo",
        help_text="Exemplo: viagem, férias, feriado ou curso.",
    )

    dia_inteiro = models.BooleanField(
        default=True,
        verbose_name="Bloquear o dia inteiro",
    )

    hora_inicio = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Bloquear a partir de",
    )

    hora_fim = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Bloquear até",
    )

    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em",
    )

    class Meta:
        verbose_name = "Data bloqueada"
        verbose_name_plural = "Datas bloqueadas"
        ordering = ["data"]

    def __str__(self):

        if self.dia_inteiro:
            return f"{self.data:%d/%m/%Y} - Dia inteiro"

        return (
            f"{self.data:%d/%m/%Y} - "
            f"{self.hora_inicio:%H:%M} às "
            f"{self.hora_fim:%H:%M}"
        )
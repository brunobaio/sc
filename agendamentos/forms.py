from datetime import date, datetime

from django import forms
from django.utils import timezone

from funcionarios.models import Funcionario
from servicos.models import Servico

from .models import Agendamento


class AgendamentoForm(forms.ModelForm):

    horario = forms.TimeField(
        label="Horário",
        input_formats=[
            "%H:%M",
        ],
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "id_horario",
            }
        ),
    )

    class Meta:
        model = Agendamento

        fields = [
            "servico",
            "funcionario",
            "data",
            "horario",
            "observacao",
        ]

        labels = {
            "servico": "Serviço",
            "funcionario": "Profissional",
            "data": "Data",
            "horario": "Horário",
            "observacao": "Observação",
        }

        widgets = {

            "servico": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "id_servico",
                }
            ),

            "funcionario": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "id_funcionario",
                }
            ),

            "data": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "id": "id_data",
                }
            ),

            "observacao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Alguma observação?",
                    "rows": 4,
                }
            ),
        }

    def __init__(
        self,
        *args,
        horarios_disponiveis=None,
        **kwargs,
    ):

        super().__init__(*args, **kwargs)

        # Somente serviços ativos
        self.fields["servico"].queryset = (
            Servico.objects
            .filter(
                ativo=True
            )
            .order_by(
                "nome"
            )
        )

        # Inicialmente não mostra nenhum funcionário
        self.fields["funcionario"].queryset = (
            Funcionario.objects.none()
        )

        self.fields["funcionario"].empty_label = (
            "Selecione primeiro um serviço"
        )

        # Se estiver enviando o formulário via POST
        if "servico" in self.data:

            try:

                servico_id = int(
                    self.data.get(
                        "servico"
                    )
                )

                self.fields["funcionario"].queryset = (
                    Funcionario.objects
                    .filter(
                        ativo=True,
                        servicos__id=servico_id,
                    )
                    .distinct()
                    .order_by(
                        "nome"
                    )
                )

                self.fields["funcionario"].empty_label = (
                    "Escolha um profissional"
                )

            except (
                ValueError,
                TypeError,
            ):
                pass

        # Se estiver editando um agendamento existente
        elif (
            self.instance.pk
            and self.instance.servico_id
        ):

            self.fields["funcionario"].queryset = (
                Funcionario.objects
                .filter(
                    ativo=True,
                    servicos=self.instance.servico,
                )
                .distinct()
                .order_by(
                    "nome"
                )
            )

        # Bloqueia datas anteriores visualmente
        self.fields["data"].widget.attrs["min"] = (
            timezone.localdate().isoformat()
        )

        # Horários iniciais
        escolhas_horario = [
            (
                "",
                (
                    "Selecione serviço, profissional "
                    "e data"
                ),
            )
        ]

        if horarios_disponiveis:

            escolhas_horario = [
                (
                    horario,
                    horario,
                )
                for horario in horarios_disponiveis
            ]

            escolhas_horario.insert(
                0,
                (
                    "",
                    "Escolha um horário",
                ),
            )

        self.fields["horario"].widget.choices = (
            escolhas_horario
        )

    def clean_data(self):

        data_agendamento = (
            self.cleaned_data.get(
                "data"
            )
        )

        if not data_agendamento:
            return data_agendamento

        if (
            data_agendamento
            < timezone.localdate()
        ):

            raise forms.ValidationError(
                (
                    "Não é permitido agendar "
                    "em uma data anterior."
                )
            )

        return data_agendamento

    def clean_funcionario(self):

        funcionario = (
            self.cleaned_data.get(
                "funcionario"
            )
        )

        servico = (
            self.cleaned_data.get(
                "servico"
            )
        )

        if (
            funcionario
            and servico
        ):

            realiza_servico = (
                funcionario.servicos
                .filter(
                    id=servico.id
                )
                .exists()
            )

            if not realiza_servico:

                raise forms.ValidationError(
                    (
                        "Este profissional não realiza "
                        "o serviço selecionado."
                    )
                )

            if not funcionario.ativo:

                raise forms.ValidationError(
                    (
                        "Este profissional não está "
                        "disponível para agendamentos."
                    )
                )

        return funcionario

    def clean(self):

        cleaned_data = super().clean()

        data_agendamento = (
            cleaned_data.get(
                "data"
            )
        )

        horario_agendamento = (
            cleaned_data.get(
                "horario"
            )
        )

        if (
            not data_agendamento
            or not horario_agendamento
        ):
            return cleaned_data

        agora = timezone.localtime()

        data_hora_agendamento = (
            timezone.make_aware(
                datetime.combine(
                    data_agendamento,
                    horario_agendamento,
                ),
                timezone.get_current_timezone(),
            )
        )

        if data_hora_agendamento <= agora:

            raise forms.ValidationError(
                (
                    "Não é possível marcar "
                    "um horário que já passou."
                )
            )

        return cleaned_data
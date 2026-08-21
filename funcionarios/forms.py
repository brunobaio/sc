import re

from django import forms

from servicos.models import Servico

from .models import Funcionario


class FuncionarioForm(forms.ModelForm):

    class Meta:
        model = Funcionario

        fields = [
            "nome",
            "cpf",
            "telefone",
            "email",
            "cargo",
            "data_admissao",
            "servicos",
            "ativo",
            "observacao",
        ]

        widgets = {
            "nome": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nome completo",
                }
            ),

            "cpf": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "000.000.000-00",
                    "maxlength": "14",
                }
            ),

            "telefone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "(17) 99999-9999",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "funcionaria@gmail.com",
                }
            ),

            "cargo": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "data_admissao": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "servicos": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "employee-services-checkboxes",
                }
            ),

            "ativo": forms.CheckboxInput(
                attrs={
                    "class": "employee-active-checkbox",
                }
            ),

            "observacao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Informações adicionais",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["servicos"].queryset = (
            Servico.objects
            .filter(ativo=True)
            .order_by("nome")
        )

    def clean_cpf(self):
        cpf_informado = self.cleaned_data.get(
            "cpf",
            "",
        )

        cpf_numeros = re.sub(
            r"\D",
            "",
            cpf_informado,
        )

        if len(cpf_numeros) != 11:
            raise forms.ValidationError(
                "Digite um CPF com 11 números."
            )

        cpf_formatado = (
            f"{cpf_numeros[:3]}."
            f"{cpf_numeros[3:6]}."
            f"{cpf_numeros[6:9]}-"
            f"{cpf_numeros[9:]}"
        )

        cpf_existente = Funcionario.objects.filter(
            cpf=cpf_formatado
        )

        if self.instance.pk:
            cpf_existente = cpf_existente.exclude(
                pk=self.instance.pk
            )

        if cpf_existente.exists():
            raise forms.ValidationError(
                "Este CPF já está cadastrado."
            )

        return cpf_formatado

    def clean_telefone(self):
        telefone_informado = self.cleaned_data.get(
            "telefone",
            "",
        )

        telefone_numeros = re.sub(
            r"\D",
            "",
            telefone_informado,
        )

        if len(telefone_numeros) not in [10, 11]:
            raise forms.ValidationError(
                "Digite um telefone válido com DDD."
            )

        if len(telefone_numeros) == 11:
            return (
                f"({telefone_numeros[:2]}) "
                f"{telefone_numeros[2:7]}-"
                f"{telefone_numeros[7:]}"
            )

        return (
            f"({telefone_numeros[:2]}) "
            f"{telefone_numeros[2:6]}-"
            f"{telefone_numeros[6:]}"
        )
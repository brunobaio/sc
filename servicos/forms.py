from django import forms

from .models import Servico


class ServicoForm(forms.ModelForm):

    class Meta:

        model = Servico

        fields = [
            "nome",
            "descricao",
            "preco",
            "duracao",
            "ativo",
        ]

        widgets = {

            "nome": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nome do serviço",
                }
            ),

            "descricao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descrição do serviço",
                    "rows": 4,
                }
            ),

            "preco": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "0,00",
                }
            ),

            "duracao": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "Duração em minutos",
                }
            ),

            "ativo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }


    def clean_preco(self):

        preco = self.cleaned_data.get("preco")

        if preco is not None and preco < 0:

            raise forms.ValidationError(
                "O preço não pode ser negativo."
            )

        return preco


    def clean_duracao(self):

        duracao = self.cleaned_data.get("duracao")

        if duracao is not None and duracao <= 0:

            raise forms.ValidationError(
                "A duração deve ser maior que zero."
            )

        return duracao
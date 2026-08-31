from django import forms

from .models import Produto


class ProdutoForm(forms.ModelForm):

    class Meta:

        model = Produto

        fields = [
            "nome",
            "descricao",
            "preco",
            "estoque",
            "imagem",
            "ativo",
        ]

        widgets = {

            "nome": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nome do produto",
                }
            ),

            "descricao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descrição do produto",
                    "rows": 4,
                }
            ),

            "preco": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "0,00",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "estoque": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Quantidade em estoque",
                    "min": "0",
                }
            ),

            "imagem": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
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


    def clean_estoque(self):

        estoque = self.cleaned_data.get("estoque")

        if estoque is not None and estoque < 0:

            raise forms.ValidationError(
                "O estoque não pode ser negativo."
            )

        return estoque
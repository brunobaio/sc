from django import forms

from .models import Avaliacao


class AvaliacaoForm(forms.ModelForm):

    class Meta:
        model = Avaliacao

        fields = [
            "nota",
            "comentario",
        ]

        widgets = {

            "nota": forms.RadioSelect(
                choices=[
                    (1, "1"),
                    (2, "2"),
                    (3, "3"),
                    (4, "4"),
                    (5, "5"),
                ]
            ),

            "comentario": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "maxlength": 500,
                    "placeholder": "Conte como foi sua experiência no Bella Rosa...",
                }
            ),
        }
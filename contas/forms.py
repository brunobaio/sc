from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
import re


class CadastroForm(UserCreationForm):

    first_name = forms.CharField(
        label="Nome Completo",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome completo'
        })
    )

    username = forms.CharField(
        label="Nome de Usuário",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite um usuário'
        })
    )

    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu Gmail'
        })
    )

    telefone = forms.CharField(
        label="Telefone",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(17)99999-9999'
        })
    )

    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    password2 = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Usuario
        fields = (
            'first_name',
            'username',
            'email',
            'telefone',
            'password1',
            'password2'
        )

    def clean_email(self):

        email = self.cleaned_data['email'].lower()

        if not email.endswith("@gmail.com"):
            raise forms.ValidationError(
                "Cadastre um endereço Gmail válido."
            )

        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este e-mail já está cadastrado."
            )

        return email

    def clean_telefone(self):

        telefone = self.cleaned_data['telefone']

        telefone = re.sub(r'\D', '', telefone)

        if len(telefone) != 11:
            raise forms.ValidationError(
                "Digite um telefone válido."
            )

        return telefone


class EsqueciSenhaForm(forms.Form):

    username = forms.CharField(
        label="Nome de Usuário",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu usuário'
        })
    )

    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o Gmail cadastrado'
        })
    )

    nova_senha = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a nova senha'
        })
    )

    confirmar_senha = forms.CharField(
        label="Confirmar Nova Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme a nova senha'
        })
    )
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CadastroForm, EsqueciSenhaForm
from .models import Usuario


def cadastro(request):

    if request.user.is_authenticated:
        return redirect("perfil")

    if request.method == "POST":

        form = CadastroForm(request.POST)

        if form.is_valid():

            usuario = form.save()

            login(request, usuario)

            messages.success(
                request,
                "Cadastro realizado com sucesso!"
            )

            return redirect("perfil")

    else:
        form = CadastroForm()

    return render(
        request,
        "contas/cadastro.html",
        {
            "form": form
        }
    )


def login_cliente(request):

    if request.user.is_authenticated:
        return redirect("perfil")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        senha = request.POST.get(
            "password",
            ""
        )

        usuario = authenticate(
            request,
            username=username,
            password=senha
        )

        if usuario is not None:

            login(
                request,
                usuario
            )

            messages.success(
                request,
                "Login realizado com sucesso!"
            )

            return redirect("perfil")

        messages.error(
            request,
            "Usuário ou senha inválidos."
        )

    return render(
        request,
        "contas/login.html"
    )


@login_required(login_url="login")
def logout_cliente(request):

    logout(request)

    return redirect("login")


@login_required(login_url="login")
def perfil(request):

    agendamentos = (
        request.user
        .agendamentos
        .select_related(
            "servico",
            "funcionario",
        )
        .order_by(
            "-data",
            "-horario",
        )
    )

    return render(
        request,
        "contas/perfil.html",
        {
            "agendamentos": agendamentos
        }
    )


def esqueci_senha(request):

    if request.user.is_authenticated:
        return redirect("perfil")

    if request.method == "POST":

        form = EsqueciSenhaForm(
            request.POST
        )

        if form.is_valid():

            username = (
                form.cleaned_data["username"]
                .strip()
            )

            email = (
                form.cleaned_data["email"]
                .strip()
                .lower()
            )

            nova_senha = (
                form.cleaned_data["nova_senha"]
            )

            confirmar_senha = (
                form.cleaned_data["confirmar_senha"]
            )

            if nova_senha != confirmar_senha:

                messages.error(
                    request,
                    "As senhas não coincidem."
                )

            else:

                try:

                    usuario = Usuario.objects.get(
                        username__iexact=username,
                        email__iexact=email
                    )

                except Usuario.DoesNotExist:

                    messages.error(
                        request,
                        "Usuário ou e-mail não encontrados."
                    )

                else:

                    usuario.set_password(
                        nova_senha
                    )

                    usuario.save(
                        update_fields=["password"]
                    )

                    messages.success(
                        request,
                        "Senha alterada com sucesso!"
                    )

                    return redirect("login")

    else:

        form = EsqueciSenhaForm()

    return render(
        request,
        "contas/esqueci_senha.html",
        {
            "form": form
        }
    )
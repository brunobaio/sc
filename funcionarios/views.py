from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from painel.views import usuario_eh_administradora

from .forms import FuncionarioForm
from .models import Funcionario


def verificar_administradora(usuario):
    if not usuario_eh_administradora(usuario):
        raise PermissionDenied(
            "Você não possui permissão para acessar esta página."
        )


@login_required(login_url="login")
def lista_funcionarios(request):

    verificar_administradora(request.user)

    busca = request.GET.get(
        "busca",
        "",
    ).strip()

    situacao = request.GET.get(
        "situacao",
        "ativos",
    )

    funcionarios = (
        Funcionario.objects
        .prefetch_related("servicos")
        .order_by("nome")
    )

    if situacao == "ativos":
        funcionarios = funcionarios.filter(
            ativo=True
        )

    elif situacao == "inativos":
        funcionarios = funcionarios.filter(
            ativo=False
        )

    if busca:
        funcionarios = funcionarios.filter(
            Q(nome__icontains=busca)
            | Q(cpf__icontains=busca)
            | Q(telefone__icontains=busca)
            | Q(email__icontains=busca)
            | Q(cargo__icontains=busca)
        ).distinct()

    contexto = {
        "funcionarios": funcionarios,
        "busca": busca,
        "situacao": situacao,
    }

    return render(
        request,
        "funcionarios/lista.html",
        contexto,
    )


@login_required(login_url="login")
def cadastrar_funcionario(request):

    verificar_administradora(request.user)

    if request.method == "POST":
        form = FuncionarioForm(
            request.POST
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Funcionário cadastrado com sucesso!"
            )

            return redirect(
                "lista_funcionarios"
            )

    else:
        form = FuncionarioForm()

    return render(
        request,
        "funcionarios/formulario.html",
        {
            "form": form,
            "titulo": "Cadastrar funcionário",
            "texto_botao": "Cadastrar funcionário",
        },
    )


@login_required(login_url="login")
def editar_funcionario(
    request,
    funcionario_id,
):

    verificar_administradora(request.user)

    funcionario = get_object_or_404(
        Funcionario,
        id=funcionario_id,
    )

    if request.method == "POST":
        form = FuncionarioForm(
            request.POST,
            instance=funcionario,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Funcionário atualizado com sucesso!"
            )

            return redirect(
                "lista_funcionarios"
            )

    else:
        form = FuncionarioForm(
            instance=funcionario
        )

    return render(
        request,
        "funcionarios/formulario.html",
        {
            "form": form,
            "funcionario": funcionario,
            "titulo": "Editar funcionário",
            "texto_botao": "Salvar alterações",
        },
    )


@login_required(login_url="login")
@require_POST
def alterar_situacao_funcionario(
    request,
    funcionario_id,
):

    verificar_administradora(request.user)

    funcionario = get_object_or_404(
        Funcionario,
        id=funcionario_id,
    )

    funcionario.ativo = not funcionario.ativo

    funcionario.save(
        update_fields=[
            "ativo",
            "atualizado_em",
        ]
    )

    if funcionario.ativo:
        mensagem = (
            "Funcionário ativado com sucesso."
        )
    else:
        mensagem = (
            "Funcionário desativado com sucesso."
        )

    messages.success(
        request,
        mensagem,
    )

    return redirect(
        "lista_funcionarios"
    )
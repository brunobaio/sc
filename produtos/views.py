from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProdutoForm
from .models import Produto


# ==========================================================
# PERMISSÃO DE ADMINISTRADOR
# ==========================================================

def usuario_eh_administradora(usuario):

    return (
        usuario.is_authenticated
        and (
            usuario.is_superuser
            or usuario.is_staff
            or usuario.is_admin_salao
        )
    )


def verificar_permissao_administradora(usuario):

    if not usuario_eh_administradora(usuario):

        raise PermissionDenied(
            "Você não possui permissão para acessar esta página."
        )


# ==========================================================
# VITRINE PÚBLICA
# ==========================================================

def lista_produtos(request):

    produtos = (
        Produto.objects
        .filter(
            ativo=True
        )
        .order_by(
            "nome"
        )
    )

    contexto = {
        "produtos": produtos,
    }

    return render(
        request,
        "produtos/lista_produtos.html",
        contexto,
    )


# ==========================================================
# PAINEL - LISTA DE PRODUTOS
# ==========================================================

@login_required(login_url="login")
def painel_produtos(request):

    verificar_permissao_administradora(
        request.user
    )

    produtos = (
        Produto.objects
        .all()
        .order_by(
            "nome"
        )
    )

    total_produtos = (
        produtos.count()
    )

    total_ativos = (
        produtos
        .filter(
            ativo=True
        )
        .count()
    )

    total_inativos = (
        produtos
        .filter(
            ativo=False
        )
        .count()
    )

    total_sem_estoque = (
        produtos
        .filter(
            estoque=0
        )
        .count()
    )

    contexto = {

        "produtos":
            produtos,

        "total_produtos":
            total_produtos,

        "total_ativos":
            total_ativos,

        "total_inativos":
            total_inativos,

        "total_sem_estoque":
            total_sem_estoque,
    }

    return render(
        request,
        "produtos/painel_produtos.html",
        contexto,
    )


# ==========================================================
# CADASTRAR PRODUTO
# ==========================================================

@login_required(login_url="login")
def cadastrar_produto(request):

    verificar_permissao_administradora(
        request.user
    )

    if request.method == "POST":

        form = ProdutoForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            produto = form.save()

            messages.success(
                request,
                (
                    f'Produto "{produto.nome}" '
                    "cadastrado com sucesso."
                )
            )

            return redirect(
                "painel_produtos"
            )

    else:

        form = ProdutoForm()

    contexto = {
        "form": form,
        "titulo": "Cadastrar Produto",
        "texto_botao": "Cadastrar Produto",
    }

    return render(
        request,
        "produtos/form_produto.html",
        contexto,
    )


# ==========================================================
# EDITAR PRODUTO
# ==========================================================

@login_required(login_url="login")
def editar_produto(
    request,
    produto_id,
):

    verificar_permissao_administradora(
        request.user
    )

    produto = get_object_or_404(
        Produto,
        id=produto_id,
    )

    if request.method == "POST":

        form = ProdutoForm(
            request.POST,
            request.FILES,
            instance=produto,
        )

        if form.is_valid():

            produto = form.save()

            messages.success(
                request,
                (
                    f'Produto "{produto.nome}" '
                    "atualizado com sucesso."
                )
            )

            return redirect(
                "painel_produtos"
            )

    else:

        form = ProdutoForm(
            instance=produto
        )

    contexto = {

        "form":
            form,

        "produto":
            produto,

        "titulo":
            "Editar Produto",

        "texto_botao":
            "Salvar Alterações",
    }

    return render(
        request,
        "produtos/form_produto.html",
        contexto,
    )


# ==========================================================
# ATIVAR / DESATIVAR PRODUTO
# ==========================================================

@login_required(login_url="login")
@require_POST
def alterar_status_produto(
    request,
    produto_id,
):

    verificar_permissao_administradora(
        request.user
    )

    produto = get_object_or_404(
        Produto,
        id=produto_id,
    )

    produto.ativo = not produto.ativo

    produto.save(
        update_fields=[
            "ativo",
            "atualizado_em",
        ]
    )

    if produto.ativo:

        messages.success(
            request,
            (
                f'Produto "{produto.nome}" '
                "ativado com sucesso."
            )
        )

    else:

        messages.success(
            request,
            (
                f'Produto "{produto.nome}" '
                "desativado com sucesso."
            )
        )

    return redirect(
        "painel_produtos"
    )


# ==========================================================
# EXCLUIR PRODUTO
# ==========================================================

@login_required(login_url="login")
@require_POST
def excluir_produto(
    request,
    produto_id,
):

    verificar_permissao_administradora(
        request.user
    )

    produto = get_object_or_404(
        Produto,
        id=produto_id,
    )

    nome_produto = produto.nome

    produto.delete()

    messages.success(
        request,
        (
            f'Produto "{nome_produto}" '
            "excluído com sucesso."
        )
    )

    return redirect(
        "painel_produtos"
    )
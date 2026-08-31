from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import AvaliacaoForm
from .models import Avaliacao


# ==========================================================
# VERIFICAR ADMINISTRADOR
# ==========================================================

def usuario_eh_administrador(usuario):
    return (
        usuario.is_authenticated
        and (
            usuario.is_superuser
            or usuario.is_staff
            or usuario.is_admin_salao
        )
    )


def verificar_permissao_administrador(usuario):
    if not usuario_eh_administrador(usuario):
        raise PermissionDenied(
            "Você não possui permissão para acessar esta página."
        )


# ==========================================================
# LISTA PÚBLICA DE AVALIAÇÕES
# ==========================================================

def lista_avaliacoes(request):

    avaliacoes = (
        Avaliacao.objects
        .filter(aprovado=True)
        .select_related("cliente")
        .order_by("-criado_em")
    )

    contexto = {
        "avaliacoes": avaliacoes,
    }

    return render(
        request,
        "avaliacoes/lista_avaliacoes.html",
        contexto,
    )


# ==========================================================
# CLIENTE CADASTRAR AVALIAÇÃO
# ==========================================================

@login_required(login_url="login")
def cadastrar_avaliacao(request):

    if request.method == "POST":

        form = AvaliacaoForm(
            request.POST
        )

        if form.is_valid():

            avaliacao = form.save(
                commit=False
            )

            avaliacao.cliente = request.user

            avaliacao.aprovado = False

            avaliacao.save()

            messages.success(
                request,
                (
                    "Avaliação enviada com sucesso! "
                    "Ela será publicada após aprovação do salão."
                )
            )

            return redirect(
                "lista_avaliacoes"
            )

    else:

        form = AvaliacaoForm()

    contexto = {
        "form": form,
    }

    return render(
        request,
        "avaliacoes/cadastrar_avaliacao.html",
        contexto,
    )


# ==========================================================
# PAINEL DE AVALIAÇÕES
# ==========================================================

@login_required(login_url="login")
def painel_avaliacoes(request):

    verificar_permissao_administrador(
        request.user
    )

    filtro = request.GET.get(
        "filtro",
        "pendentes"
    )

    avaliacoes = (
        Avaliacao.objects
        .select_related("cliente")
        .all()
        .order_by("-criado_em")
    )


    if filtro == "pendentes":

        avaliacoes = avaliacoes.filter(
            aprovado=False
        )

    elif filtro == "aprovadas":

        avaliacoes = avaliacoes.filter(
            aprovado=True
        )


    total_avaliacoes = Avaliacao.objects.count()

    total_pendentes = (
        Avaliacao.objects
        .filter(
            aprovado=False
        )
        .count()
    )

    total_aprovadas = (
        Avaliacao.objects
        .filter(
            aprovado=True
        )
        .count()
    )


    contexto = {

        "avaliacoes": avaliacoes,

        "filtro": filtro,

        "total_avaliacoes":
            total_avaliacoes,

        "total_pendentes":
            total_pendentes,

        "total_aprovadas":
            total_aprovadas,
    }


    return render(
        request,
        "avaliacoes/painel_avaliacoes.html",
        contexto,
    )


# ==========================================================
# APROVAR AVALIAÇÃO
# ==========================================================

@login_required(login_url="login")
@require_POST
def aprovar_avaliacao(
    request,
    avaliacao_id,
):

    verificar_permissao_administrador(
        request.user
    )

    avaliacao = get_object_or_404(
        Avaliacao,
        id=avaliacao_id,
    )

    avaliacao.aprovado = True

    avaliacao.save()

    messages.success(
        request,
        "Avaliação aprovada com sucesso."
    )

    return redirect(
        "painel_avaliacoes"
    )


# ==========================================================
# DESAPROVAR AVALIAÇÃO
# ==========================================================

@login_required(login_url="login")
@require_POST
def desaprovar_avaliacao(
    request,
    avaliacao_id,
):

    verificar_permissao_administrador(
        request.user
    )

    avaliacao = get_object_or_404(
        Avaliacao,
        id=avaliacao_id,
    )

    avaliacao.aprovado = False

    avaliacao.save()

    messages.success(
        request,
        "Avaliação retirada da publicação."
    )

    return redirect(
        "painel_avaliacoes"
    )


# ==========================================================
# EXCLUIR AVALIAÇÃO
# ==========================================================

@login_required(login_url="login")
@require_POST
def excluir_avaliacao(
    request,
    avaliacao_id,
):

    verificar_permissao_administrador(
        request.user
    )

    avaliacao = get_object_or_404(
        Avaliacao,
        id=avaliacao_id,
    )

    avaliacao.delete()

    messages.success(
        request,
        "Avaliação excluída com sucesso."
    )

    return redirect(
        "painel_avaliacoes"
    )
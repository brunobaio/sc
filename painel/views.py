from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.views.decorators.http import require_POST

from agendamentos.models import Agendamento
from contas.models import Usuario
from financeiro.models import Receita
from servicos.models import Servico


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


@login_required(login_url="login")
def dashboard(request):

    verificar_permissao_administradora(
        request.user
    )

    hoje = date.today()

    agendamentos_hoje = (
        Agendamento.objects
        .filter(
            data=hoje
        )
        .select_related(
            "cliente",
            "servico",
            "funcionario",
        )
        .order_by(
            "horario"
        )
    )

    proximos_agendamentos = (
        Agendamento.objects
        .filter(
            data__gte=hoje,
            status__in=[
                Agendamento.STATUS_PENDENTE,
                Agendamento.STATUS_CONFIRMADO,
            ],
        )
        .select_related(
            "cliente",
            "servico",
            "funcionario",
        )
        .order_by(
            "data",
            "horario",
        )[:10]
    )

    total_clientes = (
        Usuario.objects
        .filter(
            is_superuser=False,
            is_admin_salao=False,
        )
        .count()
    )

    total_servicos = (
        Servico.objects
        .filter(
            ativo=True
        )
        .count()
    )

    total_agendamentos_hoje = (
        agendamentos_hoje.count()
    )

    total_pendentes = (
        agendamentos_hoje
        .filter(
            status=Agendamento.STATUS_PENDENTE
        )
        .count()
    )

    total_confirmados = (
        agendamentos_hoje
        .filter(
            status=Agendamento.STATUS_CONFIRMADO
        )
        .count()
    )

    total_concluidos = (
        agendamentos_hoje
        .filter(
            status=Agendamento.STATUS_CONCLUIDO
        )
        .count()
    )

    contexto = {
        "hoje": hoje,
        "agendamentos_hoje": agendamentos_hoje,
        "proximos_agendamentos": proximos_agendamentos,
        "total_clientes": total_clientes,
        "total_servicos": total_servicos,
        "total_agendamentos_hoje": total_agendamentos_hoje,
        "total_pendentes": total_pendentes,
        "total_confirmados": total_confirmados,
        "total_concluidos": total_concluidos,
    }

    return render(
        request,
        "painel/dashboard.html",
        contexto,
    )


@login_required(login_url="login")
def lista_agendamentos(request):

    verificar_permissao_administradora(
        request.user
    )

    filtro = request.GET.get(
        "filtro",
        "ativos"
    )

    data_selecionada = request.GET.get(
        "data",
        ""
    )

    busca = request.GET.get(
        "busca",
        ""
    ).strip()

    agendamentos = (
        Agendamento.objects
        .select_related(
            "cliente",
            "servico",
            "funcionario",
        )
        .order_by(
            "data",
            "horario",
        )
    )

    if filtro == "ativos":

        agendamentos = agendamentos.filter(
            status__in=[
                Agendamento.STATUS_PENDENTE,
                Agendamento.STATUS_CONFIRMADO,
            ]
        )

    elif filtro == "pendentes":

        agendamentos = agendamentos.filter(
            status=Agendamento.STATUS_PENDENTE
        )

    elif filtro == "confirmados":

        agendamentos = agendamentos.filter(
            status=Agendamento.STATUS_CONFIRMADO
        )

    elif filtro == "concluidos":

        agendamentos = agendamentos.filter(
            status=Agendamento.STATUS_CONCLUIDO
        )

    elif filtro == "cancelados":

        agendamentos = agendamentos.filter(
            status__in=[
                Agendamento.STATUS_CANCELADO_CLIENTE,
                Agendamento.STATUS_CANCELADO_ADMIN,
                Agendamento.STATUS_DESISTENCIA,
                Agendamento.STATUS_NAO_COMPARECEU,
            ]
        )

    elif filtro == "hoje":

        agendamentos = agendamentos.filter(
            data=date.today()
        )

    if data_selecionada:

        agendamentos = agendamentos.filter(
            data=data_selecionada
        )

    if busca:

        agendamentos = agendamentos.filter(
            Q(
                cliente__first_name__icontains=busca
            )
            | Q(
                cliente__username__icontains=busca
            )
            | Q(
                cliente__email__icontains=busca
            )
            | Q(
                servico__nome__icontains=busca
            )
            | Q(
                funcionario__nome__icontains=busca
            )
        )

    contexto = {
        "agendamentos": agendamentos,
        "filtro": filtro,
        "data_selecionada": data_selecionada,
        "busca": busca,
    }

    return render(
        request,
        "painel/agendamentos.html",
        contexto,
    )


@login_required(login_url="login")
@require_POST
def alterar_status_agendamento(
    request,
    agendamento_id,
):

    verificar_permissao_administradora(
        request.user
    )

    agendamento = get_object_or_404(
        Agendamento,
        id=agendamento_id,
    )

    novo_status = request.POST.get(
        "status",
        ""
    )

    motivo = request.POST.get(
        "motivo_status",
        ""
    ).strip()

    status_validos = {
        valor
        for valor, nome
        in Agendamento.STATUS_CHOICES
    }

    if novo_status not in status_validos:

        messages.error(
            request,
            "Status inválido."
        )

        return redirect(
            "painel_agendamentos"
        )

    agendamento.status = novo_status

    if motivo:

        agendamento.motivo_status = motivo

    else:

        agendamento.motivo_status = (
            mensagem_padrao_status(
                novo_status
            )
        )

    agendamento.save(
        update_fields=[
            "status",
            "motivo_status",
            "atualizado_em",
        ]
    )

    # ==========================================
    # CRIAÇÃO AUTOMÁTICA DA RECEITA
    # ==========================================

    if (
        novo_status
        == Agendamento.STATUS_CONCLUIDO
    ):

        receita, criada = (
            Receita.objects.get_or_create(
                agendamento=agendamento,
                defaults={
                    "valor": agendamento.servico.preco,
                    "pago": False,
                },
            )
        )

        if criada:

            messages.success(
                request,
                (
                    "Atendimento concluído e receita "
                    "registrada automaticamente."
                )
            )

        else:

            messages.success(
                request,
                (
                    "Atendimento concluído. "
                    "A receita já estava registrada."
                )
            )

    else:

        messages.success(
            request,
            (
                "Agendamento atualizado para "
                f"{agendamento.get_status_display()}."
            )
        )

    return redirect(
        "painel_agendamentos"
    )


def mensagem_padrao_status(status):

    mensagens = {

        Agendamento.STATUS_PENDENTE:
            "Agendamento definido como pendente.",

        Agendamento.STATUS_CONFIRMADO:
            "Agendamento confirmado pela administradora.",

        Agendamento.STATUS_CANCELADO_CLIENTE:
            "Agendamento cancelado pela cliente.",

        Agendamento.STATUS_CANCELADO_ADMIN:
            "Agendamento cancelado pelo salão.",

        Agendamento.STATUS_DESISTENCIA:
            (
                "Cliente informou que não poderá "
                "comparecer ao atendimento."
            ),

        Agendamento.STATUS_NAO_COMPARECEU:
            (
                "Cliente não compareceu "
                "ao horário marcado."
            ),

        Agendamento.STATUS_CONCLUIDO:
            "Atendimento realizado e concluído.",
    }

    return mensagens.get(
        status,
        ""
    )
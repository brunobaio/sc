from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from agendamentos.models import Agendamento
from contas.models import Usuario
from financeiro.models import Receita
from funcionarios.models import Funcionario
from servicos.models import Servico


# ==========================================================
# PERMISSÕES
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
# DASHBOARD
# ==========================================================

@login_required(login_url="login")
def dashboard(request):

    verificar_permissao_administradora(request.user)

    hoje = date.today()

    # ------------------------------------------------------
    # AGENDAMENTOS DE HOJE
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # PRÓXIMOS AGENDAMENTOS
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # CLIENTES
    # ------------------------------------------------------

    total_clientes = (
        Usuario.objects
        .filter(
            is_superuser=False,
            is_admin_salao=False,
        )
        .count()
    )

    # ------------------------------------------------------
    # SERVIÇOS
    # ------------------------------------------------------

    total_servicos = (
        Servico.objects
        .filter(
            ativo=True
        )
        .count()
    )

    # ------------------------------------------------------
    # TOTAIS DE HOJE
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # AGENDAMENTOS DO MÊS
    # ------------------------------------------------------

    agendamentos_mes = (
        Agendamento.objects
        .filter(
            data__year=hoje.year,
            data__month=hoje.month,
        )
    )

    total_agendamentos_mes = (
        agendamentos_mes.count()
    )

    total_concluidos_mes = (
        agendamentos_mes
        .filter(
            status=Agendamento.STATUS_CONCLUIDO
        )
        .count()
    )

    total_cancelados_mes = (
        agendamentos_mes
        .filter(
            status__in=[
                Agendamento.STATUS_CANCELADO_CLIENTE,
                Agendamento.STATUS_CANCELADO_ADMIN,
                Agendamento.STATUS_DESISTENCIA,
            ]
        )
        .count()
    )

    total_faltas_mes = (
        agendamentos_mes
        .filter(
            status=Agendamento.STATUS_NAO_COMPARECEU
        )
        .count()
    )

    # ------------------------------------------------------
    # SERVIÇO MAIS REALIZADO
    # ------------------------------------------------------

    servico_mais_realizado = (
        agendamentos_mes
        .filter(
            status=Agendamento.STATUS_CONCLUIDO
        )
        .values(
            "servico__nome"
        )
        .annotate(
            total=Count("id")
        )
        .order_by(
            "-total"
        )
        .first()
    )

    if servico_mais_realizado:

        nome_servico_mais_realizado = (
            servico_mais_realizado["servico__nome"]
        )

        total_servico_mais_realizado = (
            servico_mais_realizado["total"]
        )

    else:

        nome_servico_mais_realizado = "Sem dados"
        total_servico_mais_realizado = 0

    # ------------------------------------------------------
    # PROFISSIONAL DESTAQUE
    # ------------------------------------------------------

    profissional_destaque = (
        agendamentos_mes
        .filter(
            status=Agendamento.STATUS_CONCLUIDO,
            funcionario__isnull=False,
        )
        .values(
            "funcionario__nome"
        )
        .annotate(
            total=Count("id")
        )
        .order_by(
            "-total"
        )
        .first()
    )

    if profissional_destaque:

        nome_profissional_destaque = (
            profissional_destaque["funcionario__nome"]
        )

        total_profissional_destaque = (
            profissional_destaque["total"]
        )

    else:

        nome_profissional_destaque = "Sem dados"
        total_profissional_destaque = 0

    # ------------------------------------------------------
    # FATURAMENTO DO MÊS
    # ------------------------------------------------------

    faturamento_mes = (
        Receita.objects
        .filter(
            pago=True,
            data_pagamento__year=hoje.year,
            data_pagamento__month=hoje.month,
        )
        .aggregate(
            total=Sum("valor")
        )["total"]
        or 0
    )

    # ------------------------------------------------------
    # CONTEXTO
    # ------------------------------------------------------

    contexto = {

        "hoje":
            hoje,

        "agendamentos_hoje":
            agendamentos_hoje,

        "proximos_agendamentos":
            proximos_agendamentos,

        "total_clientes":
            total_clientes,

        "total_servicos":
            total_servicos,

        "total_agendamentos_hoje":
            total_agendamentos_hoje,

        "total_pendentes":
            total_pendentes,

        "total_confirmados":
            total_confirmados,

        "total_concluidos":
            total_concluidos,

        "total_agendamentos_mes":
            total_agendamentos_mes,

        "total_concluidos_mes":
            total_concluidos_mes,

        "total_cancelados_mes":
            total_cancelados_mes,

        "total_faltas_mes":
            total_faltas_mes,

        "nome_servico_mais_realizado":
            nome_servico_mais_realizado,

        "total_servico_mais_realizado":
            total_servico_mais_realizado,

        "nome_profissional_destaque":
            nome_profissional_destaque,

        "total_profissional_destaque":
            total_profissional_destaque,

        "faturamento_mes":
            faturamento_mes,
    }

    return render(
        request,
        "painel/dashboard.html",
        contexto,
    )


# ==========================================================
# LISTA DE AGENDAMENTOS
# ==========================================================

@login_required(login_url="login")
def lista_agendamentos(request):

    verificar_permissao_administradora(request.user)

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

    # ------------------------------------------------------
    # FILTROS
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # DATA
    # ------------------------------------------------------

    if data_selecionada:

        agendamentos = agendamentos.filter(
            data=data_selecionada
        )

    # ------------------------------------------------------
    # PESQUISA
    # ------------------------------------------------------

    if busca:

        agendamentos = agendamentos.filter(

            Q(
                cliente__first_name__icontains=busca
            )

            |

            Q(
                cliente__username__icontains=busca
            )

            |

            Q(
                cliente__email__icontains=busca
            )

            |

            Q(
                servico__nome__icontains=busca
            )

            |

            Q(
                funcionario__nome__icontains=busca
            )
        )

    # ------------------------------------------------------
    # CONTEXTO
    # ------------------------------------------------------

    contexto = {

        "agendamentos":
            agendamentos,

        "filtro":
            filtro,

        "data_selecionada":
            data_selecionada,

        "busca":
            busca,
    }

    return render(
        request,
        "painel/agendamentos.html",
        contexto,
    )


# ==========================================================
# ALTERAR STATUS DO AGENDAMENTO
# ==========================================================

@login_required(login_url="login")
@require_POST
def alterar_status_agendamento(
    request,
    agendamento_id,
):

    verificar_permissao_administradora(request.user)

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

    agendamento.save()

    # ------------------------------------------------------
    # GERAR RECEITA AUTOMATICAMENTE
    # ------------------------------------------------------

    if novo_status == Agendamento.STATUS_CONCLUIDO:

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


# ==========================================================
# MENSAGENS DE STATUS
# ==========================================================

def mensagem_padrao_status(status):

    mensagens = {

        Agendamento.STATUS_PENDENTE:
            "Agendamento definido como pendente.",

        Agendamento.STATUS_CONFIRMADO:
            "Agendamento confirmado pelo salão.",

        Agendamento.STATUS_CANCELADO_CLIENTE:
            "Agendamento cancelado pela cliente.",

        Agendamento.STATUS_CANCELADO_ADMIN:
            "Agendamento cancelado pelo salão.",

        Agendamento.STATUS_DESISTENCIA:
            "Cliente informou desistência do atendimento.",

        Agendamento.STATUS_NAO_COMPARECEU:
            "Cliente não compareceu ao horário marcado.",

        Agendamento.STATUS_CONCLUIDO:
            "Atendimento realizado e concluído.",
    }

    return mensagens.get(
        status,
        ""
    )


# ==========================================================
# RELATÓRIO DE ATENDIMENTOS
# ==========================================================

@login_required(login_url="login")
def relatorio_atendimentos(request):

    verificar_permissao_administradora(request.user)

    # ------------------------------------------------------
    # PEGAR FILTROS
    # ------------------------------------------------------

    data_inicial = request.GET.get(
        "data_inicial",
        ""
    )

    data_final = request.GET.get(
        "data_final",
        ""
    )

    funcionario_id = request.GET.get(
        "funcionario",
        ""
    )

    servico_id = request.GET.get(
        "servico",
        ""
    )

    status = request.GET.get(
        "status",
        ""
    )

    # ------------------------------------------------------
    # QUERY INICIAL
    # ------------------------------------------------------

    agendamentos = (
        Agendamento.objects
        .select_related(
            "cliente",
            "servico",
            "funcionario",
        )
        .all()
    )

    # ------------------------------------------------------
    # FILTRO DATA INICIAL
    # ------------------------------------------------------

    if data_inicial:

        agendamentos = agendamentos.filter(
            data__gte=data_inicial
        )

    # ------------------------------------------------------
    # FILTRO DATA FINAL
    # ------------------------------------------------------

    if data_final:

        agendamentos = agendamentos.filter(
            data__lte=data_final
        )

    # ------------------------------------------------------
    # FILTRO PROFISSIONAL
    # ------------------------------------------------------

    if funcionario_id:

        agendamentos = agendamentos.filter(
            funcionario_id=funcionario_id
        )

    # ------------------------------------------------------
    # FILTRO SERVIÇO
    # ------------------------------------------------------

    if servico_id:

        agendamentos = agendamentos.filter(
            servico_id=servico_id
        )

    # ------------------------------------------------------
    # FILTRO STATUS
    # ------------------------------------------------------

    if status:

        agendamentos = agendamentos.filter(
            status=status
        )

    # ------------------------------------------------------
    # ORDENAR
    # ------------------------------------------------------

    agendamentos = agendamentos.order_by(
        "-data",
        "-horario",
    )

    # ======================================================
    # INDICADORES
    # ======================================================

    total_agendamentos = (
        agendamentos.count()
    )

    total_concluidos = (
        agendamentos
        .filter(
            status=Agendamento.STATUS_CONCLUIDO
        )
        .count()
    )

    total_pendentes = (
        agendamentos
        .filter(
            status=Agendamento.STATUS_PENDENTE
        )
        .count()
    )

    total_confirmados = (
        agendamentos
        .filter(
            status=Agendamento.STATUS_CONFIRMADO
        )
        .count()
    )

    total_cancelados = (
        agendamentos
        .filter(
            status__in=[
                Agendamento.STATUS_CANCELADO_CLIENTE,
                Agendamento.STATUS_CANCELADO_ADMIN,
                Agendamento.STATUS_DESISTENCIA,
            ]
        )
        .count()
    )

    total_nao_compareceu = (
        agendamentos
        .filter(
            status=Agendamento.STATUS_NAO_COMPARECEU
        )
        .count()
    )

    # ======================================================
    # FATURAMENTO DO PERÍODO
    # ======================================================

    faturamento = (
        Receita.objects
        .filter(
            agendamento__in=agendamentos,
            pago=True,
        )
        .aggregate(
            total=Sum("valor")
        )["total"]
        or 0
    )

    # ======================================================
    # SERVIÇO MAIS REALIZADO
    # ======================================================

    servico_destaque = (
        agendamentos
        .filter(
            status=Agendamento.STATUS_CONCLUIDO
        )
        .values(
            "servico__nome"
        )
        .annotate(
            total=Count("id")
        )
        .order_by(
            "-total"
        )
        .first()
    )

    if servico_destaque:

        nome_servico_destaque = (
            servico_destaque["servico__nome"]
        )

        quantidade_servico_destaque = (
            servico_destaque["total"]
        )

    else:

        nome_servico_destaque = "Sem dados"
        quantidade_servico_destaque = 0

    # ======================================================
    # PROFISSIONAL DESTAQUE
    # ======================================================

    profissional_destaque = (
        agendamentos
        .filter(
            status=Agendamento.STATUS_CONCLUIDO,
            funcionario__isnull=False,
        )
        .values(
            "funcionario__nome"
        )
        .annotate(
            total=Count("id")
        )
        .order_by(
            "-total"
        )
        .first()
    )

    if profissional_destaque:

        nome_profissional_destaque = (
            profissional_destaque[
                "funcionario__nome"
            ]
        )

        quantidade_profissional_destaque = (
            profissional_destaque[
                "total"
            ]
        )

    else:

        nome_profissional_destaque = "Sem dados"
        quantidade_profissional_destaque = 0

    # ======================================================
    # DADOS PARA SELECTS
    # ======================================================

    funcionarios = (
        Funcionario.objects
        .filter(
            ativo=True
        )
        .order_by(
            "nome"
        )
    )

    servicos = (
        Servico.objects
        .filter(
            ativo=True
        )
        .order_by(
            "nome"
        )
    )

    # ======================================================
    # CONTEXTO
    # ======================================================

    contexto = {

        "agendamentos":
            agendamentos,

        "funcionarios":
            funcionarios,

        "servicos":
            servicos,

        "status_choices":
            Agendamento.STATUS_CHOICES,

        "data_inicial":
            data_inicial,

        "data_final":
            data_final,

        "funcionario_selecionado":
            funcionario_id,

        "servico_selecionado":
            servico_id,

        "status_selecionado":
            status,

        "total_agendamentos":
            total_agendamentos,

        "total_concluidos":
            total_concluidos,

        "total_pendentes":
            total_pendentes,

        "total_confirmados":
            total_confirmados,

        "total_cancelados":
            total_cancelados,

        "total_nao_compareceu":
            total_nao_compareceu,

        "faturamento":
            faturamento,

        "nome_servico_destaque":
            nome_servico_destaque,

        "quantidade_servico_destaque":
            quantidade_servico_destaque,

        "nome_profissional_destaque":
            nome_profissional_destaque,

        "quantidade_profissional_destaque":
            quantidade_profissional_destaque,
    }

    return render(
        request,
        "painel/relatorios.html",
        contexto,
    )
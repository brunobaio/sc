from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from funcionarios.models import Funcionario

from .models import Receita


def verificar_administrador(usuario):

    if not (
        usuario.is_authenticated
        and (
            usuario.is_superuser
            or usuario.is_staff
            or usuario.is_admin_salao
        )
    ):
        raise PermissionDenied(
            "Você não possui permissão para acessar o financeiro."
        )


@login_required(login_url="login")
def dashboard_financeiro(request):

    verificar_administrador(request.user)

    hoje = date.today()

    receitas_base = (
        Receita.objects
        .select_related(
            "agendamento",
            "agendamento__cliente",
            "agendamento__servico",
            "agendamento__funcionario",
        )
        .order_by("-criado_em")
    )

    # ==========================================
    # FILTROS
    # ==========================================

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

    forma_pagamento = request.GET.get(
        "forma_pagamento",
        ""
    )

    status_pagamento = request.GET.get(
        "status",
        ""
    )

    receitas = receitas_base

    if data_inicial:
        receitas = receitas.filter(
            agendamento__data__gte=data_inicial
        )

    if data_final:
        receitas = receitas.filter(
            agendamento__data__lte=data_final
        )

    if funcionario_id:
        receitas = receitas.filter(
            agendamento__funcionario_id=funcionario_id
        )

    if forma_pagamento:
        receitas = receitas.filter(
            forma_pagamento=forma_pagamento
        )

    if status_pagamento == "pago":
        receitas = receitas.filter(
            pago=True
        )

    elif status_pagamento == "pendente":
        receitas = receitas.filter(
            pago=False
        )

    # ==========================================
    # RESUMO
    # ==========================================

    faturamento_filtrado = (
        receitas
        .filter(pago=True)
        .aggregate(
            total=Sum("valor")
        )["total"]
        or 0
    )

    total_pendente = (
        receitas
        .filter(pago=False)
        .aggregate(
            total=Sum("valor")
        )["total"]
        or 0
    )

    quantidade_receitas = receitas.count()

    quantidade_pagas = (
        receitas
        .filter(pago=True)
        .count()
    )

    quantidade_pendentes = (
        receitas
        .filter(pago=False)
        .count()
    )

    # ==========================================
    # FATURAMENTO DE HOJE
    # ==========================================

    faturamento_hoje = (
        Receita.objects
        .filter(
            pago=True,
            data_pagamento=hoje,
        )
        .aggregate(
            total=Sum("valor")
        )["total"]
        or 0
    )

    # ==========================================
    # FATURAMENTO DO MÊS
    # ==========================================

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

    # ==========================================
    # GRÁFICO - FATURAMENTO POR MÊS
    # ==========================================

    faturamento_por_mes = (
        Receita.objects
        .filter(
            pago=True,
            data_pagamento__isnull=False,
        )
        .annotate(
            mes=TruncMonth("data_pagamento")
        )
        .values("mes")
        .annotate(
            total=Sum("valor")
        )
        .order_by("mes")
    )

    meses_labels = []

    meses_valores = []

    nomes_meses = {
        1: "Jan",
        2: "Fev",
        3: "Mar",
        4: "Abr",
        5: "Mai",
        6: "Jun",
        7: "Jul",
        8: "Ago",
        9: "Set",
        10: "Out",
        11: "Nov",
        12: "Dez",
    }

    for item in faturamento_por_mes:

        mes = item["mes"]

        if mes:

            meses_labels.append(
                f"{nomes_meses[mes.month]}/{mes.year}"
            )

            meses_valores.append(
                float(item["total"])
            )

    # ==========================================
    # GRÁFICO - FATURAMENTO POR PROFISSIONAL
    # ==========================================

    faturamento_por_profissional = (
        Receita.objects
        .filter(
            pago=True,
            agendamento__funcionario__isnull=False,
        )
        .values(
            "agendamento__funcionario__nome"
        )
        .annotate(
            total=Sum("valor")
        )
        .order_by("-total")
    )

    profissionais_labels = []

    profissionais_valores = []

    for item in faturamento_por_profissional:

        profissionais_labels.append(
            item["agendamento__funcionario__nome"]
        )

        profissionais_valores.append(
            float(item["total"])
        )

    # ==========================================
    # SELECT DE PROFISSIONAIS
    # ==========================================

    funcionarios = (
        Funcionario.objects
        .filter(
            ativo=True
        )
        .order_by("nome")
    )

    contexto = {

        # Totais
        "faturamento_hoje": faturamento_hoje,
        "faturamento_mes": faturamento_mes,
        "faturamento_filtrado": faturamento_filtrado,
        "total_pendente": total_pendente,

        # Quantidades
        "quantidade_receitas": quantidade_receitas,
        "quantidade_pagas": quantidade_pagas,
        "quantidade_pendentes": quantidade_pendentes,

        # Receitas
        "ultimas_receitas": receitas[:100],

        # Selects
        "funcionarios": funcionarios,
        "formas_pagamento": Receita.FORMAS_PAGAMENTO,

        # Filtros
        "data_inicial": data_inicial,
        "data_final": data_final,
        "funcionario_selecionado": funcionario_id,
        "forma_pagamento_selecionada": forma_pagamento,
        "status_selecionado": status_pagamento,

        # Gráfico mensal
        "meses_labels": meses_labels,
        "meses_valores": meses_valores,

        # Gráfico profissionais
        "profissionais_labels": profissionais_labels,
        "profissionais_valores": profissionais_valores,
    }

    return render(
        request,
        "financeiro/dashboard.html",
        contexto,
    )


@login_required(login_url="login")
@require_POST
def registrar_pagamento(
    request,
    receita_id,
):

    verificar_administrador(request.user)

    receita = get_object_or_404(
        Receita,
        id=receita_id,
    )

    forma_pagamento = request.POST.get(
        "forma_pagamento",
        ""
    )

    formas_validas = {
        valor
        for valor, nome
        in Receita.FORMAS_PAGAMENTO
    }

    if forma_pagamento not in formas_validas:

        messages.error(
            request,
            "Selecione uma forma de pagamento válida."
        )

        return redirect(
            "financeiro_dashboard"
        )

    receita.forma_pagamento = forma_pagamento

    receita.pago = True

    receita.data_pagamento = (
        timezone.localdate()
    )

    receita.save(
        update_fields=[
            "forma_pagamento",
            "pago",
            "data_pagamento",
            "atualizado_em",
        ]
    )

    messages.success(
        request,
        "Pagamento registrado com sucesso."
    )

    return redirect(
        "financeiro_dashboard"
    )


@login_required(login_url="login")
@require_POST
def marcar_como_pendente(
    request,
    receita_id,
):

    verificar_administrador(request.user)

    receita = get_object_or_404(
        Receita,
        id=receita_id,
    )

    receita.pago = False

    receita.data_pagamento = None

    receita.forma_pagamento = ""

    receita.save(
        update_fields=[
            "pago",
            "data_pagamento",
            "forma_pagamento",
            "atualizado_em",
        ]
    )

    messages.success(
        request,
        "Pagamento marcado como pendente."
    )

    return redirect(
        "financeiro_dashboard"
    )
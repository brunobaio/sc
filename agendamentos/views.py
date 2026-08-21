from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from funcionarios.models import Funcionario
from painel.models import DataBloqueada, HorarioFuncionamento
from servicos.models import Servico

from .forms import AgendamentoForm
from .models import Agendamento


INTERVALO_MINUTOS = 30


def buscar_configuracao_dia(data):
    return HorarioFuncionamento.objects.filter(
        dia_semana=data.weekday()
    ).first()


def buscar_bloqueio_data(data):
    return DataBloqueada.objects.filter(
        data=data
    ).first()


def buscar_horarios_disponiveis(
    data,
    servico,
    funcionario,
):
    configuracao_dia = buscar_configuracao_dia(data)

    if configuracao_dia is None:
        return []

    if not configuracao_dia.aberto:
        return []

    if (
        configuracao_dia.hora_abertura is None
        or configuracao_dia.hora_fechamento is None
    ):
        return []

    bloqueio = buscar_bloqueio_data(data)

    if bloqueio and bloqueio.dia_inteiro:
        return []

    abertura = datetime.combine(
        data,
        configuracao_dia.hora_abertura,
    )

    fechamento = datetime.combine(
        data,
        configuracao_dia.hora_fechamento,
    )

    duracao_novo_servico = timedelta(
        minutes=servico.duracao
    )

    agendamentos_existentes = (
        Agendamento.objects
        .filter(
            data=data,
            funcionario=funcionario,
            status__in=[
                Agendamento.STATUS_PENDENTE,
                Agendamento.STATUS_CONFIRMADO,
            ],
        )
        .select_related("servico")
        .order_by("horario")
    )

    periodos_ocupados = []

    for agendamento_existente in agendamentos_existentes:
        inicio_existente = datetime.combine(
            data,
            agendamento_existente.horario,
        )

        fim_existente = inicio_existente + timedelta(
            minutes=agendamento_existente.servico.duracao
        )

        periodos_ocupados.append(
            (
                inicio_existente,
                fim_existente,
            )
        )

    if (
        bloqueio
        and not bloqueio.dia_inteiro
        and bloqueio.hora_inicio
        and bloqueio.hora_fim
    ):
        inicio_bloqueio = datetime.combine(
            data,
            bloqueio.hora_inicio,
        )

        fim_bloqueio = datetime.combine(
            data,
            bloqueio.hora_fim,
        )

        periodos_ocupados.append(
            (
                inicio_bloqueio,
                fim_bloqueio,
            )
        )

    horarios_disponiveis = []

    horario_atual = abertura

    agora = timezone.localtime()

    while horario_atual < fechamento:
        fim_novo_agendamento = (
            horario_atual + duracao_novo_servico
        )

        cabe_no_expediente = (
            fim_novo_agendamento <= fechamento
        )

        horario_ja_passou = False

        if data == agora.date():
            horario_com_fuso = timezone.make_aware(
                horario_atual,
                timezone.get_current_timezone(),
            )

            horario_ja_passou = (
                horario_com_fuso <= agora
            )

        existe_conflito = False

        for inicio_ocupado, fim_ocupado in periodos_ocupados:
            if (
                horario_atual < fim_ocupado
                and fim_novo_agendamento > inicio_ocupado
            ):
                existe_conflito = True
                break

        if (
            cabe_no_expediente
            and not horario_ja_passou
            and not existe_conflito
        ):
            horarios_disponiveis.append(
                horario_atual.strftime("%H:%M")
            )

        horario_atual += timedelta(
            minutes=INTERVALO_MINUTOS
        )

    return horarios_disponiveis


@login_required(login_url="login")
def funcionarios_disponiveis(request):
    servico_id = request.GET.get("servico")

    if not servico_id:
        return JsonResponse(
            {
                "funcionarios": [],
            }
        )

    funcionarios = (
        Funcionario.objects
        .filter(
            ativo=True,
            servicos__id=servico_id,
        )
        .distinct()
        .order_by("nome")
    )

    dados = [
        {
            "id": funcionario.id,
            "nome": funcionario.nome,
        }
        for funcionario in funcionarios
    ]

    return JsonResponse(
        {
            "funcionarios": dados,
        }
    )


@login_required(login_url="login")
def datas_indisponiveis(request):
    datas_bloqueadas = list(
        DataBloqueada.objects.filter(
            dia_inteiro=True
        ).values_list(
            "data",
            flat=True,
        )
    )

    datas_formatadas = [
        data.strftime("%Y-%m-%d")
        for data in datas_bloqueadas
    ]

    dias_semana_fechados = list(
        HorarioFuncionamento.objects.filter(
            aberto=False
        ).values_list(
            "dia_semana",
            flat=True,
        )
    )

    return JsonResponse(
        {
            "datas_bloqueadas": datas_formatadas,
            "dias_semana_fechados": dias_semana_fechados,
        }
    )


@login_required(login_url="login")
def horarios_disponiveis(request):
    servico_id = request.GET.get("servico")
    funcionario_id = request.GET.get("funcionario")
    data_texto = request.GET.get("data")

    if (
        not servico_id
        or not funcionario_id
        or not data_texto
    ):
        return JsonResponse(
            {
                "horarios": [],
                "erro": (
                    "Informe o serviço, "
                    "o profissional e a data."
                ),
            },
            status=400,
        )

    try:
        data = datetime.strptime(
            data_texto,
            "%Y-%m-%d",
        ).date()

    except ValueError:
        return JsonResponse(
            {
                "horarios": [],
                "erro": "Data inválida.",
            },
            status=400,
        )

    if data < timezone.localdate():
        return JsonResponse(
            {
                "horarios": [],
                "erro": (
                    "Não é permitido selecionar "
                    "uma data anterior."
                ),
            },
            status=400,
        )

    servico = get_object_or_404(
        Servico,
        id=servico_id,
        ativo=True,
    )

    funcionario = get_object_or_404(
        Funcionario,
        id=funcionario_id,
        ativo=True,
    )

    if not funcionario.servicos.filter(
        id=servico.id
    ).exists():
        return JsonResponse(
            {
                "horarios": [],
                "erro": (
                    "Esse profissional não realiza "
                    "o serviço selecionado."
                ),
            },
            status=400,
        )

    configuracao_dia = buscar_configuracao_dia(data)
    bloqueio = buscar_bloqueio_data(data)

    if configuracao_dia is None:
        return JsonResponse(
            {
                "horarios": [],
                "duracao": servico.duracao,
                "erro": (
                    "Esse dia ainda não foi configurado."
                ),
            }
        )

    if not configuracao_dia.aberto:
        return JsonResponse(
            {
                "horarios": [],
                "duracao": servico.duracao,
                "erro": (
                    "O salão não funciona nesse dia."
                ),
            }
        )

    if bloqueio and bloqueio.dia_inteiro:
        mensagem = (
            "Esta data está indisponível."
        )

        if bloqueio.motivo:
            mensagem = (
                f"Esta data está indisponível: "
                f"{bloqueio.motivo}."
            )

        return JsonResponse(
            {
                "horarios": [],
                "duracao": servico.duracao,
                "erro": mensagem,
            }
        )

    horarios = buscar_horarios_disponiveis(
        data,
        servico,
        funcionario,
    )

    return JsonResponse(
        {
            "horarios": horarios,
            "duracao": servico.duracao,
            "abertura": (
                configuracao_dia.hora_abertura.strftime("%H:%M")
                if configuracao_dia.hora_abertura
                else ""
            ),
            "fechamento": (
                configuracao_dia.hora_fechamento.strftime("%H:%M")
                if configuracao_dia.hora_fechamento
                else ""
            ),
        }
    )


@login_required(login_url="login")
def agendamento(request):
    horarios_para_formulario = []

    if request.method == "POST":
        servico_id = request.POST.get("servico")
        funcionario_id = request.POST.get("funcionario")
        data_texto = request.POST.get("data")

        if (
            servico_id
            and funcionario_id
            and data_texto
        ):
            try:
                servico = Servico.objects.get(
                    id=servico_id,
                    ativo=True,
                )

                funcionario = Funcionario.objects.get(
                    id=funcionario_id,
                    ativo=True,
                )

                data = datetime.strptime(
                    data_texto,
                    "%Y-%m-%d",
                ).date()

                horarios_para_formulario = (
                    buscar_horarios_disponiveis(
                        data,
                        servico,
                        funcionario,
                    )
                )

            except (
                Servico.DoesNotExist,
                Funcionario.DoesNotExist,
                ValueError,
            ):
                pass

        form = AgendamentoForm(
            request.POST,
            horarios_disponiveis=horarios_para_formulario,
        )

        if form.is_valid():
            data_escolhida = (
                form.cleaned_data["data"]
            )

            servico_escolhido = (
                form.cleaned_data["servico"]
            )

            funcionario_escolhido = (
                form.cleaned_data["funcionario"]
            )

            horario_escolhido = (
                form.cleaned_data["horario"]
                .strftime("%H:%M")
            )

            configuracao_dia = buscar_configuracao_dia(
                data_escolhida
            )

            bloqueio = buscar_bloqueio_data(
                data_escolhida
            )

            if data_escolhida < timezone.localdate():
                form.add_error(
                    "data",
                    (
                        "Não é permitido agendar "
                        "em uma data anterior."
                    ),
                )

            elif configuracao_dia is None:
                form.add_error(
                    "data",
                    (
                        "Esse dia ainda não "
                        "foi configurado."
                    ),
                )

            elif not configuracao_dia.aberto:
                form.add_error(
                    "data",
                    (
                        "O salão não funciona "
                        "nesse dia."
                    ),
                )

            elif bloqueio and bloqueio.dia_inteiro:
                form.add_error(
                    "data",
                    (
                        "Essa data está bloqueada "
                        "pela administradora."
                    ),
                )

            else:
                horarios_atualizados = (
                    buscar_horarios_disponiveis(
                        data_escolhida,
                        servico_escolhido,
                        funcionario_escolhido,
                    )
                )

                if horario_escolhido not in horarios_atualizados:
                    form.add_error(
                        "horario",
                        (
                            "Esse horário não está disponível "
                            "para este profissional."
                        ),
                    )

                else:
                    novo_agendamento = form.save(
                        commit=False
                    )

                    novo_agendamento.cliente = (
                        request.user
                    )

                    novo_agendamento.status = (
                        Agendamento.STATUS_PENDENTE
                    )

                    novo_agendamento.save()

                    messages.success(
                        request,
                        "Agendamento realizado com sucesso!",
                    )

                    return redirect("perfil")

    else:
        form = AgendamentoForm()

    return render(
        request,
        "agendamentos/agendamento.html",
        {
            "form": form,
            "hoje": (
                timezone.localdate().isoformat()
            ),
        },
    )


@login_required(login_url="login")
@require_POST
def cancelar_agendamento(
    request,
    agendamento_id,
):
    agendamento_cliente = get_object_or_404(
        Agendamento,
        id=agendamento_id,
        cliente=request.user,
    )

    if not agendamento_cliente.pode_cliente_cancelar:
        messages.error(
            request,
            (
                "Esse agendamento não pode "
                "mais ser cancelado."
            ),
        )

        return redirect("perfil")

    agendamento_cliente.status = (
        Agendamento.STATUS_CANCELADO_CLIENTE
    )

    agendamento_cliente.motivo_status = (
        "Cancelado pela cliente através do sistema."
    )

    agendamento_cliente.save(
        update_fields=[
            "status",
            "motivo_status",
            "atualizado_em",
        ]
    )

    messages.success(
        request,
        "Agendamento cancelado com sucesso.",
    )

    return redirect("perfil")
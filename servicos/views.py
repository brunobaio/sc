from django.shortcuts import render

from .models import Servico


def lista_servicos(request):

    servicos = (
        Servico.objects
        .filter(ativo=True)
        .order_by("nome")
    )

    contexto = {
        "servicos": servicos
    }

    return render(
        request,
        "servicos/lista_servicos.html",
        contexto
    )
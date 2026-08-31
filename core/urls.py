from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "financeiro/",
        include("financeiro.urls"),
    ),

    path(
        "",
        include("paginas.urls"),
    ),

    path(
        "servicos/",
        include("servicos.urls"),
    ),

    path(
        "contas/",
        include("contas.urls"),
    ),

    path(
        "agendamento/",
        include("agendamentos.urls"),
    ),

    path(
        "painel/funcionarios/",
        include("funcionarios.urls"),
    ),

    path(
        "painel/",
        include("painel.urls"),
    ),

    path(
    "produtos/",
    include("produtos.urls"),
    ),

    path(
    "avaliacoes/",
    include("avaliacoes.urls"),
),

]


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
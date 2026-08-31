from funcionarios.models import Funcionario
from servicos.models import Servico


funcionarias = [

    {
        "nome": "Lavínia Busnardo",
        "cpf": "SEM-CPF-001",
        "telefone": "Não informado",
        "cargo": Funcionario.CARGO_CABELEIREIRA,

        "servicos": [
            "Corte Feminino",
            "Escova",
            "Escova Modelada",
            "Coloração",
            "Luzes",
            "Hidratação",
            "Progressiva",
        ],
    },

    {
        "nome": "Nicoly Tuany",
        "cpf": "SEM-CPF-002",
        "telefone": "Não informado",
        "cargo": Funcionario.CARGO_MANICURE,

        "servicos": [
            "Manicure",
            "Pedicure",
        ],
    },

    {
        "nome": "Alana Coelho",
        "cpf": "SEM-CPF-003",
        "telefone": "Não informado",
        "cargo": Funcionario.CARGO_MAQUIADORA,

        "servicos": [
            "Design de Sobrancelhas",
            "Maquiagem Social",
            "Maquiagem Noiva",
        ],
    },

    {
        "nome": "Maria Eduarda",
        "cpf": "SEM-CPF-004",
        "telefone": "Não informado",
        "cargo": Funcionario.CARGO_ESTETICISTA,

        "servicos": [
            "Penteado Noiva",
        ],
    },

]


for dados in funcionarias:

    funcionaria, criada = Funcionario.objects.update_or_create(

        nome=dados["nome"],

        defaults={
            "cpf": dados["cpf"],
            "telefone": dados["telefone"],
            "cargo": dados["cargo"],
            "ativo": True,
        },
    )

    servicos = Servico.objects.filter(
        ativo=True,
        nome__in=dados["servicos"],
    )

    funcionaria.servicos.set(servicos)

    print(f"\n{funcionaria.nome}")

    if servicos.exists():

        print("Serviços:")

        for servico in servicos:
            print(f"  - {servico.nome}")

    else:
        print("Nenhum serviço encontrado.")


print("\nFuncionárias atualizadas com sucesso!")
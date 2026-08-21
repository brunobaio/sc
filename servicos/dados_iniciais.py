from .models import Servico


def cadastrar_servicos():

    servicos = [

        {
            "nome": "Corte Feminino",
            "descricao": "Lavagem e corte profissional.",
            "preco": 60,
            "duracao": 60,
        },

        {
            "nome": "Escova",
            "descricao": "Escova lisa.",
            "preco": 45,
            "duracao": 45,
        },

        {
            "nome": "Escova Modelada",
            "descricao": "Escova com modelagem.",
            "preco": 55,
            "duracao": 60,
        },

        {
            "nome": "Chapinha",
            "descricao": "Finalização com chapinha.",
            "preco": 35,
            "duracao": 30,
        },

        {
            "nome": "Babyliss",
            "descricao": "Modelagem com babyliss.",
            "preco": 50,
            "duracao": 45,
        },

        {
            "nome": "Lavagem",
            "descricao": "Lavagem simples.",
            "preco": 20,
            "duracao": 20,
        },

        {
            "nome": "Coloração Completa",
            "descricao": "Coloração total.",
            "preco": 180,
            "duracao": 180,
        },

        {
            "nome": "Retoque de Raiz",
            "descricao": "Retoque da raiz.",
            "preco": 120,
            "duracao": 120,
        },

        {
            "nome": "Luzes",
            "descricao": "Aplicação de luzes.",
            "preco": 280,
            "duracao": 240,
        },

        {
            "nome": "Mechas",
            "descricao": "Mechas completas.",
            "preco": 320,
            "duracao": 240,
        },

        {
            "nome": "Morena Iluminada",
            "descricao": "Técnica Morena Iluminada.",
            "preco": 450,
            "duracao": 300,
        },

        {
            "nome": "Platinado",
            "descricao": "Descoloração completa.",
            "preco": 650,
            "duracao": 360,
        },

        {
            "nome": "Hidratação",
            "descricao": "Tratamento hidratante.",
            "preco": 60,
            "duracao": 45,
        },

        {
            "nome": "Nutrição",
            "descricao": "Nutrição capilar.",
            "preco": 70,
            "duracao": 45,
        },

        {
            "nome": "Reconstrução",
            "descricao": "Reconstrução dos fios.",
            "preco": 90,
            "duracao": 60,
        },

        {
            "nome": "Botox Capilar",
            "descricao": "Tratamento Botox.",
            "preco": 180,
            "duracao": 150,
        },

        {
            "nome": "Progressiva",
            "descricao": "Escova progressiva.",
            "preco": 250,
            "duracao": 240,
        },

        {
            "nome": "Manicure",
            "descricao": "Serviço de manicure.",
            "preco": 35,
            "duracao": 45,
        },

        {
            "nome": "Pedicure",
            "descricao": "Serviço de pedicure.",
            "preco": 40,
            "duracao": 50,
        },

        {
            "nome": "Manicure e Pedicure",
            "descricao": "Combo unhas.",
            "preco": 65,
            "duracao": 90,
        },

        {
            "nome": "Esmaltação em Gel",
            "descricao": "Unhas em gel.",
            "preco": 80,
            "duracao": 90,
        },

        {
            "nome": "Alongamento de Unhas",
            "descricao": "Alongamento completo.",
            "preco": 180,
            "duracao": 180,
        },

        {
            "nome": "Manutenção Alongamento",
            "descricao": "Manutenção.",
            "preco": 100,
            "duracao": 120,
        },

        {
            "nome": "Design de Sobrancelhas",
            "descricao": "Design.",
            "preco": 35,
            "duracao": 30,
        },

        {
            "nome": "Henna",
            "descricao": "Aplicação de Henna.",
            "preco": 45,
            "duracao": 40,
        },

        {
            "nome": "Design + Henna",
            "descricao": "Design completo.",
            "preco": 60,
            "duracao": 45,
        },

        {
            "nome": "Brow Lamination",
            "descricao": "Alinhamento das sobrancelhas.",
            "preco": 150,
            "duracao": 90,
        },

        {
            "nome": "Lash Lifting",
            "descricao": "Lifting de cílios.",
            "preco": 180,
            "duracao": 90,
        },

        {
            "nome": "Extensão Fio a Fio",
            "descricao": "Cílios fio a fio.",
            "preco": 220,
            "duracao": 150,
        },

        {
            "nome": "Volume Brasileiro",
            "descricao": "Volume brasileiro.",
            "preco": 250,
            "duracao": 180,
        },

        {
            "nome": "Manutenção de Cílios",
            "descricao": "Manutenção.",
            "preco": 120,
            "duracao": 90,
        },

        {
            "nome": "Maquiagem Social",
            "descricao": "Maquiagem.",
            "preco": 180,
            "duracao": 90,
        },

        {
            "nome": "Maquiagem Festa",
            "descricao": "Maquiagem completa.",
            "preco": 220,
            "duracao": 120,
        },

        {
            "nome": "Maquiagem Formatura",
            "descricao": "Formatura.",
            "preco": 250,
            "duracao": 120,
        },

        {
            "nome": "Noiva Completa",
            "descricao": "Pacote Noiva.",
            "preco": 1500,
            "duracao": 360,
        },

        {
            "nome": "Dia da Noiva Premium",
            "descricao": "Pacote Premium.",
            "preco": 2300,
            "duracao": 480,
        },

        {
            "nome": "Pacote Madrinha",
            "descricao": "Maquiagem + Penteado.",
            "preco": 420,
            "duracao": 180,
        },

        {
            "nome": "Pacote Formanda",
            "descricao": "Maquiagem + Penteado.",
            "preco": 380,
            "duracao": 180,
        },

        {
            "nome": "Pacote Debutante",
            "descricao": "Maquiagem + Penteado.",
            "preco": 450,
            "duracao": 180,
        }

    ]

    for s in servicos:
        Servico.objects.get_or_create(
            nome=s["nome"],
            defaults={
                "descricao": s["descricao"],
                "preco": s["preco"],
                "duracao": s["duracao"],
                "ativo": True,
            }
        )
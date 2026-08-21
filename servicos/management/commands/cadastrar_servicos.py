from django.core.management.base import BaseCommand
from servicos.models import Servico


class Command(BaseCommand):

    help = "Cadastra serviços iniciais do salão"


    def handle(self, *args, **kwargs):

        servicos = [

            ("Corte Feminino", "Corte profissional", 60, 60),

            ("Escova", "Escova simples", 45, 45),

            ("Escova Modelada", "Escova com modelagem", 55, 60),

            ("Coloração", "Coloração completa", 180, 180),

            ("Luzes", "Luzes no cabelo", 280, 240),

            ("Mechas", "Mechas completas", 320, 240),

            ("Hidratação", "Tratamento capilar", 60, 45),

            ("Botox Capilar", "Tratamento Botox", 180, 150),

            ("Progressiva", "Alisamento", 250, 240),

            ("Manicure", "Unhas das mãos", 35, 45),

            ("Pedicure", "Unhas dos pés", 40, 50),

            ("Design de Sobrancelhas", "Design", 35, 30),

            ("Henna", "Sobrancelha com henna", 45, 40),

            ("Maquiagem Social", "Maquiagem para eventos", 180, 90),

            ("Maquiagem Noiva", "Maquiagem especial noiva", 350, 120),

            ("Penteado Noiva", "Penteado de casamento", 500, 180),

            ("Dia da Noiva Premium", "Pacote completo da noiva", 2000, 480),

            ("Pacote Madrinha", "Maquiagem + penteado", 420, 180),

            ("Pacote Formanda", "Maquiagem + penteado", 380, 180),

        ]


        for nome, descricao, preco, duracao in servicos:

            Servico.objects.get_or_create(
                nome=nome,
                defaults={
                    "descricao": descricao,
                    "preco": preco,
                    "duracao": duracao,
                    "ativo": True
                }
            )


        self.stdout.write(
            self.style.SUCCESS(
                "Serviços cadastrados com sucesso!"
            )
        )
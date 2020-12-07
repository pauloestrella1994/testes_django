from decimal import Decimal, ROUND_DOWN
from django.db import models

class Sabor(models.Model):
    sabor = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.sabor}'

class Sorvete(models.Model):
    unidades = models.PositiveIntegerField('unidades')
    sabores = models.ManyToManyField('sabor')
    preco_de_venda = models.DecimalField(
        'Preço de venda',
        max_digits=6,
        decimal_places=2,
        default=Decimal('0')
    )
    preco_de_custo = models.DecimalField(
        'Preço de custo',
        max_digits=6,
        decimal_places=2
    )

    def __str__(self):
        sabores = ''.join(str(sabor) for sabor in self.sabores.all())
        exibicao = f'{sabores} {str(self.preco_de_venda).replace(".", ",")}'
        return exibicao
    
    def calcula_preco_de_venda(self):
        """
        Deve ser respeitadas as seguintes regras para precificação do sorvete:

        Porcentagem baseada no total/Condição
        A cada 10 unidades, cujo valor total de custo seja 0 < valor <= 24.99
        O preço de custo será igual ao valor unitário + 10% do valor unitário
        A cada 10 unidades, cujo valor total de custo seja 25 <= valor <= 49.99
        O preço de custo será igual ao valor unitário + 20% do valor unitário
        A cada 10 unidades, cujo valor total de custo seja valor >= 50
        O preço de custo será igual ao valor unitário + 35% do valor unitário

        """
        preco_de_custo = self.preco_de_custo * 10
        if preco_de_custo <= Decimal('24.99'):
            self.preco_de_venda = (
                    self.preco_de_custo + self.preco_de_custo * 0.1
            )

        elif preco_de_custo >=Decimal('25') and \
            preco_de_custo <= Decimal('49.99'):
            self.preco_de_venda = (
                self.preco_de_custo + self.preco_de_custo * 0.2
            )
            
        else:
            self.preco_de_venda = (
                self.preco_de_custo + self.preco_de_custo * 0.35
            )
        self.save()
        return Decimal(str(self.preco_de_venda)).quantize(
            Decimal('0.01'),
            rounding=ROUND_DOWN
        )
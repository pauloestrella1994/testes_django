from decimal import Decimal
from django.test import TestCase
from core.models import Sabor, Sorvete

class TestModelSabor(TestCase):
    def setUp(self) -> None:
        self.sabor = Sabor(sabor='abacate')
    
    def test_retorna_sabor(self):
        esperado = 'abacate'
        resultado = str(self.sabor)
        self.assertEqual(esperado, resultado)

class TestModelSorvete(TestCase):
    def setUp(self) -> None:
        self.sabor = Sabor.objects.create(sabor='abacate')
        self.sorvete = Sorvete.objects.create(
            unidades=1,
            preco_de_venda=1,
            preco_de_custo=0.5
        )
        self.sorvete.sabores.set((self.sabor, ))

    def test_retorno_sorvete_e_preco(self):
        esperado = 'abacate 1'
        resultado = str(self.sorvete)
        self.assertEqual(esperado, resultado)
    
    def test_calcula_preco_de_venda_retorna_0_55(self):
        esperado = Decimal('0.55')
        resultado = self.sorvete.calcula_preco_de_venda()
        self.assertEqual(esperado, resultado)
    
    def test_calcula_preco_de_venda_retorna_5_98(self):
        sabor = Sabor.objects.create(sabor='abacate')
        sorvete = Sorvete.objects.create(
            unidades=10,
            preco_de_venda=0,
            preco_de_custo=4.99
        )        
        sorvete.sabores.set((sabor, ))
        
        esperado = Decimal('5.98')
        resultado = sorvete.calcula_preco_de_venda()
        self.assertEqual(esperado, resultado)
    
    def test_calcula_preco_de_venda_retorna_8_10(self):
        sabor = Sabor.objects.create(sabor='abacate')
        sorvete = Sorvete.objects.create(
            unidades=10,
            preco_de_venda=0,
            preco_de_custo=6
        )        
        sorvete.sabores.set((sabor, ))
        
        esperado = Decimal('8.10')
        resultado = sorvete.calcula_preco_de_venda()
        self.assertEqual(esperado, resultado)

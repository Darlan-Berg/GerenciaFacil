from random import randint

class Produtos():
    def __init__(self, nome: str, marca: str, valor_produtos: float, quantidade: int, data_validade: str):
        self.nome = nome
        self.marca = marca
        self.valor_produtos = valor_produtos
        self.quantidade = quantidade
        self.valor_unit = self.valor_compra / self.quantidade # limitar quantidade de casas decimais
        self.data_validade = data_validade

class Compra:
    def __init__(self, lista_produtos: list, data: str):
        self.lista_produtos = lista_produtos
        self.data = data
        self.codigo = randint(0, 100)
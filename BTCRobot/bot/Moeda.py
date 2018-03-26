# -*- coding: utf-8 -*-
from Cotacao import Cotacao

class Moeda:

    def __init__(self, nome, ticker):
        self.nome = nome
        self.ticher = ticker
        self.cotacaoDia = Cotacao()

    @property
    def nome(self):
        return self.nome

    @property
    def ticker(self):
        return self.ticker












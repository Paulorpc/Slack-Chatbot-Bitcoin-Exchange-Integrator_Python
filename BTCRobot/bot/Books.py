# -*- coding: utf-8 -*-

import Ordem

class OrdersBookUsuario:

    __executadas = []
    __compras = []
    __vendas  = []

    def addOrdem(self, ordem):
        if not isinstance(ordem, Ordem): raise TypeError

        if   ordem.tipo == Ordem.TipoOrdem.COMPRA:   self.compras.append(ordem)
        elif ordem.tipo == Ordem.TipoOrdem.VENDA:    self.vendas.append(ordem)


    def executaOrdem(self, ordem):
        if not isinstance(ordem, Ordem): raise TypeError

        if ordem.tipo == Ordem.TipoOrdem.COMPRA:
           self.__executadas.append( self.__compras.remove(ordem) )
        elif ordem.tipo == Ordem.TipoOrdem.VENDA:
           self.__executadas.append( self.__vendas.remove(ordem) )


    @property
    def compras(self):
        return self.compras

    @property
    def vendas(self):
        return self.vendas

    @property
    def executadas(self):
        return self.executadas


class OrdersBookPublica:

    __executadas = []
    __compras = []
    __vendas = []

    def addOrdem(self, ordem):
        if not isinstance(ordem, Ordem): raise TypeError

        if not ordem.status == Ordem.Status.EXECUTADA:
            if ordem.tipo == Ordem.TipoOrdem.COMPRA:
                self.compras.append(ordem)
            elif ordem.tipo == Ordem.TipoOrdem.VENDA:
                self.vendas.append(ordem)
        else:
            self.__executadas.append(ordem)

    @property
    def compras(self):
        return self.compras

    @property
    def vendas(self):
        return self.vendas

    @property
    def executadas(self):
        return self.executadas

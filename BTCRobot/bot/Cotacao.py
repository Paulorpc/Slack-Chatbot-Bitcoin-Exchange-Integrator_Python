# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

class Cotacao:

    def __init__(self):
        self._precoMax = 0.0
        self._precoMin = 0.0
        self._volume = 0.0
        self._precoUltimaNegociacao = 0.0
        self._precoMaiorOfeCompra = 0.0
        self._precoMenorOfeVenda = 0.0
        self._precoAbertura = 0.0
        self._precoFechamento = 0.0
        self._dataHora_Unix = None
        self._dataHora = None
        self._dataHoraInicial_Unix = None
        self._dataHoraInicial = None

        self.__precoMax_old = 0.0
        self.__precoMin_old = 0.0
        self.__volume_old = 0.0
        self.__precoUltimaNegociacao_old = 0.0
        self.__precoMaiorOfeCompra_old = 0.0
        self.__precoMenorOfeVenda_old = 0.0
        self.__dataHora_Unix_old = None
        self.__dataHora_old = None
        self.__variacaoDia = 0.0
        self.__variacaoSemana = 0.0


    @property
    def precoMax(self):
        '''
        Maior valor, em reais, de negociação nas últimas 24 horas.
        :return:
        '''
        return float(self._precoMax)

    @precoMax.setter
    def precoMax(self, value):
        self._precoMax = float(value)

    @property
    def precoMin(self):
        '''
        Menor valor, em reais, de negociação nas últimas 24 horas.
        :return:
        '''
        return float(self._precoMin)

    @precoMin.setter
    def precoMin(self, value):
        '''
        Menor valor, em reais, de negociação nas últimas 24 horas.
        :param value:
        :return:
        '''
        self._precoMin = float(value)

    @property
    def volume(self):
        '''
        VOL: Volume de bitcoins/litecoins negociados nas últimas 24 horas.
        :return:
        '''
        return self._volume

    @volume.setter
    def volume(self, value):
        '''
        VOL: Volume de bitcoins/litecoins negociados nas últimas 24 horas.
        :param value:
        :return:
        '''
        self._volume = value

    @property
    def precoUltimaNegociacao(self):
        '''
        LAST: Preço unitário do último negócio, em reais.
        :return:
        '''
        return float(self._precoUltimaNegociacao)

    @precoUltimaNegociacao.setter
    def precoUltimaNegociacao(self, value):
        '''
        LAST: Preço unitário do último negócio, em reais.
        :param value:
        :return:
        '''
        self._precoUltimaNegociacao = float(value)

    @property
    def precoMaiorOfeCompra(self):
        '''
        BUY: Maior valor, em reais, de oferta de compra.
        :return:
        '''
        return float(self._precoMaiorOfeCompra)

    @precoMaiorOfeCompra.setter
    def precoMaiorOfeCompra(self, value):
        '''
        BUY: Maior valor, em reais, de oferta de compra.
        :param value:
        :return:
        '''
        self._precoMaiorOfeCompra = float(value)

    @property
    def precoMenorOfeVenda(self):
        '''
        SELL: Menor valor, em reais, de oferta de venda.
        :return:
        '''
        return float(self._precoMenorOfeVenda)

    @precoMenorOfeVenda.setter
    def precoMenorOfeVenda(self, value):
        '''
        SELL: Menor valor, em reais, de oferta de venda.
        :param value:
        :return:
        '''
        self._precoMenorOfeVenda = float(value)

    @property
    def precoAbertura(self):
        return float(self.precoAbertura)

    @precoAbertura.setter
    def precoAbertura(self, value):
        self._precoAbertura = float(value)

    @property
    def precoFechamento(self):
        return float(self._precoFechamento)

    @precoFechamento.setter
    def precoFechamento(self, value):
        self._precoFechamento = float(value)

    def variacaoDia(self, tipo="perc"):
        return self.__variacaoDia

    def variacaoSemana(self, tipo="perc"):
        return self.__variacaoSemana

    def dataHora(self):
        '''
        Data e hora da última atualização da moeda
        :return: data hora
        '''
        return self._dataHora

    def dataHoraInicial(self):
        '''
        Data e hora da última atualização da moeda
        :return: data hora
        '''
        return self._dataHoraInicial



    def atualizaCotacaoMoeda(self, response_json):
        """
        Método de coleta de cotação diário da moeda.
        :param response_json: JSON com informações do MB
        """

        # Armazena valores atualizado em variaveis de suporte para verificar mudanças da cotação
        self.__precoMax_old = self._precoMax
        self.__precoMin_old = self._precoMin
        self.__volume_old = self._volume
        self.__precoUltimaNegociacao_old = self._precoUltimaNegociacao
        self.__precoMaiorOfeCompra_old = self.precoMaiorOfeCompra
        self.__precoMenorOfeVenda_old = self._precoMenorOfeVenda
        self.__dataHora_Unix_old = self._dataHora_Unix
        self.__dataHora_old = self._dataHora

        # Variaveis de cotação da moeda
        self._precoMax = float(response_json["ticker"]["high"])
        self._precoMin = float(response_json["ticker"]["low"])
        self._volume = float(response_json["ticker"]["vol"])
        self._precoUltimaNegociacao = float(response_json["ticker"]["last"])
        self._precoMaiorOfeCompra = float(response_json["ticker"]["buy"])
        self._precoMenorOfeVenda = float(response_json["ticker"]["sell"])
        self._dataHora_Unix = response_json["ticker"]["date"]
        self._dataHora = datetime.fromtimestamp(int(response_json["ticker"]["date"]))


        # Data hora da primeira atualização
        if self._dataHoraInicial is None:
            self._dataHoraInicial_Unix = response_json["ticker"]["date"]
            self._dataHoraInicial = datetime.fromtimestamp(int(response_json["ticker"]["date"]))

        # Desenvolvendo variação dia/semana
        else:
            dataReset = (self._dataHoraInicial + timedelta(days=1))
            if dataReset <= self.dataHora():
                print "--------> " + str(dataReset) + "  " + self.dataHora()
                self.__variacaoDia = 0.0

            dataReset = (self._dataHoraInicial + timedelta(days=7))
            if dataReset <= self.dataHora():
                print "--------> " + str(dataReset) + "  " + self.dataHora()
                self.__variacaoSemana = 0.0


            if self.__precoUltimaNegociacao_old > 0.0:
                self.__variacaoDia += ((self._precoUltimaNegociacao / self.__precoUltimaNegociacao_old)-1)*100
                self.__variacaoSemana += ((self._precoUltimaNegociacao / self.__precoUltimaNegociacao_old)-1)*100




    @property
    def precoMax_old(self):
        '''
        Maior valor, em reais, de negociação nas últimas 24 horas.
        :return:
        '''
        return float(self.__precoMax_old)

    @precoMax_old.setter
    def precoMax_old(self, value):
        self.__precoMax_old = float(value)

    @property
    def precoMin_old(self):
        '''
        Menor valor, em reais, de negociação nas últimas 24 horas.
        :return:
        '''
        return float(self.__precoMin_old)

    @precoMin_old.setter
    def precoMin_old(self, value):
        '''
        Menor valor, em reais, de negociação nas últimas 24 horas.
        :param value:
        :return:
        '''
        self.__precoMin_old = float(value)

    @property
    def volume_old(self):
        '''
        VOL: Volume de bitcoins/litecoins negociados nas últimas 24 horas.
        :return:
        '''
        return self.__volume_old

    @volume_old.setter
    def volume_old(self, value):
        '''
        VOL: Volume de bitcoins/litecoins negociados nas últimas 24 horas.
        :param value:
        :return:
        '''
        self.__volume_old = value

    @property
    def precoUltimaNegociacao_old(self):
        '''
        LAST: Preço unitário do último negócio, em reais.
        :return:
        '''
        return float(self.__precoUltimaNegociacao_old)

    @precoUltimaNegociacao_old.setter
    def precoUltimaNegociacao_old(self, value):
        '''
        LAST: Preço unitário do último negócio, em reais.
        :param value:
        :return:
        '''
        self.__precoUltimaNegociacao_old = float(value)

    @property
    def precoMaiorOfeCompra_old(self):
        '''
        BUY: Maior valor, em reais, de oferta de compra.
        :return:
        '''
        return float(self.__precoMaiorOfeCompra_old)

    @precoMaiorOfeCompra_old.setter
    def precoMaiorOfeCompra_old(self, value):
        '''
        BUY: Maior valor, em reais, de oferta de compra.
        :param value:
        :return:
        '''
        self.__precoMaiorOfeCompra_old = float(value)

    @property
    def precoMenorOfeVenda_old(self):
        '''
        SELL: Menor valor, em reais, de oferta de venda.
        :return:
        '''
        return float(self.__precoMenorOfeVenda_old)

    @precoMenorOfeVenda_old.setter
    def precoMenorOfeVenda_old(self, value):
        '''
        SELL: Menor valor, em reais, de oferta de venda.
        :param value:
        :return:
        '''
        self.__precoMenorOfeVenda_old = float(value)
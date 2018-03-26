# -*- coding: utf-8 -*-

from Config import Config
from enum import Enum
from Moeda import Moeda
from Util import Util, DataHora


class TipoOrdem(Enum):
    COMPRA = 'compra'
    VENDA = 'venda'

class Status(Enum):
    ATIVA = 'ativa'
    CANCELADA = 'cancelada'
    EXECUTADA = 'executada'


class Ordem:

    def __init__(self, tipo, moeda, qtde, preco):

        if not isinstance(moeda, Moeda):
            raise TypeError("moeda deve ser uma instancia Moeda")
        if not isinstance(tipo, TipoOrdem):
            raise TypeError("tipo deve ser uma instancia de TipoOrdem")
        if not isinstance(qtde, int) or not isinstance(qtde, float):
            raise TypeError("qtde deve ser uma instancia de int ou float")
        if not isinstance(preco, int) or not isinstance(preco, float):
            raise TypeError("preco deve ser uma instancia de int ou float")

        self.__preco = float(preco)
        self.__qtde = float(qtde)
        self.__tipo = tipo
        self.__moeda = moeda
        self.__dataCriacao = DataHora.hora()
        self.dataStatus = [ (Status.ATIVA, DataHora.hora()) ]
        self.status = Status.ATIVA


    def qtde(self):
        return self.__qtde

    def preco(self):
        return self.__preco

    def tipo(self):
        return self.__tipo

    def moeda(self):
        return self.__moeda

    @property
    def tipo(self):
        return self.tipo

    @tipo.setter
    def tipo(self, value):
        if isinstance(value, TipoOrdem):
            self.tipo = value
        else:
            raise TypeError

    @property
    def status(self):
        return self.status

    @status.setter
    def status(self, value):
        if isinstance(value, Status):
            self.status = value
            self.dataStatus.append( value, DataHora.hora() )
        else:
            raise TypeError

    def dataCriacao(self):
        return self.dataCriacao


    @staticmethod
    def getOrdensExecutadas(response_json, file=None):
        """
        Método de manipulação das ordens executadas no MB com condicional para monitoração de valores desejados apenas.
        :param file: Arquivo CSV para gravação dos dados
        :param response_json: JSON com informações do MB
        :return: Array com valores de interesse
        """

        aOrdensExecutadas = []

        # Grava em arquivo
        if file is not None:
            file.writerow(["TID", "DATA", "PREÇO", "QTDE BTC", "QTDE R$", "TIPO, ORDEM"])

        for item in response_json:
            valorReal = item["amount"] * item["price"]

            # Estipula o valor de insvestimento que deseja monitorar
            if ( valorReal >= Config.VALOR_ORDENS_MONITORADAS ):
                data = DataHora.formataDataHora(int(item["date"]))
                qtde = Util.formataQtde(item["amount"], 4)
                preco = Util.formataDinheiro(item["price"], None)
                valorReal = Util.formataDinheiro(valorReal, None)
                status = Status.EXECUTADA.name

                if (item["type"] == "buy"):     tipoOrdem = TipoOrdem.COMPRA.name
                elif (item["type"] == "sell"):  tipoOrdem = TipoOrdem.VENDA.name
                else:
                    raise "Tipo da ordem inválido"

                try:
                    # Grava em arquivo CSV e no vetor de retorno
                    if file is not None:
                        file.writerow([item["tid"], data, preco, qtde, valorReal, tipoOrdem, status])

                    aOrdensExecutadas.append([data, preco, qtde, tipoOrdem])

                except Exception as e:
                    print "Erro de execução no método ordensExecutadas(). \n>> " + e.message

        return aOrdensExecutadas


    @staticmethod
    def getOrdensCompraVenda(response_json, file=None):
        """
        Método de manipulação das ordens de Compra/Venda no MB com condicional para monitoração de valores desejados apenas.
        :param file: Arquivo CSV para gravação dos dados
        :param response_json: JSON com informações do MB
        :return: Array com valores de interesse
        """

        # Grava em arquivo
        aOrdensCompraVenda = [[], []]

        # Grava em arquivo
        if file is not None:
            file.writerow(["DATA", "PREÇO", "QTDE BTC", "QTDE R$", "ORDEM"])

        for itemType in response_json:
            for preco, qtde in response_json[itemType]:
                valorReal = round((qtde * preco), 2)

                # Estipula o valor de insvestimento que deseja monitorar
                if (valorReal >= Config.VALOR_ORDENS_MONITORADAS):

                    # Coloca linha em negrito na msg
                    if qtde > Config.QTDE_MOEDA_NEGRITO:
                        qtde  = "*" + Util.formataQtde(qtde, 4) + "*"
                        preco = "*" + Util.formataDinheiro(preco, None) + "*"
                    else:
                        qtde = Util.formataQtde(qtde, 4)
                        preco = Util.formataDinheiro(preco, None)

                    valorReal = Util.formataDinheiro(valorReal, None)

                    if (itemType == "asks"):
                        tipoOrdem = TipoOrdem.VENDA
                        i = 0
                    elif (itemType == "bids"):
                        tipoOrdem = TipoOrdem.COMPRA
                        i = 1
                    else:
                        tipoOrdem = "ERROR"
                        i = -1

                    try:
                        aOrdensCompraVenda[i].append([DataHora.hoje(), preco, qtde, valorReal, tipoOrdem])
                        # Grava em arquivo CSV e no vetor de retorno
                        if file is not None:
                            file.writerow([DataHora.hoje(), preco, qtde, valorReal, tipoOrdem])
                    except Exception as e:
                        print "Erro de execução no método ordensCompraVenda(). \n>> " + e.message

        return aOrdensCompraVenda

# -*- coding: utf-8 -*-

import Mensagens
from Global import Global
from Ordem import Ordem, TipoOrdem
from Config import Config
import csv
from Util import Tempo

class Estrategia:

    @staticmethod
    def painelCotacaoMoeda(moeda, metodoColeta, wsOrigem):
        ###### MENSAGEM DE INFORMATIVO DA MOEDA ######

        if Estrategia.atualizaCotacaoMoeda(moeda, metodoColeta, wsOrigem, 5*Tempo.MIN.value) is True:

            color = None
            # if (moeda.cotacaoDia.precoMax > moeda.cotacaoDia.precoMax_old and moeda.cotacaoDia.precoMax_old > 0.0):
            if (0.0 < moeda.cotacaoDia.precoMax_old < moeda.cotacaoDia.precoMax):
                color = "good"
            elif (moeda.cotacaoDia.precoMin < moeda.cotacaoDia.precoMin_old and moeda.cotacaoDia.precoMin_old > 0):
                color = "danger"

            msg = Mensagens.Painel.cotacaoMoeda(moeda, color)

            if moeda.cotacaoDia.precoMax >= moeda.cotacaoDia.precoMax_old or moeda.cotacaoDia.precoMin <= moeda.cotacaoDia.precoMin_old:
                Global.ws_Slack.postMessage(Config.SLACK_MEMBERID, msg)



    @staticmethod
    def painelOrdensExecutadas(moeda, metodoColeta, wsOrigem, gravarCsv=False):
        ###### MENSAGEM DE ORDENS EXECUTADAS ######
        try:
            metodo = metodoColeta.TRADES

            file = None
            if gravarCsv:
                file = csv.writer(open("mercadoBitcoin.csv", "wb+"))

            resp = wsOrigem.getDadosJSON(metodo)
            aOrdensExcutadas = Ordem.getOrdensExecutadas(resp, file)

        except Exception as e:
            print "\tException em 'Mensagem de ordens executadas': " + e.message
            pass
        else:
            # VERIFICA O ARRAY DE ORDENS EXECUTADAS DA COLETA ANTERIOR PARA SABER SE HÁ NOVAS ORDENS EXECUTADAS
            novasOrdensExecutadas = False
            for item in aOrdensExcutadas:
                if (Global.aOrdensExcutadas_old.__contains__(item)):
                    continue
                else:
                    novasOrdensExecutadas = True
                    break

            # ATUALIZA ARRAY DE ORDENS AUXILIAR PARA FUTURA COMPARAÇÃO
            Global.aOrdensExcutadas_old = aOrdensExcutadas[:]

            if (len(aOrdensExcutadas) > 0 and novasOrdensExecutadas):
                ordensCompra = ""
                ordensVenda = ""
                i = 0
                j = 0
                # MONTAGEM DO TEXTO PARA JSON DAS ORDENS DE COMPRA E VENDA EXECUTADAS
                for item in aOrdensExcutadas:
                    if (i < 10 and item[3] == TipoOrdem.COMPRA.name):
                        i += 1
                        ordensCompra += str(item[1]) + "\t" + str(item[2]) + "\n"

                    if (j < 10 and item[3] == TipoOrdem.VENDA.name):
                        j += 1
                        ordensVenda += str(item[1]) + "\t" + str(item[2]) + "\n"

                    if (i + j >= 20 or i + j >= len(aOrdensExcutadas)):
                        break

                color=""
                if len(ordensCompra) > len(ordensVenda):
                    color = "good"
                elif len(ordensCompra) < len(ordensVenda):
                    color = "danger"

                msg = Mensagens.Painel.ordensExecutadas(moeda, ordensCompra, ordensVenda, color=color)

                # Conexão server slack
                try:
                    Global.ws_Slack.postMessage(Config.SLACK_MEMBERID, msg)
                except Exception as e:
                    print "\tException em 'WS Slack - Ordens executadas': " + e.message
                    pass



    @staticmethod
    def painelOrdensCompraVenda(moeda, metodoColeta, wsOrigem, gravarCsv=False):
        ###### MENSAGEM DE ORDENS DE COMPRA/VENDA ######
        try:
            metodo = metodoColeta.ORDERBOOK

            file = None
            if gravarCsv:
                file = csv.writer(open("mercadoBitcoin.csv", "wb+"))

            resp = wsOrigem.getDadosJSON(metodo)
            aOrdensCompraVenda = Ordem.getOrdensCompraVenda(resp, file)
        except Exception as e:
            print "\tException em 'Mensagem de ordens compra/venda': " + e.message
            pass
        else:
            # MONTAGEM DO TEXTO PARA JSON DAS ORDENS DE COMPRA E VENDA
            ordensCompra = ""
            ordensVenda = ""
            for tipoOrdem in aOrdensCompraVenda:
                i = 0
                for ordem in tipoOrdem:
                    i += 1
                    if (i <= 10 and ordem[4] == TipoOrdem.COMPRA): ordensCompra += str(ordem[1]) + "\t" + str(ordem[2]) + "\n"
                    if (i <= 10 and ordem[4] == TipoOrdem.VENDA): ordensVenda += str(ordem[1]) + "\t" + str(ordem[2]) + "\n"

            msg = Mensagens.Painel.ordensCompraVenda(moeda, ordensCompra, ordensVenda)

            # Conexão server slack
            try:
                Global.ws_Slack.postMessage(Config.SLACK_MEMBERID, msg)
            except Exception as e:
                print "\tException em 'WS Slack - Ordens compra/venda': " + e.message
                pass


    @staticmethod
    def atualizaCotacaoMoeda(moeda, metodoColeta, wsOrigem, tempoEntreAtualizacao=0):

        # if moeda.cotacaoDia.dataHora() is None or DataHora.somaHora(moeda.cotacaoDia.dataHora(), tempoEntreAtualizacao) < DataHora.hora():
            try:
                metodo = metodoColeta.TICKER
                resp = wsOrigem.getDadosJSON(metodo)
                moeda.cotacaoDia.atualizaCotacaoMoeda(resp)
                return True

            except Exception as e:
                print "\tException em 'atualizaCotacaoMoeda': " + e.message
                return False
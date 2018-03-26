# -*- coding: utf-8 -*-

import urllib
import hmac
import hashlib
import httplib
import json

from Config import Config
from collections import OrderedDict
from enum import Enum

from slackclient import SlackClient


class MetodoColetaDadosMB(Enum):
    TICKER = 'ticker'
    TRADES = 'trades'
    ORDERBOOK = 'orderbook'


class MercadoBitcoin(Config):
    # Metodos privados de configuração (__XXX) herdados de 'Config'

    def __init__(self, TAPI_METHOD=None, COIN_PAIR=None):

        self.response = None
        self.responseJson = None

        if TAPI_METHOD is None:
            TAPI_METHOD = Config.TAPI_METHOD
        if COIN_PAIR is None:
            COIN_PAIR = Config.COIN_PAIR

        # Parâmetros URL
        self.__PARAMS = {
            'tapi_method': TAPI_METHOD,
            'tapi_nonce': Config.TAPI_NONCE,
            'coin_pair': COIN_PAIR              # MOEDA
        }
        self.__PARAMS = urllib.urlencode(self.__PARAMS)


    def getConn(self, metodo, desdeTid=None):
        return self.__conexao(metodo, desdeTid)

    def getDados(self, metodo, desdeTid=None):
        conn = self.__conexao(metodo, desdeTid)
        response = conn.getresponse()
        response = response.read()
        self.response = response

        if conn:
            conn.close()

        return response

    def getDadosJSON(self, metodo, desdeTid=None):
        response = self.getDados(metodo, desdeTid)
        responseJson = json.loads(response, object_pairs_hook=OrderedDict)
        self.responseJson = responseJson
        return responseJson



    def __conexao(self, metodo, desdeTid=None):
        """
        Método de conexão e coleta dos dados no Webservice do Mercado Bitboin (MB)
        :param METODO: Número do método que deseja chamar
        :param desdeTid: Último ID coletado de Ordens Executadas para continuar coleta a partir dele (opcional)
        :return: dados coletados como resposta do Webservice
        """
        if not isinstance(metodo, MetodoColetaDadosMB):
            raise "PASSE ITEM DE ENUM DA CLASSE 'metodoColetaDadosMB'"

        # Constantes
        request_path = '/api/' + str(metodo.name).lower() + '/'

        if (desdeTid > 0):
            requestParam = '?tid=' + desdeTid
            request_path += requestParam

        # Gerar MAC
        params_string = request_path + '?' + self.__PARAMS
        H = hmac.new(Config.MB_TAPI_SECRET, digestmod=hashlib.sha512)
        H.update(params_string)
        tapi_mac = H.hexdigest()

        # Gerar cabeçalho da requisição
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'TAPI-ID': Config.MB_TAPI_ID,
            'TAPI-MAC': tapi_mac
        }

        conn = None
        try:
            # Conexao publica usar metodo GET
            conn = httplib.HTTPSConnection(Config.REQUEST_HOST)
            conn.request("GET", request_path, self.__PARAMS, headers)

        except Exception as e:
            print "\tException em 'Conexão com webservice MB': " + e.message
            pass

        return conn



class Slack(Config):

    @staticmethod
    def getConn():
        token = Config.MAIN_USER.slack_tokenID
        return SlackClient(token)

    @staticmethod
    def postMessage(canal, msg, asUser=False, botname=Config.BOT_USER.nome, botIcon=Config.BOTICON):
        '''
        Método de envio de mensagem para o Slack.
        :param canal: ID do canal, grupo ou usuário de destino
        :param msg: Mensagem a ser enviada
        :param asUser: (True) Enviar como usuário padrão da conexão ou (False) como bot
        :param botname: Nome do bot exibido no envio da mensagem
        :param botIcon: icone do bot
        '''
        sc = Slack.getConn()
        sc.api_call(
            "chat.postMessage",
            channel=canal,
            username=botname,
            as_user=asUser,
            attachments=msg,
            icon_url=botIcon
        )

    def getListaUsuarios(self):
        return

    def getListaCanais(self):
        return

    def getIdUsuario(self, nome):
        return

    def getIdCanal(self, nome):
        return


    # v1.0
    # funcionando
    # while True:
    #
    #     slack_token = "xoxb-232327601397-69F1gxfCtkdFfAhdS23x32qy"
    #     sc = SlackClient(slack_token)
    #
    #     if sc.rtm_connect():
    #         while True:
    #
    #             for slack_message in sc.rtm_read():
    #                 tipo = slack_message.get("type")
    #                 channel = slack_message.get("channel")
    #                 message = slack_message.get("text")
    #                 user = slack_message.get("user")
    #
    #                 print tipo, channel, message, user
    #
    #                 if message == "cotacao":
    #                     sc.rtm_send_message("#btcbot", "<@{}>".format(user))
    #                     Estrategia.painelCotacaoMoeda(bitcoin, metodoColeta, ws_MB)
    #
    #                 if message == "funcionando":
    #                     sc.rtm_send_message("#btcbot", "<@{}> sim, estou. Obrigado pela preocupação!".format(user))
    #
    #             time.sleep(1)
    #     else:
    #         print "Connection Failed"


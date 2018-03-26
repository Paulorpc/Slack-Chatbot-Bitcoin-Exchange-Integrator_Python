# -*- coding: utf-8 -*-


__author__ = "Paulo Cezar"
__email__ = "paulorpc@gmail.com"
__status__ = "Production (beta)"


import time
from Util import Util, Time
from Global import Global
from Config import Config
from Estrategia import Estrategia

from slackclient import SlackClient

########################
# EXECUÇÃO DO PROGRAMA #
########################
bitcoin = Global.bitcoin
ws_MB = Global.ws_MB()
ws_Slack = Global.ws_Slack
metodoColeta = Global.metodoColeta

aOrdensExcutadas_old = []

horaInicialExec  = horaProxExecucao ="07:00"
horaFinalExec    = "20:00"
sleep            = 5 * Time.MIN.value

# horaInicialExec  = datetime(2017,  1,  1,  8, 30, 00, 000000)   # 08:30
# horaProxExecucao = datetime(2017,  1,  1,  8, 30, 00, 000000)   # 08:30
# horaFinalExec    = datetime(2050, 12, 31, 19, 30, 00, 000000)   # 19:00

while True:

    # sc = SlackClient(Config.BOT_USER.slack_tokenID)
    # if sc.rtm_connect():
    #
    #     while True:
    #
    #         for slack_message in sc.rtm_read():
    #             tipo = slack_message.get("type")
    #             channel = slack_message.get("channel")
    #             message = slack_message.get("text")
    #             user = slack_message.get("user")
    #
    #             print tipo, channel, message, user
    #
    #             if message == "cotacao":
    #                 sc.rtm_send_message("#btcbot", "<@{}>".format(user))
    #                 Estrategia.painelCotacaoMoeda(bitcoin, metodoColeta, ws_MB)
    #
    #             if message == "funcionando":
    #                 sc.rtm_send_message("#btcbot", "<@{}> sim, estou. Obrigado pela preocupação!".format(user))
    #
    #             if message == "tem alguem ai?":
    #                 sc.rtm_send_message("#btcbot", "<@{}> sim, como posso ajudar?".format(user))
    #
    #         time.sleep(1)
    #
    # else:
    #     print "Falha na conexão RTM"


    agora = Util.hora()
    print "Out Timer:    >> " + agora

    if not QUIT_PROGRAM:

        if (horaInicialExec <= agora <= horaFinalExec) or Config.DEBUG_MODE:
            print "Active Timer: >> " + agora

            # Painel de cotação 24h
            Estrategia.painelCotacaoMoeda(bitcoin, metodoColeta, ws_MB)

            # Ordens Executadas
            Estrategia.painelOrdensExecutadas(bitcoin, metodoColeta, ws_MB)

            # INICIO DE TIMER PARA ENVIO DE ORDENS COMPRA/VENDA
            if (horaInicialExec <= horaProxExecucao <= agora <= horaFinalExec) or Config.DEBUG_MODE:
                print "In Timer:     >> " + Util.hora()

                # Ordens compra/venda
                Estrategia.painelOrdensCompraVenda(bitcoin, metodoColeta, ws_MB)

                horaProxExecucao = Util.formataHora(Util.somaHora(2 * Time.HORA.value))

        print ">> Prox Execucao: " + horaProxExecucao + " Now: " + Util.hora() + " final: " + horaFinalExec

        # if not Config.DEBUG_MODE:
        #     time.sleep(sleep)

        Estrategia.atualizaCotacaoMoeda(bitcoin, metodoColeta, ws_MB)

    else:
        print "else"
        # sc.rtm_send_message(channel, "<@{}> Grupo não autorizado a utilizar o bot. \nContate: paulorpc@gmail.com".format(user))

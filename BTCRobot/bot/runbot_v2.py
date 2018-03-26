# -*- coding: utf-8 -*-

__author__ = "Paulo Cezar"
__email__  = "paulorpc@gmail.com"
__status__ = "Production (beta)"

from Util import Util, Tempo, DataHora
from datetime import datetime, timedelta
from Global import Global
from Config import Config
from Estrategia import Estrategia
from slackclient import SlackClient
from Triggers import Triggers


########################
# EXECUÇÃO DO PROGRAMA #
########################
bitcoin = Global.bitcoin
ws_MB = Global.ws_MB()
metodoColeta = Global.metodoColeta

aOrdensExcutadas_old = []

horaInicialExec  = datetime.today().replace(hour=7, minute=0, second=0, microsecond=0)
horaFinalExec    = datetime.today().replace(hour=21, minute=0, second=0, microsecond=0)
horaProxExec_PC = horaProxExec_OEx = horaProxExec_OCV = horaInicialExec

while True:
    sc = SlackClient(Config.BOT_USER.slack_tokenID)
    if sc.rtm_connect():
        print 'teste';
        SAIR = False
        # LOOP DO PROGRAMA
        while not SAIR:
            # EXECUCAO DO SLACK RTM - ITERACAO BOT
            if Config.RTM_ATIVO:
                try:
                    for slack_message in sc.rtm_read():

                        tipo = Util.unicodeToUtf8(slack_message.get("type"), toLower=True)
                        channel = Util.unicodeToUtf8(slack_message.get("channel"), toLower=True)
                        message = Util.unicodeToUtf8(slack_message.get("text"), toLower=True)
                        user = slack_message.get("user")
                        print "** Evento RTM recebido :: {} :: {} | {} | {} | {}" .format(Config.SLACK_MEMBERID, tipo, channel, message, user)

                        # GATILHOS DE TEXTO PARA AÇÃO DO BOT
                        triggers = Triggers(sc, slack_message)
                        triggers.execTriggers()

                except Exception as e:
                    print "Problema com slack RTM: " + str(e)
                    SAIR = True
                    pass


            # EXECUCAO DO WEB API (Slack/MB) - POST MENSAGENS
            if Config.WEBAPI_ATIVO:

                agora = DataHora.hojeHora()

                # SE CHEGOU AO FINAL DO PERIODO DE EXECUÇÃO, AVANÇA O DIA.
                if agora >= horaFinalExec:
                    horaInicialExec = horaInicialExec + timedelta(days=1)
                    horaFinalExec   = horaFinalExec   + timedelta(days=1)

                # PERÍODO DE EXECUÇÃO DE INTERESSE
                if (horaInicialExec <= agora <= horaFinalExec) or Config.DEBUG_MODE:

                    # EXECUÇÃO E PROGRAMAÇÃO DO ENVIO DE PAINEL COTACAO
                    if (horaProxExec_PC <= agora and Config.timer_PainelCotacao_ATIVO) or Config.DEBUG_MODE:
                        Estrategia.painelCotacaoMoeda(bitcoin, metodoColeta, ws_MB)
                        horaProxExec_PC = DataHora.somaHora(agora, 6 * Tempo.HORA.value)
                        print ">> Painel Cotação      :: Agora: {} | Prox Execucao: {} | Fim: {}" .format(DataHora.hora(), horaProxExec_PC, horaFinalExec)

                    # EXECUÇÃO E PROGRAMAÇÃO DO ENVIO DE ORDENS EXECUTADAS
                    if (horaProxExec_OEx <= agora and Config.timer_OrdensExecutadas_ATIVO) or Config.DEBUG_MODE:
                        Estrategia.painelOrdensExecutadas(bitcoin, metodoColeta, ws_MB)
                        horaProxExec_OEx = DataHora.somaHora(agora, 2 * Tempo.HORA.value)
                        print ">> Ordens Executadas   :: Agora: {} | Prox Execucao: {} | Fim: {}".format(DataHora.hora(), horaProxExec_OEx, horaFinalExec)

                    # EXECUÇÃO E PROGRAMAÇÃO DO ENVIO DE ORDENS COMPRA/VENDA
                    if (horaProxExec_OCV <= agora and Config.timer_OrdensCompraVenda_ATIVO) or Config.DEBUG_MODE:
                        Estrategia.painelOrdensCompraVenda(bitcoin, metodoColeta, ws_MB)
                        horaProxExec_OCV = DataHora.somaHora(agora, 2 * Tempo.HORA.value)
                        print ">> Ordens Compra/Venda :: Agora: {} | Prox Execucao: {} | Fim: {}" .format(DataHora.hora(), horaProxExec_OCV, horaFinalExec)

# -*- coding: utf-8 -*-

from Util import Util
from Global import Global
from Config import Config
from Estrategia import Estrategia
import Mensagens


class Triggers:

    def __init__(self, sc, slack_message):

        self.__sc = sc

        self.__tipo = Util.unicodeToUtf8(slack_message.get("type"), toLower=True)
        self.__channel = Util.unicodeToUtf8(slack_message.get("channel"), toLower=True)
        self.__message = Util.unicodeToUtf8(slack_message.get("text"), toLower=True)
        self.__user = slack_message.get("user")

        self.__bitcoin = Global.bitcoin
        self.__ws_MB = Global.ws_MB()
        self.__ws_Slack = Global.ws_Slack
        self.__metodoColeta = Global.metodoColeta



    def execTriggers(self):
        """
        Executa todas as triggers existentes
        :return:
        """
        self.painelAcoes()
        self.painelCotacao()
        self.painelOrdensCompraVenda()
        self.painelOrdensExecutadas()
        self.botAlguemAi()
        self.botFuncionando()
        self.botDono()
        self.botSobre()
        self.valorOrdens()


    def triggersValorOrdens(self):
        triggers = []
        triggers.append("valorOrdens")
        triggers.append("valor_ordens")
        triggers.append("filtros")
        triggers.append("filtro")
        triggers.append("filtro_Valor")
        triggers.append("filtros_Valor")
        triggers.append("filtro_Valores")
        triggers.append("filtros_Valores")
        triggers.append("filtroValores")
        triggers.append("filtrosValores")
        return triggers

    def triggersPainelAcoes(self):
        triggers = []
        triggers.append("ação")
        triggers.append("ações")
        triggers.append("##")
        triggers.append("info")
        triggers.append("dicas")
        triggers.append("detalhe")
        triggers.append("detalhes")
        return triggers

    def triggersPainelCotacao(self):
        triggers = []
        triggers.append("painelcotação")
        triggers.append("paineldecotação")
        triggers.append("painel_cotação")
        triggers.append("cotação")
        triggers.append("painelcotações")
        triggers.append("paineldecotações")
        triggers.append("painel_cotações")
        triggers.append("cotação_dia")
        triggers.append("cotaçãoDia")
        return triggers

    def triggerspainelOrdensCompraVenda(self):
        triggers = []
        triggers.append("ordens_compravenda")
        triggers.append("compravenda")
        triggers.append("compraevenda")
        triggers.append("compra_venda")
        triggers.append("painelCompraVenda")
        triggers.append("painel_CompraVenda")
        triggers.append("painel_Ordens_CompraVenda")
        return triggers

    def triggersPainelOrdensExecutadas(self):
        triggers = []
        triggers.append("ordens_executadas")
        triggers.append("executadas")
        triggers.append("painelExecutadas")
        triggers.append("painelOrdensExecutadas")
        triggers.append("painel_OrdensExecutadas")
        triggers.append("painel_Ordens_Executadas")
        return triggers

    def triggersBotFuncionando(self):
        triggers = []
        triggers.append("funcionando?")
        triggers.append("você está funcionando?")
        triggers.append("vc está funcionando?")
        triggers.append("está funcionando?")
        return triggers

    def triggersBotAlguemAi(self):
        triggers = []
        triggers.append("Tem alguém ai?")
        triggers.append("alguém ai?")
        triggers.append("alguém ai??")
        triggers.append("alguém ai???")
        triggers.append("está ai?")
        triggers.append("você está ai?")
        return triggers

    def triggersBotDono(self):
        triggers = []
        triggers.append("a quem você pertênce?")
        triggers.append("Quem é seu dono?")
        triggers.append("Quem te desenvolveu?")
        return triggers

    def triggersBotSobre(self):
        triggers = []
        triggers.append("quem é você?")
        return triggers


    def painelAcoes(self):
        triggers = self.triggersPainelAcoes()
        if self.__verficaTriggers(triggers):
            self.__sc.rtm_send_message(Config.SLACK_MEMBERID, self.__nomeUsuario)
            Global.ws_Slack.postMessage(Config.SLACK_MEMBERID, Mensagens.Painel.acoes())

    def painelCotacao(self):
        triggers = self.triggersPainelCotacao()
        if self.__verficaTriggers(triggers):
            self.__sc.rtm_send_message(Config.SLACK_MEMBERID, self.__nomeUsuario)
            Estrategia.painelCotacaoMoeda(self.__bitcoin, self.__metodoColeta, self.__ws_MB)


    def painelOrdensCompraVenda(self):
        triggers = self.triggerspainelOrdensCompraVenda()
        if self.__verficaTriggers(triggers):
            self.__sc.rtm_send_message(Config.SLACK_MEMBERID, self.__nomeUsuario)
            Estrategia.painelOrdensCompraVenda(self.__bitcoin, self.__metodoColeta, self.__ws_MB)

    def painelOrdensExecutadas(self):
        triggers = self.triggersPainelOrdensExecutadas()
        if self.__verficaTriggers(triggers):
            self.__sc.rtm_send_message(Config.SLACK_MEMBERID, self.__nomeUsuario)
            Estrategia.painelOrdensExecutadas(self.__bitcoin, self.__metodoColeta, self.__ws_MB)


    def botFuncionando(self):
        triggers = self.triggersBotFuncionando()
        if self.__verficaTriggers(triggers):
            msgResposta = "{}, obrigado pela preocupação! {}".format(self.__nomeUsuario(), self.__dicaAcoes())
            self.__sc.rtm_send_message(Config.SLACK_MEMBERID, msgResposta)


    def botAlguemAi(self):
        triggers = self.triggersBotAlguemAi()
        if self.__verficaTriggers(triggers):
            msgResposta = "{}, estou sempre aqui! Posso ajudar? {} :crazy_parrot:".format(self.__nomeUsuario(), self.__dicaAcoes())
            self.__sc.rtm_send_message(Config.SLACK_MEMBERID, msgResposta)

    def botDono(self):
        triggers = self.triggersBotDono()
        if self.__verficaTriggers(triggers):
            msgResposta = "{}, sou livre! Porém, quem me criou foi o {}".format(self.__nomeUsuario(), Config.MAIN_USER.nome)
            self.__sc.rtm_send_message(Config.SLACK_MEMBERID, msgResposta)

    def botSobre(self):
        triggers = self.triggersBotSobre()
        if self.__verficaTriggers(triggers):
            msgResposta = "{}, meu nome é {}. Sou um robo para lhe ajudar com informações de Bitcoin.".format(self.__nomeUsuario(), Config.BOT_USER.nome)
            self.__sc.rtm_send_message(Config.SLACK_MEMBERID, msgResposta)

    def valorOrdens(self):
        triggers = self.triggersValorOrdens()
        if self.__verficaTriggers(triggers):
            msgResposta = "{}, as ordens monitoras estão com filtro para valores acima de {}".format(self.__nomeUsuario(), Util.formataDinheiro(Config.VALOR_ORDENS_MONITORADAS))
            self.__sc.rtm_send_message(Config.SLACK_MEMBERID, msgResposta)




    def __nomeUsuario(self):
        return "<@{}>".format(self.__user)


    def __dicaAcoes(self):
        return "Digite '#Ações' para mais informação."


    def __verficaTriggers(self, triggers):

        if self.__message is not None:
            message = Util.removerAcentos(self.__message)

            for trigger in triggers:
                trigger = format(Util.removerAcentos(trigger)).lower()

                if   message[0:5] == "bot, ": message = message[5:]
                elif message[0:4] == "bot," : message = message[5:]
                elif message[0:1] == "#"    : message = message[1:]

                if trigger == message:
                    return True


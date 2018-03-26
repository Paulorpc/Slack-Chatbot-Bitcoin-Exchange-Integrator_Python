# -*- coding: utf-8 -*-


from Moeda import Moeda
import WS as ws

class Global:
    bitcoin = Moeda("BITCOIN", "BTCBRL")
    ws_MB = ws.MercadoBitcoin
    ws_Slack = ws.Slack
    metodoColeta = ws.MetodoColetaDadosMB

    aOrdensExcutadas_old = []

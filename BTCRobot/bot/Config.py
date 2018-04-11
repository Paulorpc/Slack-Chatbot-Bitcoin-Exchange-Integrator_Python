# -*- coding: utf-8 -*-

import time
from enum import Enum
from Usuario import Usuario


class ICONS(Enum):
    slack      = "https://pixel21.com/wp-content/uploads/Slack-App-app-logo-png-300x250.png"
    pig        = "https://gdblogs.shu.ac.uk/b3017571/wp-content/uploads/sites/52/2015/05/piggy.png"
    futurama   = "http://www.iconeasy.com/icon/png/Movie%20%26%20TV/Futurama%20Vol.%204%20-%20The%20Robots/Fat%20Bot.png"
    coin1      = "https://maxcdn.icons8.com/office/PNG/512/Logos/bitcoin_80-512.png"
    coin2      = "https://apkplz.com/storage/images/com/bitcoinsgiver/300/bitcoinsgiver-free-bitcoin.png"
    smarti     = "https://www.smarti.blog.br/wp-content/uploads/2016/08/cropped-page_icon.jpg"
    robotface  = "http://d2trtkcohkrm90.cloudfront.net/images/emoji/apple/ios-10/256/robot-face.png"
    default    = "https://platform.slack-edge.com/img/default_application_icon.png"


class Config:

    DEBUG_MODE = False                          # Modo de depuração

    RTM_ATIVO = True                            # Ativa o loop de execução do RTM para ativação do bot
    WEBAPI_ATIVO = True                         # Ativa o loop de execução do WebAPI para envios dos posts de msgs

    timer_PainelCotacao_ATIVO = True            # Ativa o agendador (timer) para envio do painel de cotação moeda
    timer_OrdensCompraVenda_ATIVO = True        # Ativa o agendador (timer) para envio das ordens compra/venda
    timer_OrdensExecutadas_ATIVO = True         # Ativa o agendador (timer) para envio das ordens executadas


    # MERCADO BITCOIN WS API
    MB_TAPI_ID = ''
    MB_TAPI_SECRET = ''          # CODIGO DE USUÁRIO
    REQUEST_HOST = 'www.mercadobitcoin.net'

    PARANS = None
    TAPI_NONCE = str(int(time.time()))
    TAPI_METHOD = "trades"
    COIN_PAIR = "BRLBTC"


    ## ------------------------------------------------------------------------------------------------------------ ##


    #SLACK WS
    # TOKEN DE USUARIO PRINCIPAL
    __SLACK_TOKEN_CONEXAO = "" #Authentication RTM API / Use Legacy token generator to generate token
    __SLACK_TOKEN_MEMBER = ""
    MAIN_USER = Usuario("Paulo Cezar", "paulorpc@gmail.com", __SLACK_TOKEN_MEMBER, __SLACK_TOKEN_CONEXAO)

    # TOKEN DO BOT SLACK
    __SLACK_TOKEN_CONEXAO = "" #Slack API Token
    __SLACK_TOKEN_MEMBER = ""
    BOT_USER = Usuario("bbot", "paulorpc@gmail.com", __SLACK_TOKEN_MEMBER, __SLACK_TOKEN_CONEXAO)
    BOT_USER.addCanal("#btcbot")


    # BOTNAME = "BTC Bot"
    MAIN_CHANNEL = "#btcbot"
    DEBUG_CHANNEL = "#debug"
    # BOTICON = ICONS.coin2.value
    BOTICON = ICONS.robotface.value

    SLACK_MEMBERID = ""
    if not DEBUG_MODE: SLACK_MEMBERID = MAIN_CHANNEL
    else: SLACK_MEMBERID = DEBUG_CHANNEL

    IMAGE_URL = "http://my-website.com/path/to/image.jpg"
    THUMB_URL = "http://example.com/path/to/thumb.png"

    FOOTER = "www.smarti.blog.br"
    FOOTER_ICON = ICONS.smarti.value


    ## ------------------------------------------------------------------------------------------------------------ ##

    # ORDENS
    # Estipula o valor de insvestimento que deseja monitorar nas ordens (R$ >= ORDENS_MONITORADAS)
    VALOR_ORDENS_MONITORADAS = 30000
    # qtde da moeda acimna deste valor são marcados em negrito no painel
    QTDE_MOEDA_NEGRITO = 5

# -*- coding: utf-8 -*-

from Config import Config
from Util import Util
from Moeda import Moeda


class Painel:

    @staticmethod
    def cotacaoMoeda(moeda,
                     color       = "",
                     title       = "Cotação da Moeda - Painel de 24h",
                     title_link  = "https://www.mercadobitcoin.com.br/BRLBTC/negociacoes/",
                     image_url   = Config.IMAGE_URL,
                     thumb_url   = Config.THUMB_URL,
                     footer      = Config.FOOTER,
                     footer_icon = Config.FOOTER_ICON):

        lista = []
        if not isinstance(moeda, Moeda):
            raise "MOEDA DEVE SER INSTANCIA DE COTAÇÃO"

        structuredMsg = {
            "fallback": "Required plain-text summary of the attachment.",
            "color": color,
            "title": title,
            "title_link": title_link,
            "fields": [
                {
                    "title": "Maior Valor",
                    "value": Util.formataDinheiro(moeda.cotacaoDia.precoMax),
                    "short": True
                },
                {
                    "title": "Menor Valor",
                    "value": Util.formataDinheiro(moeda.cotacaoDia.precoMin),
                    "short": True
                },
                {
                    "title": "Maior oferta (compra)",
                    "value": Util.formataDinheiro(moeda.cotacaoDia.precoMaiorOfeCompra),
                    "short": True
                },
                {
                    "title": "Menor oferta (venda)",
                    "value": Util.formataDinheiro(moeda.cotacaoDia.precoMenorOfeVenda),
                    "short": True
                },
                {
                    "title": "Volume Negociado",
                    "value": Util.formataQtde(moeda.cotacaoDia.volume, 2) + " BTC",
                    "short": True
                },
                {
                    "title": "Valor do úlitmo negócio",
                    "value": Util.formataDinheiro(moeda.cotacaoDia.precoUltimaNegociacao),
                    "short": True
                },
                # {
                #     "title": "Variação do Dia",
                #     "value": Util.formataPercentual(moeda.cotacaoDia.variacaoDia('perc')),
                #     "short": True
                # },
                # {
                #     "title": "Variação últ. 7 dias",
                #     "value": Util.formataPercentual(moeda.cotacaoDia.variacaoSemana('perc')),
                #     "short": True
                # },
                {
                    "title": "Monitoramento de Ordens",
                    "value": "Acima de " + Util.formataDinheiro(Config.VALOR_ORDENS_MONITORADAS),
                    "short": True
                },
            ],
            "mrkdwn_in": ["pretext", "text", "fields"],
            "mrkdwn": True,
            "image_url": image_url,
            "thumb_url": thumb_url,
            "footer": footer,
            "footer_icon": footer_icon
        }
        lista.append(structuredMsg)
        return lista


    @staticmethod
    def ordensCompraVenda(moeda,
                          ordensCompra,
                          ordensVenda,
                          color       = "",
                          title       = "Ordens de Compra/Venda - Painel de Negocioações",
                          title_link  = "https://www.mercadobitcoin.com.br/BRLBTC/negociacoes/",
                          image_url   = Config.IMAGE_URL,
                          thumb_url   = Config.THUMB_URL,
                          footer      = Config.FOOTER,
                          footer_icon = Config.FOOTER_ICON):

        lista = []
        if not isinstance(moeda, Moeda):
            raise "MOEDA DEVE SER INSTANCIA DE Moeda"

        structuredMsg = {
            "fallback": "Required plain-text summary of the attachment.",
            "color": color,
            "title": title,
            "title_link": title_link,
            "pretext": Painel.barraSuperiorInfo(moeda),
            "fields": [
                {
                    "title": "Ordens de Compra",
                    "value": ordensCompra,
                    "short": True
                },
                {
                    "title": "Ordens de Venda",
                    "value": ordensVenda,
                    "short": True
                }

            ],
            "mrkdwn_in": ["pretext", "text", "fields"],
            "mrkdwn": True,
            "image_url": image_url,
            "thumb_url": thumb_url,
            "footer": footer,
            "footer_icon": footer_icon
        }
        lista.append(structuredMsg)
        return lista


    @staticmethod
    def ordensExecutadas(moeda,
                         ordensCompra,
                         ordensVenda,
                         color       = "",
                         title       = "Ordens Executadas - Painel de Negocioações",
                         title_link  = "https://www.mercadobitcoin.com.br/BRLBTC/negociacoes/",
                         image_url   = Config.IMAGE_URL,
                         thumb_url   = Config.THUMB_URL,
                         footer      = Config.FOOTER,
                         footer_icon = Config.FOOTER_ICON):

        lista = []
        if not isinstance(moeda, Moeda):
            raise "MOEDA DEVE SER INSTANCIA DE COTAÇÃO"

        structuredMsg = {
            "fallback": "Required plain-text summary of the attachment.",
            "color": color,
            "title": title,
            "title_link": title_link,
            "pretext": Painel.barraSuperiorInfo(moeda),
            "fields": [
                {
                    "title": "Ordens de Compra",
                    "value": ordensCompra,
                    "short": True
                },
                {
                    "title": "Ordens de Venda",
                    "value": ordensVenda,
                    "short": True
                }

            ],
            "mrkdwn_in": ["pretext", "text", "fields"],
            "mrkdwn": True,
            "image_url": image_url,
            "thumb_url": thumb_url,
            "footer": footer,
            "footer_icon": footer_icon
        }
        lista.append(structuredMsg)
        return lista

    @staticmethod
    def acoes(color="",
              title="Ações de Solicitação ao {}" .format(Config.BOT_USER.nome),
              title_link="https://www.mercadobitcoin.com.br/BRLBTC/negociacoes/",
              image_url=Config.IMAGE_URL,
              thumb_url=Config.THUMB_URL,
              footer=Config.FOOTER,
              footer_icon=Config.FOOTER_ICON):

        lista = []
        structuredMsg = {
            "fallback": "Required plain-text summary of the attachment.",
            "color": color,
            "title": title,
            "title_link": title_link,
            "fields": [
                {
                    "title": "Painel de Cotação",
                    "value": Painel.listaDestaqueSlack("painelcotação, painelcotações, cotaçãoDia"),
                    "short": False
                },
                {
                    "title": "Ordens de Compra/Venda",
                    "value": Painel.listaDestaqueSlack("painelCompraVenda, compravenda, ordens_compravenda"),
                    "short": False
                },
                {
                    "title": "Ordens Executadas",
                    "value": Painel.listaDestaqueSlack("painelExecutadas, executadas, ordens_executadas"),
                    "short": False
                },
                {
                    "title": "Filtros",
                    "value": Painel.listaDestaqueSlack("filtros, filtrosOrdens, filtrosValor"),
                    "short": False
                }
            ],
            "mrkdwn_in": ["pretext", "text", "fields"],
            "mrkdwn": True,
            "image_url": image_url,
            "thumb_url": thumb_url,
            "footer": footer,
            "footer_icon": footer_icon
        }
        lista.append(structuredMsg)
        return lista


    @staticmethod
    def barraSuperiorInfo(moeda):
        return "Últ: " + Util.destaqueSlack( Util.formataDinheiro(moeda.cotacaoDia.precoUltimaNegociacao) ) \
          + "   Max: " + Util.destaqueSlack( Util.formataDinheiro(moeda.cotacaoDia.precoMax) ) \
          + "   Min: " + Util.destaqueSlack( Util.formataDinheiro(moeda.cotacaoDia.precoMin) ) \
          + "   Vol: " + Util.destaqueSlack( Util.formataQtde(moeda.cotacaoDia.volume, 2) + " BTC" ) #\
          #+ "   Var: " + Util.destaqueSlack( Util.formataPercentual(moeda.cotacaoDia.variacaoDia('%')) )


    @staticmethod
    def listaDestaqueSlack(texto):
        keys = texto.split(",")
        saida = ""
        for item in keys:
            item = Util.destaqueSlack(Util.hashtag(item.strip()))
            saida += item + ", "

        return saida[:-2]
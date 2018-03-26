# -*- coding: utf-8 -*-


from datetime import datetime, time
from datetime import timedelta
import locale
from enum import Enum
from unicodedata import normalize


class Tempo(Enum):
    SEG = 1
    MIN = 60 * SEG
    HORA = 60 * MIN



class DataHora():

    # a = DataHora.hoje()
    # b = DataHora.hora()
    # c = DataHora.hojeHora()
    # d = DataHora.formataData(DataHora.hojeHora())
    # e = DataHora.formataHora(DataHora.hojeHora())
    # f = DataHora.formataDataHora(DataHora.hojeHora())
    # soma = DataHora.somaHora(DataHora.hora(), 1*Time.HORA.value)

    @staticmethod
    def hora():
        return datetime.now().time().replace(microsecond=0)

    @staticmethod
    def hoje():
        return datetime.now().date()

    @staticmethod
    def hojeHora():
        return datetime.now().replace(microsecond=0)

    @staticmethod
    def formataData(dataHora):

        if isinstance(dataHora, str):
            data = datetime.fromtimestamp(int(dataHora)).strftime('%d/%m/%Y %H:%M')
        else:
            data = dataHora.strftime('%d/%m/%y')

        return data

    @staticmethod
    def formataHora(dataHora):
        return dataHora.strftime('%H:%M')

    @staticmethod
    def formataDataHora(dataHora):

        if isinstance(dataHora, datetime):
            dataHora = dataHora.strftime('%d/%m/%y %H:%M')
        elif isinstance(dataHora, int):
            dataHora = datetime.fromtimestamp(dataHora).strftime('%d/%m/%Y %H:%M')

        return dataHora

    @staticmethod
    def somaHora(hora, deltaSeg):

        if isinstance(hora, time):
            hora = datetime(2000, 1, 1, hour=hora.hour, minute=hora.minute, second=hora.second)

        hora = hora + timedelta(seconds=deltaSeg)
        # hora = hora.time()
        return hora




class Util:

    @staticmethod
    def formataQtde(qtde, digitos=5):

        if not isinstance(digitos, int):
            raise "paramentro 'digitos' para método 'formataQtde' deve ser do tipo int ou int"

        qtde = Util.__doubleToString(round(qtde, digitos), digitos).replace(".", ",")
        return qtde

    @staticmethod
    def formataDinheiro(valor, simbolo="R$"):

        if not isinstance(valor, int) and not isinstance(valor, float):
            raise "paramentro 'valor' para método 'formataDinheiro' deve ser do tipo int ou float"

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        valor = locale.currency(valor, grouping=True, symbol=simbolo)

        return valor

    @staticmethod
    def formataPercentual(valor, digitos=2):
        if isinstance(digitos, int):
            var = "%0." + str(digitos) + "f"
            return var % valor + " %"
        return -1



    @staticmethod
    def __doubleToString(valor, digitos):
        if isinstance(digitos, int):
            var = "%0." + str(digitos) + "f"
            return var % valor
        return -1

    @staticmethod
    def unicodeToUtf8(texto, toLower=False, toUpper=False):
        if isinstance(texto, unicode):
            texto = texto.encode("utf-8")

            if toLower is True:
                texto = texto.lower()
            elif toUpper is True:
                texto = texto.upper()

        return texto

    @staticmethod
    def removerAcentos(txt, codif='utf-8'):
        return normalize('NFKD', txt.decode(codif)).encode('ASCII', 'ignore')


    @staticmethod
    def destaqueSlack(msg):
        return "`{}`".format(msg)

    @staticmethod
    def hashtag(msg):
        return "#{}".format(msg)





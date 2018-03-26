# -*- coding: utf-8 -*-


class Usuario:

    def __init__(self, nome, email, slack_MemberID, slackTokenID):
        self._nome = nome
        self._slack_MemberID = slack_MemberID
        self._slack_tokenID = slackTokenID
        self._mb_userToken = None
        self._mb_user = False
        self._emails = []
        self._canais = []

        self._emails.append(email)


    @property
    def nome(self):
        return self._nome

    @property
    def slack_MemberID(self):
        return self._slack_MemberID

    @property
    def slack_tokenID(self):
        return self._slack_tokenID

    @property
    def mb_userToken(self):
        return self._mb_userToken

    @mb_userToken.setter
    def mb_userToken(self, token):
        self._mb_userToken = token
        self._mb_user = True

    @property
    def mb_user(self):
        return self._mb_user

    def emails(self):
        if len(self._emails) > 1:
            return self._emails
        elif len(self._emails) == 1:
            return self._emails[0]
        else:
            return None

    def addEmails(self, value):
        self._emails.append(value)

    def canais(self):
        if len(self._canais) > 1:
            return self._canais
        elif len(self._canais) > 0:
            return self._canais[0]
        else:
            return None

    def addCanal(self, canal):
        self._canais.append(canal)


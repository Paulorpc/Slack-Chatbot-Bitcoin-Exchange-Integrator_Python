# Slack-Chatbot-Bitcoin-Exchange-Integrator_Python
A Slack's ChatBot that collects data from a Exchange's Webservice and display information to the user/channel.

This primary version was built to work with Bitcoin, connecting to Mercado Bitcoin Exchange only. The idea is to evaluate it to work with distinct cryptocurrencys and exchanges.

To concentrate forces in the bot strategy that sends requested data from the exchange to the slack's users and channels, was used an Slack's client API for python. You must set it up properly to get the bot started. Furthermore, you also need to create your mercado bitcoin and slack account and create your bot into slack's account. Your account's information (tokens and ids) must be used to "fill" the variable in the config.py file. 

#### To get more information about:
> - __slackclient for python__, see **README.md** into python-slackclient folder, or [click here](https://github.com/Paulorpc/Slack-Chatbot-Bitcoin-Exchange-Integrator_Python/tree/master/BTCRobot/python-slackclient)
> - **Slack Bot User API**, [click here](https://api.slack.com/bot-users)
> - **Mercado Bitcoin API**, [click here](https://www.mercadobitcoin.com.br/api-doc/)

## Config.py setup variables.
#### Exchange Web Service API user connection - Mercado Bitcoin
```
MB_TAPI_ID
MB_TAPI_SECRET
```
#### Main user's tokens from Mercado Bitcoin and Slack
```
__SLACK_TOKEN_CONEXAO
__SLACK_TOKEN_MEMBER
```

#### Slacks's chabot user Token
```
__SLACK_TOKEN_CONEXAO
__SLACK_TOKEN_MEMBER
```

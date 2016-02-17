import bottom
from parser import Chat, Payload, PayloadType, Commands

host = 'chat.freenode.net'
port = 6697
ssl = True

client = bottom.Client(host=host, port=port, ssl=ssl)


class Pybot:
    def __init__(self, nick, channels, server, password):
        self.nick = nick
        self.channels = channels
        self.server = server
        self.password = password

bot = Pybot(
    nick='Omnius',
    channels=['#omnius'],
    server='chat.freenode.net',
    password='botomnius',
)

chat = Chat()

@client.on('CLIENT_DISCONNECT')
async def reconnect(**kwargs):
    ## Todo: add in a reconnect handler when disconnect detected
    print('Disconnected')
    client.trigger('reconnect')

    client.loop.create_task(client.connect())

    await client.wait('CLIENT_CONNECT')


@client.on('CLIENT_CONNECT')
def connect(**kwargs):
    print(kwargs)
    client.send('NICK', nick=bot.nick)
    client.send('USER', user=bot.nick, realname='PyBot')
    client.send('PRIVMSG', target='nickserv',
                message='identify {}'.format(bot.password))
    client.send('JOIN', channel=bot.channels)


@client.on('PING')
def keepalive(message, **kwargs):
    print(message)
    client.send('PONG', message=message)


@client.on('PRIVMSG')
async def message(nick, target, message, **kwargs):
    print("{}: {}".format(nick, message))
    if nick == bot.nick:
        return
    else:
        payload = await chat.parse(msg=message, target=target, invoker=nick)

    if payload.payloadType == PayloadType.CHAT_MESSAGE:
        if payload.target == None:
            if target == bot.nick:
                payload.target = nick
            else:
                payload.target = target
        if '\n' in payload.response:
            lines = payload.response.split('\n')
        else:
            lines = [payload.response]
        for line in lines:
            client.send(
                'PRIVMSG',
                target=payload.target,
                message=line,
            )


client.loop.create_task(client.connect())
client.loop.run_forever()

from utils.console import Console
import discord
from utils import handleJson
SHL = Console("BundestagsBot Sub")

settings = {
    'name': 'sub',
    'channels': ['dm', 'bot'],
}

path = 'C:/server/settings/BoB/surveys.json'


async def main(client, message, params):

    if len(str(message.content).split(' ')) == 2:
        sub = str(message.content).split(' ')[1]
        if sub.lower() in ['yes', 'no', 'ja', 'nein', 'true', 'false']:
            if ['yes', 'no', 'ja', 'nein', 'true', 'false'].index(sub.lower()) % 2 == 0:  # resubs
                subs(True, message.author.id)
                await message.channel.send(content='Done.')
            else:  # unsubs
                subs(False, message.author.id)
                await message.channel.send(content='Done.\nDu kannst die Umfragen wieder abonnieren mit >sub True')
        else:
            await message.channel.send(content='Ungültiges Argument. Verwende: >sub True|False')
    else:
        await message.channel.send(content='Ungültige Anzahl an Argumenten. Verwende: >sub True|False')


def subs(sub, user_id):
    data = handleJson.readjson(path)
    if sub:
        if user_id in data["unsubs"]:
            data["unsubs"].remove(user_id)
    else:
        if user_id not in data["unsubs"]:
            data["unsubs"].append(user_id)

    handleJson.saveasjson(path, data)

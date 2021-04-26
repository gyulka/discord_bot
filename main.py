import discord
import requests
from io import BytesIO
import asyncio
import random


class Arg_err(Exception):
    pass


headers = {"X-Yandex-API-Key": '40d1649f-0493-4b70-98ba-98533de7710b'}


def translate(string, leng):
    querystring = {"langpair": leng, "q": string, "mt": "1", "onlyprivate": "0", "de": "a@b.c"}

    headers = {
        'x-rapidapi-key': "07daa3c1fbmsh732ac5123b0dea6p1ec0d7jsnafa63c1212b6",
        'x-rapidapi-host': "translated-mymemory---translation-memory.p.rapidapi.com"
    }
    url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()['responseData']['translatedText']


class Bot(discord.Client):
    language = 'ru'

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == '!help':
            await message.channel.send('''
!set_lang - Сменить язык
!text - Перевод текста''')

        if message.content.startswith('!set_lang'):  # Смена языка
            lang = '|'.join(str(message.content).split()[1].split('-'))
            if Bot.language not in ['en', 'ru']:
                await message.channel.send('Что-то хз что')
            else:
                Bot.language = lang
                await message.channel.send(f'Язык вывода сменен на {Bot.language}')

        if message.content.startswith('!text'):  # Текст
            args = str(message.content).lstrip('!text')
            await message.channel.send(translate(args, Bot.language))


TOKEN = 'ODM1OTgzMjY0NzQwNTQwNDY2.YIXYFg.pbBz6d-ZoRWTinFGN_Xrk69LH1g'

client = Bot()
client.run(TOKEN)

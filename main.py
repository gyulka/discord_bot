import discord
import requests
from io import BytesIO
import asyncio

import pymorphy2


class Arg_err(Exception):
    pass


class YLBotClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            print(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')

    async def on_message(self, message):
        if message.author == self.user:
            return

        elif 'help' in str(message.content).lower():
            await message.channel.send('#!collocation Согласовывание слова с числительными' \
                                       'Определить, живое ли существительное или нет' \
                                       'Изменить существительное в соответствии с введенным падежом и числом' \
                                       'Начальная форма существительного' \
                                       'Морфологический анализ слова, для которого параметр score максимальный')

        elif message.content.startswith('#!infinitive'):
            args = str(message.content).split()
            try:
                if len(args) != 2:
                    raise Arg_err
                else:
                    await message.channel.send(pymorphy2.MorphAnalyzer().parse(args[-1])[0].normal_form)

            except Arg_err:
                await message.channel.send('Неверное количество аргументов!')

        elif message.content.startswith('#!alive'):
            args = str(message.content).split()
            try:
                if len(args) != 2:
                    raise Arg_err
                else:
                    word = pymorphy2.MorphAnalyzer().parse(args[-1])[0]
                    if word.tag.animacy == 'anim':
                        if word.tag.number in {'plur'}:
                            await message.channel.send('Живые')
                        else:
                            if word.tag.gender in 'masc':
                                await message.channel.send(f'{word.word} - Живой')
                            elif word.tag.gender in 'femn':
                                await message.channel.send(f'{word.word} - Живая')
                            else:
                                await message.channel.send(f'{word.word} - Живое')
                    else:
                        if word.tag.number in {'plur'}:
                            await message.channel.send('Не живые')
                        else:
                            if word.tag.gender in 'masc':
                                await message.channel.send(f'{word.word} - Не живой')
                            elif word.tag.gender in 'femn':
                                await message.channel.send(f'{word.word} - Не живая')
                            else:
                                await message.channel.send(f'{word.word} - Не живое')
            except Arg_err:
                await message.channel.send('Неверное количество аргументов!')

        elif message.content.startswith('#!change'):
            args = str(message.content).split()
            try:
                if len(args) != 4:
                    raise Arg_err
                else:
                    word = pymorphy2.MorphAnalyzer().parse(args[-3])[0]
                    await message.channel.send(word.inflect({args[-2], args[-1]}).word)
            except Arg_err:
                await message.channel.send('Неверное количество аргументов!')

        elif message.content.startswith('#!collocation'):
            args = str(message.content).split()
            try:
                if len(args) != 3:
                    raise Arg_err
                else:
                    word = pymorphy2.MorphAnalyzer().parse(args[1])[0]
                    await message.channel.send(f'{args[-1]} {word.make_agree_with_number(int(args[-1])).word}.')
            except Arg_err:
                await message.channel.send('Неверное количество аргументов!')

            except ValueError:
                await message.channel.send('Неверный тип аргументов!')

        elif message.content.startswith('#!morfol'):
            args = str(message.content).lstrip('#!morfol ')
            max_score = 0
            for word in args.split():
                if max_score < pymorphy2.MorphAnalyzer().parse(word)[0].score:
                    max_score = pymorphy2.MorphAnalyzer().parse(word)[0].score
            for word in args.split():
                if pymorphy2.MorphAnalyzer().parse(word)[0].score == max_score:
                    await message.channel.send(f'{word}: {pymorphy2.MorphAnalyzer().parse(word)[0].tag}')


TOKEN = 'ODM1OTgzMjY0NzQwNTQwNDY2.YIXYFg.pbBz6d-ZoRWTinFGN_Xrk69LH1g'

client = YLBotClient()
client.run(TOKEN)

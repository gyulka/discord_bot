import discord
import requests
from io import BytesIO
import asyncio
import random


class Arg_err(Exception):
    pass


users = 0
bots = 0
bot = discord.Client()
emoji = ['🛁', '🚴', '🚀', '🚁', '🚂', '🚃', '🚌', '🚎', '🚑', '🚒', '🚓', '🦆', '🚕', '🦚', '🦞', '🚗',
         '🦑', '🚚', '🦢', '🦟', '🦠', '🦅', '🦀', '🦗', '🦋', '🚜', '🦇', '🦔', '🦓', '🚣', '🦒', '🦎',
         '🚶', '🛌', '🛒', '🛩', '🛰', '🛸', '🤔', '🤐', '🤓', '🤡', '🤫', '🥐', '🥕', '🥝', '🥦', '🥾']


@bot.event
async def on_message(self, message):
    global users, bots
    random.shuffle(emoji)
    if message.author == self.user:
        return
    if message.content == '/start' or message.content == '/help' :
        await message.channel.send(f'играйте же в игру"')
    elif message.content == '/stop':
        users = 0
        bots = 0
        await message.channel.send('Buy')
    else:
        try:
            if emoji:
                card = int(message.content)
                user_turn = emoji.pop(card % len(emoji))
                bot_turn = emoji.pop(random.randint(0, 100) % len(emoji))
                if user_turn > bot_turn:
                    users += 1
                else:
                    bots += 1
                await message.channel.send(f'Your emoji {user_turn}\nBot emoji {bot_turn}\n'
                                           f'Score: You {users} - Bot {bots}')
            else:
                raise IndexError
        except IndexError:
            if users > bots:
                await message.channel.send(f'Emoticons are over\nScore: You {users} - Bot {bots}\n'
                                           f'You win!')
            elif users < bots:
                await message.channel.send(f'Emoticons are over\nScore: You {users} - Bot {bots}\n'
                                           f'Bot win!')
            else:
                await message.channel.send(f'Emoticons are over\nScore: You {users} - Bot {bots}\n'
                                           f'Draw result!')
        except Exception as error:
            print(error.__str__(), message.content)
            await message.channel.send('error')


TOKEN = 'ODM1OTgzMjY0NzQwNTQwNDY2.YIXYFg.pbBz6d-ZoRWTinFGN_Xrk69LH1g'


bot.run(TOKEN)

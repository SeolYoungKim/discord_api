import discord
from discord.ext import commands
from random import *
import requests
from bs4 import BeautifulSoup
import numpy as np
import asyncio


discord_token = 'OTQ4NTI4MTE0ODk4NzE4NzYy.Yh9HpQ.wT_-XiUc0IvWZu-hn-BnypRnbJs'

# discord Client class를 생성합니다.
client = commands.Bot(command_prefix='!')


@client.event   # event decorator를 설정하고 on_ready function을 할당해줍니다.
async def on_ready():  # on_ready event는 discord bot이 discord에 정상적으로 접속했을 때 실행됩니다.
    print('We have logged in as {}'.format(client))
    print('Bot name: {}'.format(client.user.name))  # 여기서 client.user는 discord bot을 의미합니다. (제가 아닙니다.)
    print('Bot ID: {}'.format(client.user.id))  # 여기서 client.user는 discord bot을 의미합니다. (제가 아닙니다.)


@client.command(name='주사위')
async def roll(ctx, number):
    await ctx.send('1 ~ {} 사이의 주사위를 돌립니다.'.format(number))

    result_number = np.random.randint(1, int(number)+1)
    await ctx.send('결과 = {}'.format(result_number))


@roll.error
async def roll_error(ctx, error):
    await ctx.send('잘못입력하셨습니다. \n!근아? 를 입력해서 사용법을 확인하세요.'.format(str(error)))


# @client.event   # event decorator를 설정하고 on_message function을 할당해줍니다.
# async def on_message(message):
#     # message란 discord 채널에 올라오는 모든 message를 의미합니다.
#     # 따라서 bot이 보낸 message도 포함이되죠.
#     # 아래 조건은 message의 author가 bot(=clinet.user)이라면 그냥 return으로 무시하라는 뜻입니다.
#     if message.author == client.user:
#         return
#
#     # message를 보낸 사람이 bot이 아니라면 message가 hello로 시작하는 경우 채널에 Hello!라는 글자를 보내라는 뜻입니다.
#     elif message.content.startswith('안녕'):
#         await message.channel.send('제가 김근아(짱깨) 입니다.')
#
#     elif message.content.startswith('!강화'):
#         await message.channel.send('강화 성공 확률은 {}% 입니다.'.format(randint(0, 100)))

@client.command(aliases=['강화'])
async def reinforce_prob(ctx):
    await ctx.send('강화 성공 확률은 {}% 입니다.'.format(randint(0, 100)))


@client.command(aliases=['야', '안녕'])
async def hi_kga(ctx):
    await ctx.send('제가 김근아(짱깨) 입니다.')


@client.command(aliases=['사사게'])
async def crwal(ctx):
    url = "https://www.inven.co.kr/board/lostark/5355?my=chu"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "lxml")

    titles = soup.find_all("div", attrs={"class": "text-wrap"})

    title = []
    link = []
    for item in titles:
        title.append(item.find("a", attrs={"class": "subject-link"}).get_text())
        link.append(item.find("a")["href"])

    embed = discord.Embed(title="사사게 현황", description="싸움구경 개꿀잼", color=0x005666)
    embed.add_field(
        name="일간 사사게_1",
        value=f"제목: {title[0]},\n 링크: {link[0]}",
        inline=False
    )

    embed.add_field(
        name="일간 사사게_2",
        value=f"제목: {title[1]},\n 링크: {link[2]}",
        inline=False
    )

    await ctx.send(embed=embed)


@client.command(name='근아?')
async def introduce_commands(ctx):
    dict_commands = {
        'roll': '!주사위 [2이상의 정수만.. 제발 오류나요] (e.g. !주사위 5 또는 !주사위 10)',
    }

    for k, v in dict_commands.items():
        await ctx.send('{}'.format(v))


# 위에서 설정한 client class를 token으로 인증하여 실행합니다.
client.run(discord_token)


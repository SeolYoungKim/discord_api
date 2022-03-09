import discord
from discord.ext import commands
from random import *
import requests
from bs4 import BeautifulSoup
import numpy as np
import asyncio
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


# discord Client class를 생성합니다.
client = commands.Bot(command_prefix='!')

bad_word = []
with open('fword_list.txt', 'r', encoding='utf8') as f:
    f_word = f.readlines()
    for fw in f_word:
        bad_word.append(fw.strip())

print(bad_word)


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
    await ctx.send('잘못입력하셨습니다. \n!사용법 을 입력해서 사용법을 확인하세요.'.format(str(error)))


def create_soup(url):
    my_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}

    res = requests.get(url, headers=my_header)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")

    return soup


def create_browser():
    options = webdriver.ChromeOptions()
    # 주석으로 된 구문은 heroku 구동 시 추가해준다.
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.headless = True
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/98.0.4758.102 Safari/537.36")

    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)

    return browser


@client.command(name='롤')
async def lol_info(ctx):
    msg = ctx.message.content.replace('!롤', '')
    user_id = msg.replace(' ', '')
    url = "https://www.op.gg/" + f"summoners/kr/{user_id}"
    soup = create_soup(url)

    # 유저 랭크 : 언랭일 때, 언랭인데 자랭이 있을 때 어떻게 할 지 작업
    rank_info = soup.find("div", attrs={"class": "tier-rank"}).get_text().upper()
    win_lose_info = soup.find("span", attrs={"class": "win-lose"}).get_text()[:-12]
    win_lose_prob = soup.find("span", attrs={"class": "win-lose"}).get_text()[-12:]
    most_chp_name = soup.find("div", attrs={"class": "name"}).find("a").get_text()
    most_chp_kda = soup.find("div", attrs={"class": re.compile("exxtup1$")}).get_text()[:-4]
    most_chp_prob = soup.find("div", attrs={"class": re.compile("exxtup0$")}).get_text()

    img = soup.find("div", attrs={"class": "medal"}).find("img")["src"]

    embed = discord.Embed(title=f"{user_id}님의 플레이어 정보", color=0x005666)
    embed.add_field(name="티어 정보", value=f"`{rank_info} | {win_lose_info} ({win_lose_prob})`", inline=False)
    embed.add_field(name="모스트 챔피언", value=f"`{most_chp_name} | {most_chp_kda} | {most_chp_prob}`", inline=False)
    embed.set_thumbnail(url=img)

    await ctx.send(embed=embed)


@client.command(aliases=['가위', '바위', '보'])
async def rock_sissor_paper(ctx):
    msg = ctx.message.content

    if msg == '!가위' or msg == '!바위' or msg == '!보':
        random_ = randint(1, 3)

        if random_ == 1:  # random 에 저장된 변수가 1일때 (가위 일때)
            if msg == "!가위":
                await ctx.send("가위!")
                await ctx.send("비겼습니다.")

            elif msg == "!바위":
                await ctx.send("가위!")
                await ctx.send("그래 내가 졌다.")

            else:
                await ctx.send("가위!")
                await ctx.send("이것도 못이기죠? 너~무쉽죠?")

        if random_ == 2:  # random 에 저장된 변수가 2일때 (바위 일때)
            if msg == "!가위":
                await ctx.send("바위!")
                await ctx.send("응애~ 베리 EZ 하죠?")

            elif msg == "!바위":
                await ctx.send("바위!")
                await ctx.send("비겼습니다.")

            else:
                await ctx.send("바위!")
                await ctx.send("제가 졌습니다.")

        if random_ == 3:  # random 에 저장된 변수가 3일때 (보 일때)
            if msg == "!가위":
                await ctx.send("보!")
                await ctx.send("제가 졌습니다.")

            elif msg == "!바위":
                await ctx.send("보!")
                await ctx.send("쉽다 쉬워~ 나가~~~!")

            else:
                await ctx.send("보!")
                await ctx.send("비겼습니다.")


@client.command(name='운세')
async def lucky(ctx):
    msg = ctx.message.content.split()
    gender = msg[1]
    birth = msg[2]

    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1" \
          "&ie=utf8&query=%EC%98%A4%EB%8A%98%EC%9D%98+%EC%9A%B4%EC%84%B8"

    browser = create_browser()
    browser.maximize_window()
    browser.get(url)

    time.sleep(1)
    if gender == "여자":
        browser.find_element(by=By.XPATH,
                             value='//*[@id="fortune_birthCondition"]/div[1]/fieldset/div[1]/span[2]/a').click()

    time.sleep(1)
    browser.find_element(by=By.XPATH,
                         value='//*[@id="srch_txt"]').click()
    time.sleep(1)
    browser.find_element(by=By.CLASS_NAME, value='srch_txt').send_keys(birth)

    time.sleep(1)
    browser.find_element(by=By.XPATH,
                         value='//*[@id="fortune_birthCondition"]/div[1]/fieldset/input').click()
    time.sleep(1)
    browser.find_element(by=By.XPATH,
                         value='//*[@id="fortune_birthResult"]/ul[2]/li[3]/a').click()

    soup = BeautifulSoup(browser.page_source, "lxml")

    luck = soup.find("dl", attrs={"class": "infor _luckText v2"}).get_text()

    embed = discord.Embed(title="오늘의 금전운", color=0x005666)
    embed.add_field(name="금전운", value=f"`{luck}`", inline=False)

    await ctx.send(embed=embed)


@client.command(aliases=['날씨'])
async def scrape_weather(ctx):

    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty\
    &fbm=1&ie=utf8&query=%EC%88%98%EC%9B%90+%EB%82%A0%EC%94%A8"

    soup = create_soup(url)

    # 오늘 날씨 요약
    today_weather = soup.find("p", attrs={"class": "summary"}).get_text()[-3:]
    compare_with_yesterday = soup.find("p", attrs={"class": "summary"}).get_text()[:-3]

    # 기온
    curr_temp = soup.find("div", attrs={"class": "temperature_text"}).get_text()
    min_temp = soup.find("span", attrs={"class": "lowest"}).get_text()  # 최저 온도
    max_temp = soup.find("span", attrs={"class": "highest"}).get_text()  # 최고 온도

    # 미세먼지
    today_items = soup.find_all("li", attrs={"class": re.compile("^item_today")})
    fine_dust = today_items[0].get_text().strip()
    ultrafine_dust = today_items[1].get_text().strip()

    embed = discord.Embed(title="오늘의 날씨", description="응~안나가면 그만이야~", color=0x005666)
    embed.add_field(
        name="날씨 요약",
        value=f"{today_weather}, {compare_with_yesterday}",
        inline=False
    )
    embed.add_field(
        name="날씨 상세",
        value=f"기온: {curr_temp} ({min_temp} / {max_temp}), \n대기 상태: {fine_dust} / {ultrafine_dust}",
        inline=False
    )

    await ctx.send(embed=embed)


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


geuna_info = {
    '김근아': None
}


@client.command(name='김근아')
async def geuna_(ctx):
    msg = ctx.message.content.split()
    target_msg = msg[1]
    author_name = ctx.message.author.name
    author_id = ctx.message.author.id

    # print(author, type(author))
    # print(author_id, type(author_id))

    global geuna_info
    global bad_word

    if target_msg == '초기화' and author_id == 426341928725118977:
        geuna_info['김근아'] = None
    else:
        if target_msg:
            if target_msg not in bad_word:
                if len(target_msg) < 10 and target_msg != '초기화':
                    if geuna_info['김근아'] is None:
                        geuna_info['김근아'] = target_msg
                    else:
                        if target_msg not in geuna_info['김근아']:
                            target_msg = ", " + msg[1]
                            geuna_info['김근아'] += target_msg

                geuna_keyword = str(geuna_info['김근아'])
                notice = f'김근아 님은 {geuna_keyword}입니다.'

                await ctx.send(notice)

            else:
                await ctx.send(f'{author_name} = {target_msg} \n욕설은 추가되지 않습니다.')


@client.command(name='사용법')
async def introduce_commands(ctx):
    embed = discord.Embed(title="기능 안내", description="기능 및 명령어 안내", color=0x005666)
    embed.add_field(name="인사하기", value="`!야 or !안녕`", inline=True)
    embed.add_field(name="강화 운 보기", value="`!강화`", inline=True)
    embed.add_field(name="사사게 염탐", value="`!사사게`", inline=True)
    embed.add_field(name="주사위 굴리기", value="`!주사위 (숫자)`", inline=True)
    embed.add_field(name="오늘의 날씨", value="`!날씨`", inline=True)
    embed.add_field(name="가위바위보", value="`!가위/!바위/!보`", inline=True)
    embed.add_field(name="롤 전적 검색", value="`!롤 (닉네임)`", inline=True)
    embed.add_field(name="오늘의 운세", value="`!운세 성별 생년월일(8자리)`", inline=True)
    embed.add_field(name="김근아 정보", value="`!김근아 10글자 미만 단어`", inline=True)
    # embed.set_thumbnail(url="https://image.fmkorea.com/files/attach/new2/20211226/44021718/2973985274/4196305521/6846842362dde48a0087207e49a2dcff.jpg")
    embed.set_image(url="https://image.fmkorea.com/files/attach/new2/20211226/44021718/2973985274/"
                        "4196305521/6846842362dde48a0087207e49a2dcff.jpg")
    embed.set_footer(text="롤 전적 검색의 경우, 언랭이면 검색이 안되거나 자랭이 출력됩니다.")

    await ctx.send(embed=embed)


# 위에서 설정한 client class를 token으로 인증하여 실행합니다.
client.run(os.environ['token'])


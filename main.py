import discord
import requests
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
import pandas as pd
from discord.ext import commands
import pymorphy2
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import random
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import pandas as pd
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import random
import asyncio
import time
import os 
from urllib3.util.retry import Retry
import ssl



TOKEN = ''
CHANNEL_ID = 1228754643845251262
# Ссылки на сайты с новостями о глобальном потеплении
ria_news = 'https://ria.ru/keyword_globalnoe_poteplenie/'


# Время между отправкой новостей (в секундах)
INTERVAL = 60  # 60 секунд для проверки
interval = 60

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


# Префикс, который будет удалять сообщение
PREFIX = "$"
DELAY = 2

async def send_news_ria(ctx):
    while True:
        # Выбираем случайный источник новостей
        response = requests.get(ria_news)
        bs = BeautifulSoup(response.text,"lxml")

        # Находим все элементы с новостями
        articles = bs.find_all('div', 'list-item__content')

        # Проходим по каждой статье по порядку
        for i, article in enumerate(articles):
            news_title = article.text.strip()
            news_link = article.find('a').get('href')

            # Отправляем сообщение с заголовком и ссылкой
            await ctx.send(f"**{news_title}**\n{news_link}")

            # Ждем INTERVAL секунд перед отправкой следующей новости
            await asyncio.sleep(interval)

        # Достигли конца страницы, ждем INTERVAL секунд перед перезагрузкой
        await asyncio.sleep(interval)

@bot.command()
async def start(ctx):
    await send_news_ria(ctx)  # Запускаем функцию отправки новостей


# Список ежедневных задач
daily_tasks = [
  "Посадите дерево или цветок",
  "Сделайте уборку в парке или дворе",
  "Откажитесь от использования одноразовых пакетов",
  "Используйте меньше воды при мытье посуды",
  "Перерабатывайте мусор",
  "Сократите потребление электроэнергии",
  "Используйте общественный транспорт вместо личного автомобиля",
  "Купите продукты местного производства",
  "Поделитесь своим экологическим опытом с друзьями",
  "Пожертвуйте деньги в экологическую организацию",
]

# Функция для отправки случайного слова
async def send_random_word(ctx):
  while True:
    # Выбираем случайное слово
    random_word = random.choice(daily_tasks)
    
    # Получаем канал по ID
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
      print("Канал не найден.")
      return

    # Отправляем сообщение в канал
    await channel.send(f"ЭКОЛОГИЧЕСКОЕ ЗАДАНИЕ НА СЕГОДНЯ: {random_word}")
    
    # Ждем INTERVAL секунд перед следующей отправкой
    await asyncio.sleep(interval)

# Команда для запуска отправки слов
@bot.command()
async def start_words_command(ctx):
  await send_random_word(ctx)
 

bot.run(TOKEN)

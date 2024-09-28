import discord
import random
import requests
from discord.ext import commands
import os
import youtube_dl
import requests
import time
import asyncio
import os
import uuid


from model import fish


image_dir = 'images'


print(os.listdir('images'))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
 
@bot.command()
async def hello(ctx):
    await ctx.send(f'Привет! Я бот {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Список доступных команд:", color=discord.Color.blue())
    bot_commands = [command.name for command in bot.commands]
    embed.add_field(name="Команды", value='\n'.join(bot_commands), inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def calculate(ctx, *, expression):
    try:
        result = eval(expression)
        await ctx.send(f'Result: {result}')
    except Exception as e:
        await ctx.send(f'Error: {e}')


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def yes_or_no(ctx):
    response = random.choice(['Да', 'Нет'])
    await ctx.send(response)


@bot.command()
async def mem(ctx):
    images = os.listdir('images')
    img_name = random.choice(images)
    with open(f'images/{img_name}','rb') as f:
            picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command()
async def animals(ctx):
    images = os.listdir('images2')
    img_name = random.choice(images)
    with open(f'images/{img_name}', 'rb') as f:
            picture = discord.File(f)
    await ctx.send(file=picture)

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('duck')
async def duck(ctx):
    '''По команде duck вызывает функцию get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

async def play_song(ctx, url):
    # Создаем экземпляр загрузчика YouTube
    ydl_opts = {'format': 'bestaudio', 'noplaylist':'True'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
    # Подключаемся к голосовому каналу
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()
    # Проигрываем аудио в голосовом канале
    source = await discord.FFmpegOpusAudio.from_probe(url2, method='fallback')
    player = voice_client.play(source)
    # Ожидаем окончания проигрывания
    await ctx.send(f'Сейчас играет: {info["title"]}')
    while not player.is_done():
        await asyncio.sleep(1)
    # Отключаемся от голосового канала
    await voice_client.disconnect()


if not os.path.exists(image_dir):
    os.makedirs(image_dir)

@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f"images/{attachment.filename}")
            await ctx.channel.send(f"Изображение сохранено в images/{attachment.filename}")

            name = fish(f"images/{attachment.filename}")
            await ctx.send(name)

            if name == "bersh":
                await ctx.channel.send("Это - берш")
            elif name == "ersh":
                await ctx.channel.send("Это - ёрш")
            elif name == "karas":
                await ctx.channel.send("Это - карась")
            elif name == "krasnoperka":
                await ctx.channel.send("Это - краснопёрка")
            elif name == "lesh":
                await ctx.channel.send("Это - лещ")
            elif name == "okun":
                await ctx.channel.send("Это - окунь")
            elif name == "shuka":
                await ctx.channel.send("Это - щука")
            elif name == "som":
                await ctx.channel.send("Это - сом")
            elif name == "sudak":
                await ctx.channel.send("Это - судак")
    else:
        await ctx.channel.send("В вашем сообщении нет изображений.")

    
@bot.event #модерация канала
async def on_message(message):
    if message.author == bot.user:  # Чтобы бот не реагировал на свои же сообщения
        return

    # Список запрещенных слов
    forbidden_words = ['Блять', 'блять', 'бля',"Бля","Пиздец", "пиздец", "Нахуй", "нахуй", "пздц", "Пздц","нах","Нах","Сука", "сука", "блядь", "Блядь","Бл", "бл", "сук", "БЛЯТЬ", "БЛЯ", "ПИЗДЕЦ", "НАХУЙ", "ПЗДЦ", "Ебал", "ебал", "ЕБАЛ", "Шлюха", "шлюха", "ШЛЮХА", "гандон", "Гандон", "ГАНДОН"]
    
    for word in forbidden_words:
        if word in message.content.lower():
            await message.delete()  # Удаляем сообщение, если оно содержит запрещенное слово
            await message.channel.send(f'{message.author.mention}, ваше сообщение было удалено за нарушение правил модерации.')
            break  # Прерываем цикл, если найдено запрещенное слово

    await bot.process_commands(message)  # Обязательно для правильной обработки других команд

# Функция для отправки сообщения по расписанию
async def scheduled_message():
    await bot.wait_until_ready()
    ecos = ["Железная банка - 10 лет", "синтетическая одежда - 30-40 лет", "жестяная банка - до 90 лет", "окурок (сигаретный фильтр) - до 3 лет", "металлические контейнеры разрушаются в морской среде за 10 лет, а бетонированные - 30 лет",
            "обувь из искусственной кожи - 40-50 лет", "жевательная резинка (в теплых климатических условиях) - 30 лет, на холоде - сотни лет", "обломки кирпича и бетона - 100 лет", "аккумуляторы, батарейки - 100 лет", "резина - 100 лет", 
            "пластик - 100 лет", "полиэтилен - 100-200 лет", "стекло - более 1000 лет"]
    channel = bot.get_channel(1228754643845251262)  # Замените 1228754643845251262 на ID канала, куда нужно отправлять сообщение
    while not bot.is_closed():
        rand = random.choice(ecos)
        await channel.send(rand)
        await asyncio.sleep(120)  # Отправлять сообщение каждыt 2 мин. (в секундах)

async def clear_messages(ctx, number_of_messages: int):
  """Очищает определенное количество сообщений в текстовом канале.

  Args:
    ctx: контекст команды
    number_of_messages: количество сообщений, которое нужно удалить
  """

  # Получаем текстовый канал, в котором была вызвана команда.
  channel = ctx.channel

  # Удаляем указанное количество сообщений.
  await channel.purge(limit=number_of_messages)

  # Отправляем сообщение об успешном удалении сообщений.
  await ctx.send(f"Очищено {number_of_messages} сообщений.")

@bot.command()
async def clear(ctx, number_of_messages: int):
    """Очищает определенное количество сообщений в текстовом канале.

    Использование: !clear <количество сообщений>
    """

    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("У вас нет прав на очистку сообщений.")
        return

    await clear_messages(ctx, number_of_messages)  


# Команда для запуска отправки сообщения по расписанию
@bot.command()
async def start_scheduled_message(ctx):
    bot.loop.create_task(scheduled_message())
    await ctx.send('Отправка сообщения по расписанию начата.')


class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.points = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        author_id = str(message.author.id)
        if author_id not in self.points:
            self.points[author_id] = 0

        self.points[author_id] += 1

    @commands.command()
    async def points(self, ctx):
        author_id = str(ctx.author.id)
        await ctx.send(f"У вас сейчас {self.points[author_id]} баллов.")

def setup(bot):
    bot.add_cog(Points(bot))
    
bot.run("")



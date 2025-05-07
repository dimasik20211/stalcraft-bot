import discord from discord.ext import commands, tasks import requests from bs4 import BeautifulSoup

TOKEN = 'MTM2OTU3MTg5NjA0NzQzNTc5Ng.GGzNzW.oIzYjubjvJXW9h-ULQcJi4SeBCrtbYgEI0Nzds'  # Замените на токен своего бота 
CHANNEL_ID = 1328017420702711919   # Замените на ID канала, куда бот будет отправлять обновления 
STEAMDB_URL = 'https://steamdb.info/app/1818450/patchnotes/'

intents = discord.Intents.default() bot = commands.Bot(command_prefix='!', intents=intents)

latest_patch_id = None

@bot.event async def on_ready(): print(f'Logged in as {bot.user.name}') check_updates.start()

@tasks.loop(minutes=10) async def check_updates(): global latest_patch_id response = requests.get(STEAMDB_URL) soup = BeautifulSoup(response.text, 'html.parser')

first_patch = soup.select_one('.patch .header a')
if first_patch:
    patch_url = 'https://steamdb.info' + first_patch['href']
    patch_id = patch_url.split('/')[-2]

    if patch_id != latest_patch_id:
        latest_patch_id = patch_id
        patch_title = first_patch.text.strip()
        
        # Загружаем текст изменений
        patch_text_block = soup.select_one('.patch .body')
        patch_text = patch_text_block.get_text(separator='\n', strip=True)[:1800]

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(f'**Новый патч STALCRAFT X найден!**\n{patch_title}\n{patch_url}\n```{patch_text}```')

bot.run(TOKEN)


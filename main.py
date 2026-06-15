import discord
import requests
import random
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)

# Función para obtener una imagen aleatoria de pato
def get_duck_image_url():
    url = "https://random-d.uk/api/random"
    res = requests.get(url)
    data = res.json()
    return data["url"]


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command()
async def hello(ctx):
    await ctx.send(f'Hola, soy un bot {bot.user}!')


@bot.command()
async def heh(ctx):
    await ctx.send("hehehe")


@bot.command()
async def files(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            await attachment.save(f"img/{attachment.filename}")

        await ctx.send("Imagen guardada con éxito en img")
    else:
        await ctx.send("No subiste ninguna imagen")


@bot.command()
async def mem(ctx):
    image = random.choice(os.listdir("images"))

    with open(f"images/{image}", "rb") as f:
        picture = discord.File(f)
        await ctx.send(file=picture)


@bot.command(name="duck")
async def duck(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)

bot.run('MTQ1MTY4MjUzOTgzMTAzODE2NQ.GDWDcv.XMTmQd9ytwvGa0bY1g0zuzDA2bNleIh3J3LT3o')
import discord
import random
from discord.ext import commands
import aiohttp
import ssl

intents = discord.Intents.default()
intents.message_content = True

# Crear el contexto SSL
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Crear el bot con el conector personalizado
async def main():
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with commands.Bot(
            command_prefix='!',
            intents=intents,
            connector=connector
        ) as bot:
            @bot.event
            async def on_ready():
                print(f'{bot.user} se ha conectado!')
            @bot.command()
            async def hello(ctx):
                await ctx.send(f'Hola, soy un bot {bot.user}!')
            @bot.command()
            async def add(ctx, left: int, right: int):
                """Adds two numbers together."""
                await ctx.send(left + right)
            @bot.command(description='For when you wanna settle the score some other way')
            async def choose(ctx, *choices: str):
                """Chooses between multiple choices."""
                await ctx.send(random.choice(choices))
            @bot.command()
            async def heh(ctx, count_heh = 5):
                await ctx.send("he" * count_heh)
            await bot.start('ADD YOUR TOKEN HERE')

# Ejecutar
import asyncio
asyncio.run(main())

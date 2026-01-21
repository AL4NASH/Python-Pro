import discord
import random
from discord.ext import commands
import aiohttp
import ssl
import requests
import os

intents = discord.Intents.default()
intents.message_content = True

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


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
            async def recycle(ctx, question: int):
                """Ask about recycling"""
                if question == "What is to recycle?":
                    await ctx.send(f"Recycling is about converting plastic waste, the garbage we consume daily, into new products or raw materials for later use.")
                elif question == "At which cans do I dispose of my waste?":
                    await ctx.send(f"White: Clean usable waste (plastic, glass, metal, paper and cardboard). Green: Reusable organic waste (food scraps, agricultural waste. Black: Non-reusable waste (toilet paper, used napkins, cardboard contaminated with food. Red: Hazardous or biological waste (masks, gloves, syringes, chemicals).")
                elif question == "Which of these objects should NOT be put in the white recycling bin even if it is plastic?":
                    await ctx.send(f"An empty water bottle. A dirty yogurt container with food remains. A clean grocery bag.")
                elif question == "Which of these objects should NOT be put in the green recycling bin?":
                    await ctx.send("Plastics and glass (never). Toilet paper and napkins (they go black). Diapers and face masks (they go black or red). Batteries and electronics (they are toxic).")
            await bot.start('PON EL TOKEN DE TU BOTSITO')
# Ejecutar
import asyncio
asyncio.run(main())

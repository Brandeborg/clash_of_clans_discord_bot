import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_API_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'I\'m ready, yo')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("$hello"):
        await message.channel.send("Hello there")

client.run(DISCORD_TOKEN)
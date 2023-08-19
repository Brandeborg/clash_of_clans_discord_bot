import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_API_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = "/", intents=intents)

@bot.command()
async def repeat(ctx, arg):
    await ctx.send(arg)

bot.run(DISCORD_TOKEN)
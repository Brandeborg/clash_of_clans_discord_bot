import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_API_TOKEN")

import discord
from discord.ext import commands

bot = commands.Bot()

@bot.slash_command(name="repeat", description="Repeats the argument", guild_ids=[1142445213084815450])
async def repeat(ctx, arg):
    await ctx.respond(arg)

bot.run(DISCORD_TOKEN)
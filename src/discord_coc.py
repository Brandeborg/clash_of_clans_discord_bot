import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_API_TOKEN")

from discord.ext import commands
bot = commands.Bot()

@bot.slash_command(name="repeat", description="Repeats the argument", guild_ids=[1142445213084815450])
async def repeat(ctx, arg):
    await ctx.respond(arg)

@bot.slash_command(name="add", description="Adds two numbers", guild_ids=[1142445213084815450])
async def repeat(ctx, num1, num2):
    await ctx.respond(int(num1) + int(num2))

bot.run(DISCORD_TOKEN)
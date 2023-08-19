import os
from dotenv import load_dotenv
import re

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_API_TOKEN")

from discord.ext import commands
from discord.commands import Option

bot = commands.Bot()

@bot.slash_command(name="repeat", description="Repeats the argument", guild_ids=[1142445213084815450])
async def repeat(ctx, arg):
    await ctx.respond(arg)

@bot.slash_command(name="add", description="Adds two numbers", guild_ids=[1142445213084815450])
async def add(ctx, num1, num2):
    await ctx.respond(int(num1) + int(num2))

@bot.slash_command(name="get_coc_id", description="Extracts the users CoC user ID from Discord username", guild_ids=[1142445213084815450])
async def cocid(ctx, coc_uid: Option(str, "Enter your CoC user ID", required = False, default = None)):
    coc_user_id = re.search(r'\((.*?)\)', ctx.author.display_name).group(1)
    await ctx.respond(coc_user_id)

bot.run(DISCORD_TOKEN)
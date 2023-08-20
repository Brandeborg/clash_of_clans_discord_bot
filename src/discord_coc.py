import os
import re
import bot_util
import clash_of_clans

from dotenv import load_dotenv
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_API_TOKEN")
DISCORD_SERVER_ID = os.getenv("DISCORD_SERVER_ID")

from discord.ext import commands
from discord.commands import Option

bot = commands.Bot()
coc = clash_of_clans.CoCAPI()

@bot.slash_command(name="player_name", description="Returns the user's Clash of Clans name", guild_ids=[DISCORD_SERVER_ID])
async def coc_name(ctx, coc_tag: Option(str, "Enter your CoC user ID", required = False, default = None)):
    try:
        tag = await get_playertag(ctx, coc_tag)
    except Exception as e:
        return await ctx.respond(e)
    
    try:
        player = coc.player(tag)
    except Exception as e:
        return await ctx.respond(e)

    await ctx.respond(player["name"])
    
    
# helper functions
async def get_playertag(ctx, coc_tag):
    tag = bot_util.extract_playertag(ctx.author.display_name) if not coc_tag else coc_tag

    if not tag.startswith("#"): tag = "#" + tag

    bot_util.validate_playertag(tag)
    
    return tag


bot.run(DISCORD_TOKEN)
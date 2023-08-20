import os
from dotenv import load_dotenv
import re
import bot_util

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_API_TOKEN")
DISCORD_SERVER_ID = os.getenv("DISCORD_SERVER_ID")

from discord.ext import commands
from discord.commands import Option

bot = commands.Bot()

@bot.slash_command(name="player_name", description="Returns the user's Clash of Clans name", guild_ids=[DISCORD_SERVER_ID])
async def coc_name(ctx, coc_tag: Option(str, "Enter your CoC user ID", required = False, default = None)):
    tag = await get_playertag(ctx, coc_tag)
    
    
# helper functions
async def get_playertag(ctx, coc_tag):
    try:
        coc_player_tag = bot_util.extract_playertag(ctx.author.display_name) if not coc_tag else coc_tag
    except Exception as e:
        return await ctx.respond(e)
    
    try:
        bot_util.validate_playertag(coc_player_tag)
    except Exception as e:
        return await ctx.respond(e)
    


bot.run(DISCORD_TOKEN)
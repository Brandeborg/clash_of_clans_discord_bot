from discord.commands import Option
from discord.ext import commands
import os
import re
import bot_util
import clash_of_clans

from dotenv import load_dotenv
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_API_TOKEN")
DISCORD_SERVER_ID = os.getenv("DISCORD_SERVER_ID")


bot = commands.Bot()
coc = clash_of_clans.CoCAPI()

# commands
@bot.slash_command(name="player_name", description="Returns the player's Clash of Clans name", guild_ids=[DISCORD_SERVER_ID])
async def coc_playername(ctx, playertag: Option(str, "Enter your CoC player tag", required=False, default=None)):
    try:
        playertag = await get_playertag(ctx.author.display_name) if not playertag else playertag
        bot_util.validate_tag(playertag)
        player = coc.player(playertag)
    except Exception as e:
        return await ctx.respond(e)
    
    await ctx.respond(player["name"])

@bot.slash_command(name="clan_name", description="Returns the player's Clash of Clans clan name", guild_ids=[DISCORD_SERVER_ID])
async def coc_clanname(ctx, playertag: Option(str, "Enter your CoC player tag", required=False, default=None),
                       clantag: Option(str, "Enter your CoC clan tag", required=False, default=None)):
    if not clantag:
        try:
            playertag = await get_playertag(ctx.author.display_name) if not playertag else playertag
            bot_util.validate_tag(playertag)
            clantag = await get_clantag(playertag)
        except Exception as e:
            return await ctx.respond(e)
    
    try:
        bot_util.validate_tag(clantag)
        clan = coc.clan(clantag)
    except Exception as e:
        return await ctx.respond(e)

    await ctx.respond(clan["name"])

# helper functions
async def get_playertag(displayname):
    tag = bot_util.extract_playertag(displayname)

    if not tag.startswith("#"):
        tag = "#" + tag

    return tag

async def get_clantag(playertag):
    player = coc.player(playertag)
    return player["clan"]["tag"]

bot.run(DISCORD_TOKEN)

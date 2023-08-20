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
    """Sends a response containing a Clash of Clans player name, 
    either by looking up an explicitly passed playertag or by extracting a playertag from
    the discord user's displayname.

    Args:
        ctx (_type_): Discord context, containing attributes such as displayname and functions
        playertag (Option, optional): A CoC player tag. Defaults to False, default=None).

    Returns:
        None: Returns nothing
    """
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
    """Sends a response containing a Clash of Clans clan name, 
    either by looking up an explicitly passed playertag or clantag or by extracting a playertag from
    the discord user's displayname. If no clan tag is passed, the player tag will be used to fetch a 
    clantag associated with the player.

    Args:
        ctx (_type_): Discord context, containing attributes such as displayname and functions
        playertag (Option, optional): A CoC player tag. Defaults to False, default=None).
        clantag (Option, optional): A CoC clan tag. Defaults to False, default=None).

    Returns:
        _type_: _description_
    """
    if not clantag:
        try:
            playertag = await get_playertag(ctx.author.display_name) if not playertag else playertag
            playertag = add_octothorpe(playertag)
            bot_util.validate_tag(playertag)
            clantag = await get_clantag(playertag)
        except Exception as e:
            return await ctx.respond(e)
    
    try:
        clantag = add_octothorpe(clantag)
        bot_util.validate_tag(clantag)
        clan = coc.clan(clantag)
    except Exception as e:
        return await ctx.respond(e)

    await ctx.respond(clan["name"])

# helper functions
async def get_playertag(displayname):
    """Just a wrapper
    """
    return bot_util.extract_playertag(displayname)

async def get_clantag(playertag: str) -> str:
    """Fetches a player from CoC API and extracts the clan tag.

    Args:
        playertag (str): A CoC player tag.

    Returns:
        str: A clan tag
    """
    player = coc.player(playertag)
    return player["clan"]["tag"]

def add_octothorpe(tag: str) -> str:
    """Adds a "#" to a tag if it does not already contrain one.

    Args:
        tag (str): A player or clan tag

    Returns:
        str: A tag with a "#"
    """
    if not tag.startswith("#"):
        tag = "#" + tag

    return tag

bot.run(DISCORD_TOKEN)

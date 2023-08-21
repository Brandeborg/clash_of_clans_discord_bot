from textwrap import dedent
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
    # fetch data
    try:
        playertag = await bot_util.get_playertag(ctx.author.display_name) if not playertag else playertag
        playertag = bot_util.add_octothorpe(playertag)
        bot_util.validate_tag(playertag)
        player = coc.player(playertag)
    except Exception as e:
        return await ctx.respond(e)
    
    # format response

    # send response
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
    # fetch data
    try:
        clantag: str = await bot_util.handle_clantag_options(ctx.author.display_name, playertag, clantag)
        clan = coc.clan(clantag)
    except Exception as e:
        return await ctx.respond(e)

    # format response

    # send response
    await ctx.respond(clan["name"])

@bot.slash_command(name="current_war", description="Returns details about a clan's ongoing war", guild_ids=[DISCORD_SERVER_ID])
async def coc_clanname(ctx, playertag: Option(str, "Enter your CoC player tag", required=False, default=None),
                       clantag: Option(str, "Enter your CoC clan tag", required=False, default=None)):
    """Sends a response containing a details about Clash of Clans clan's current war, 
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
    # fetch data
    try:
        clantag: str = await bot_util.handle_clantag_options(ctx.author.display_name, playertag, clantag)
        current_war = coc.current_war(clantag)
    except Exception as e:
        return await ctx.respond(e)

    # format response
    cw = current_war
    us = cw["clan"]
    op = cw["opponent"]

    bot_util.average_TH(us["members"])

    war_status = \
    f"""
    War Status 
    State: {cw["state"]}

    {us["name"]} (TH lvl {bot_util.average_TH(us["members"])})  
    {us["stars"]} stars
    {us["attacks"]} attacks

    vs. 
    
    {op["name"]} (TH lvl {bot_util.average_TH(op["members"])})
    {op["stars"]} stars
    {op["attacks"]} attacks
    """

    # send response
    await ctx.respond(dedent(war_status))


bot.run(DISCORD_TOKEN)

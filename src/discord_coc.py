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
    the discord user's display name.

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

@bot.slash_command(name="player_progress_th", description="Returns the players progress towards maxing current TH", guild_ids=[DISCORD_SERVER_ID])
async def coc_player_progress_th(ctx, playertag: Option(str, "Enter your CoC player tag", required=False, default=None)):
    """Sends a response containing a Clash of Clans player's progress of upgrading:
    - heroes
    - troops ("characters")
    - pets

    either by looking up an explicitly passed player tag or by extracting a player tag from
    the discord user's display name.

    Args:
        ctx (_type_): Discord context, containing attributes such as displayname and functions
        playertag (Option, optional): A CoC player tag. Defaults to False, default=None).

    Returns:
        None: Returns nothing
    """
    # fetch data from CoC API
    try:
        playertag = await bot_util.get_playertag(ctx.author.display_name) if not playertag else playertag
        playertag = bot_util.add_octothorpe(playertag)
        bot_util.validate_tag(playertag)
        player = coc.player(playertag)
    except Exception as e:
        return await ctx.respond(e)
    
    # extract max levels from static files
    player_th_lvl = player["townHallLevel"]
    
    ## heroes
    hero_maxes = bot_util.get_max_lvls(player_th_lvl, "heroes", "RequiredTownHallLevel")
    del hero_maxes["Warmachine"]
    del hero_maxes["Battle Copter"]

    hero_actuals = bot_util.get_current_lvls(player["heroes"])
    del hero_actuals["Battle Machine"]
    del hero_actuals["Battle Copter"]

    name_map = bot_util.load_json("../assets/unit_name_map.json")

    result = {}
    for hero in hero_maxes:
        hero_actual = hero_actuals[name_map[hero]] if hero in hero_actuals else 0
        hero_max = hero_maxes[hero]
        result[hero] = (hero_actual, hero_max)

    # troops
    th_lab_map = bot_util.get_th_lab_map()
    player_lab_level = th_lab_map[player_th_lvl]
    # NOTE: Need to also look at barrack level for troops. Maybe a new func that checks it after looking at lab level
    troop_maxes = bot_util.get_max_lvls(player_lab_level, "characters", "LaboratoryLevel")

    troop_actuals = bot_util.get_current_lvls(player["troops"])

    name_map = bot_util.load_json("../assets/unit_name_map.json")

    result = {}
    for troop in troop_maxes:
        troop_actual = troop_actuals[troop] if troop in troop_actuals else 0
        troop_max = troop_maxes[troop]
        result[troop] = (troop_actual, troop_max)
    print(result)

    ## troops


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
    apm = cw["attacksPerMember"]
    ts = cw["teamSize"]

    bot_util.average_TH(us["members"])

    war_status = \
    f"""
    War Status 
    State: {cw["state"]}

    {us["name"]} (TH lvl {bot_util.average_TH(us["members"])})  
    {us["stars"]} / {ts * 3} stars
    {us["attacks"]} / {ts * apm} attacks

    vs. 
    
    {op["name"]} (TH lvl {bot_util.average_TH(op["members"])})
    {op["stars"]} / {ts * 3} stars
    {op["attacks"]} / {ts * apm} attacks
    """

    # send response
    await ctx.respond(dedent(war_status))


bot.run(DISCORD_TOKEN)

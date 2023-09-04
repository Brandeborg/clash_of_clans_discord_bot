import asyncio
from textwrap import dedent
from discord.commands import Option
from discord.ext import commands
import discord
import os

import numpy as np

import bot_util
import clash_of_clans
from hero import Hero
from troop import Troop
from spell import Spell

from dotenv import load_dotenv

from unit import Unit
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
    # it can happen, that the command cannot respond with image within 3 seconds,
    # so we need to send an inital response, after which there are 15 minutes to respond
    await ctx.defer()

    # fetch data from CoC API
    try:
        playertag = await bot_util.get_playertag(ctx.author.display_name) if not playertag else playertag
        playertag = bot_util.add_octothorpe(playertag)
        bot_util.validate_tag(playertag)
        player = coc.player(playertag)
    except Exception as e:
        return await ctx.respond(e)
    
    player_th_lvl = player["townHallLevel"]
    translation = bot_util.load_json("../assets/texts_EN.json")
    unit_groups = bot_util.load_json("../assets/unit_groups.json")
    
    # create unit objects for each unit
    heroes = Hero.create_hero_objects(translation=translation, unit_groups=unit_groups, player=player)
    troops = Troop.create_troop_objects(translation=translation, unit_groups=unit_groups, player=player)
    spells = Spell.create_troop_objects(translation=translation, unit_groups=unit_groups, player=player)

    # extract relevant data for each unit
    unit_attributes = [("Heroes", Hero.list_display_attributes(heroes, th_level=player_th_lvl)),
    ("Troops", Troop.list_display_attributes(troops, th_level=player_th_lvl)),
    ("Spells", Spell.list_display_attributes(spells, th_level=player_th_lvl))]

    ## sum values
    unit_totals = []
    for name, units in unit_attributes:
        unit_total = bot_util.sum_dict_list_columns(units, ignore_columns=[0], ic_values=[name], dtype=int)
        unit_totals.append(unit_total)

    total = bot_util.sum_dict_list_columns(unit_totals, ignore_columns=[0], ic_values=["Total"], dtype=int)
    unit_totals.append(total)
    
    ## display result
    displayed_units = Unit.display_units(units=unit_totals, unit_order=["Heroes", "Troops", "Spells", "Total"])
    columns = ["Name", "Level", "Time", "Elixir", "Dark Elixir", "Gold"]

    plt_file_path = 'temp.png'
    columns = ["Name", "Level", "Time", "Elixir", "Dark Elixir", "Gold"]
    title = f"Progress for {player['name']} ({player['tag']}) to max Town Hall level {player_th_lvl}"
    bot_util.plot_table(rows=displayed_units, columns=columns, file_path=plt_file_path, title=title)

    # send response
    await ctx.respond(title, file=discord.File(plt_file_path))
    os.remove(plt_file_path)

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
async def current_war(ctx, playertag: Option(str, "Enter your CoC player tag", required=False, default=None),
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
    
    if cw["state"] == "notInWar":
        repsonse = f'{clantag} is not currently in a regular war'
        await ctx.respond(repsonse)
        return
    
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

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
@bot.slash_command(name="player_progress", description="Returns the players progress towards maxing current TH", guild_ids=[DISCORD_SERVER_ID])
async def coc_player_progress(ctx, 
                              playertag: Option(str, "Enter a CoC player tag", required=False, default=None), 
                              th_level: Option(str, "Enter a Town Hall level", required=False, default=None)):
    """Sends a response containing a Clash of Clans player's progress of upgrading:
    - heroes
    - troops ("characters")
    - spells

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
    
    try:
        th_lvl = player["townHallLevel"] if not th_level else int(th_level)
    except:
        await ctx.respond("The passed th_level is probably not a number")
        return
    translation = bot_util.load_json("../assets/texts_EN.json")
    unit_groups = bot_util.load_json("../assets/unit_groups.json")
    
    # create unit objects for each unit
    heroes = Hero.create_hero_objects(translation=translation, unit_groups=unit_groups, player=player)
    troops = Troop.create_troop_objects(translation=translation, unit_groups=unit_groups, player=player)
    spells = Spell.create_spell_objects(translation=translation, unit_groups=unit_groups, player=player)

    # extract relevant data for each unit
    unit_attributes = [("Heroes", Hero.list_display_attributes(heroes, th_level=th_lvl)),
    ("Troops", Troop.list_display_attributes(troops, th_level=th_lvl)),
    ("Spells", Spell.list_display_attributes(spells, th_level=th_lvl))]

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
    title = f"Progress for {player['name']} ({player['tag']}) to max Town Hall level {th_lvl}"
    bot_util.plot_table(rows=displayed_units, columns=columns, file_path=plt_file_path, title=title)

    # send response
    await ctx.respond(title, file=discord.File(plt_file_path))
    os.remove(plt_file_path)

@bot.slash_command(name="player_progress_heroes", description="Returns the players progress towards maxing current TH", guild_ids=[DISCORD_SERVER_ID])
async def coc_player_progress_heroes(ctx, 
                                     playertag: Option(str, "Enter a CoC player tag", required=False, default=None),
                                     th_level: Option(str, "Enter a Town Hall level", required=False, default=None)):
    """Sends a response containing a Clash of Clans player's progress of upgrading individual heroes

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
    
    #TODO: Some code repetition has snuck in again, rethink structure of individual unit commands (spells, heroes, etc.)
    # and try to reuse some stuff, like the snippet below
    try:
        th_lvl = player["townHallLevel"] if not th_level else int(th_level)
    except:
        await ctx.respond("The passed th_level is probably not a number")
        return
    translation = bot_util.load_json("../assets/texts_EN.json")
    unit_groups = bot_util.load_json("../assets/unit_groups.json")
    
    # create unit objects for each unit
    heroes = Hero.create_hero_objects(translation=translation, unit_groups=unit_groups, player=player)

    # extract relevant data for each unit
    hero_attributes = Hero.list_display_attributes(heroes, th_level=th_lvl)

    hero_attributes.append(bot_util.sum_dict_list_columns(hero_attributes, [0], ["Total"], int))
    
    ## display result
    displayed_units = Unit.display_units(units=hero_attributes, unit_order=unit_groups["home_heroes"] + ["Total"])
    columns = ["Name", "Level", "Time", "Elixir", "Dark Elixir", "Gold"]

    plt_file_path = 'temp.png'
    columns = ["Name", "Level", "Time", "Elixir", "Dark Elixir", "Gold"]
    title = f"Hero progress for {player['name']} ({player['tag']}) to max Town Hall level {th_lvl}"
    bot_util.plot_table(rows=displayed_units, columns=columns, file_path=plt_file_path, title=title)

    # send response
    await ctx.respond(title, file=discord.File(plt_file_path))
    os.remove(plt_file_path)

@bot.slash_command(name="player_progress_troops", description="Returns the players progress towards maxing current TH", guild_ids=[DISCORD_SERVER_ID])
async def coc_player_progress_troops(ctx, 
                                     playertag: Option(str, "Enter a CoC player tag", required=False, default=None),
                                     th_level: Option(str, "Enter a Town Hall level", required=False, default=None)):
    """Sends a response containing a Clash of Clans player's progress of upgrading individual troops

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
    
    try:
        th_lvl = player["townHallLevel"] if not th_level else int(th_level)
    except:
        await ctx.respond("The passed th_level is probably not a number")
        return
    translation = bot_util.load_json("../assets/texts_EN.json")
    unit_groups = bot_util.load_json("../assets/unit_groups.json")
    
    # create unit objects for each unit
    troops = Troop.create_troop_objects(translation=translation, unit_groups=unit_groups, player=player)

    # extract relevant data for each unit
    troop_attributes = Troop.list_display_attributes(troops, th_level=th_lvl)

    troop_attributes.append(bot_util.sum_dict_list_columns(troop_attributes, [0], ["Total"], int))
    
    ## display result
    displayed_units = Unit.display_units(units=troop_attributes, unit_order=unit_groups["home_troops"] + ["Total"])
    columns = ["Name", "Level", "Time", "Elixir", "Dark Elixir", "Gold"]

    plt_file_path = 'temp.png'
    columns = ["Name", "Level", "Time", "Elixir", "Dark Elixir", "Gold"]
    title = f"Troop progress for {player['name']} ({player['tag']}) to max Town Hall level {th_lvl}"
    bot_util.plot_table(rows=displayed_units, columns=columns, file_path=plt_file_path, title=title)

    # send response
    await ctx.respond(title, file=discord.File(plt_file_path))
    os.remove(plt_file_path)

@bot.slash_command(name="player_progress_spells", description="Returns the players progress towards maxing current TH", guild_ids=[DISCORD_SERVER_ID])
async def coc_player_progress_spells(ctx, 
                                     playertag: Option(str, "Enter a CoC player tag", required=False, default=None),
                                     th_level: Option(str, "Enter a Town Hall level", required=False, default=None)):
    """Sends a response containing a Clash of Clans player's progress of upgrading individual spells

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
    
    try:
        th_lvl = player["townHallLevel"] if not th_level else int(th_level)
    except:
        await ctx.respond("The passed th_level is probably not a number")
        return
    translation = bot_util.load_json("../assets/texts_EN.json")
    unit_groups = bot_util.load_json("../assets/unit_groups.json")
    
    # create unit objects for each unit
    spells = Spell.create_spell_objects(translation=translation, unit_groups=unit_groups, player=player)

    # extract relevant data for each unit
    spell_attributes = Hero.list_display_attributes(spells, th_level=th_lvl)

    spell_attributes.append(bot_util.sum_dict_list_columns(spell_attributes, [0], ["Total"], int))
    
    ## display result
    displayed_units = Unit.display_units(units=spell_attributes, unit_order=unit_groups["spells"] + ["Total"])
    columns = ["Name", "Level", "Time", "Elixir", "Dark Elixir", "Gold"]

    plt_file_path = 'temp.png'
    columns = ["Name", "Level", "Time", "Elixir", "Dark Elixir", "Gold"]
    title = f"Spell progress for {player['name']} ({player['tag']}) to max Town Hall level {th_lvl}"
    bot_util.plot_table(rows=displayed_units, columns=columns, file_path=plt_file_path, title=title)

    # send response
    await ctx.respond(title, file=discord.File(plt_file_path))
    os.remove(plt_file_path)

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

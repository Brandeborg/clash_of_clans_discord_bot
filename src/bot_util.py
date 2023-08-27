import re
import json
import pandas as pd
import matplotlib.pyplot as plt

import clash_of_clans
coc = clash_of_clans.CoCAPI()


def extract_playertag(displayname: str):
    """Get CoC playertag from Discord display name

    Args:
        displayname (str): Discord display name, which should contain a CoC playertag
    """

    match = re.search(r'\((.*?)\)', displayname)
    if match == None:
        raise Exception(
            """
            Invalid formatting of display name, should be: 
            \"Name (<COC_PLAYERTAG>)\"
            """)

    return match.group(1)


def validate_tag(tag: str):
    """Make sure a tag is of the right format (10 digits)

    Args:
        tag (str): CoC player or clan tag
    """
    if len(tag) != 10:
        raise Exception(
            """
            Invalid tag, should follow one of these formats:
            \"1BCDEFGH9\"
            \"#1BCDEFGH9\"
            """)


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


async def handle_clantag_options(displayname: str, playertag: str, clantag: str) -> str:
    """A discord user can get clan info by multiple means:
    - directly passing clan tag
    - directly passing player tag, backend fetches clan tag
    - not passing anything, but backend extracts player tag from discord display name, the fetches clan tag

    This function handles these options, resulting in a clantag 

    Args:
        displayname (str): A Discord display name
        playertag (str): A CoC player tag, might be empty
        clantag (str): A CoC clan tag, might be empty

    Returns:
        str: A clantag
    """
    if not clantag:
        playertag = await get_playertag(displayname) if not playertag else playertag
        playertag = add_octothorpe(playertag)
        validate_tag(playertag)
        clantag = await get_clantag(playertag)

        clantag = add_octothorpe(clantag)
        validate_tag(clantag)

        return clantag


async def get_playertag(displayname: str):
    """Just a wrapper
    """
    return extract_playertag(displayname)


async def get_clantag(playertag: str) -> str:
    """Fetches a player from CoC API and extracts the clan tag.

    Args:
        playertag (str): A CoC player tag.

    Returns:
        str: A clan tag
    """
    player = coc.player(playertag)
    return player["clan"]["tag"]


def average_TH(members: list) -> int:
    """Given a list of CoC members, calculates the average Townhall level

    Args:
        members (list): A list of CoC war 

    Returns:
        int: The average TH level
    """
    n_members = len(members)
    avg_th = 0
    for member in members:
        avg_th += member["townhallLevel"] / n_members

    return round(avg_th, 2)

def get_th_lab_map() -> dict:
    """Get a mapping from "Thownhall level" to the associated max level of the laboratory.
    Some units report the "required lab level" instead of "required th level", so this is needed.

    Returns:
        dict: {th_level: lab_level, ...}
    """
    buildings = load_json("../assets/buildings.json")
    lab_th_levels = buildings["Laboratory"]["TownHallLevel"]
    th_lab_map = {th_lvl: i+1 for i, th_lvl in enumerate(lab_th_levels)}

    return th_lab_map

def search_unit(name: str, units: list[dict]) -> dict:
    """Search for a unit in a list of unit dics, where the dict contains a name field

    Args:
        name (str): A unit name
        units (list[dict]): A list of units in dicts

    Returns:
        dict: A dict of the unit details
    """
    for unit in units:
        if unit["name"] == name:
            return unit
        
def display_hours_as_days(hours: int) -> str:
    """Convert hours to days and hours, ex: 36 hours -> 1d 12h

    Args:
        hours (int): _description_

    Returns:
        str: _description_
    """
    d = hours // 24
    h = hours % 24

    return f"{d}d {h}h"

def display_large_number(number: int) -> str:
    return f'{number:,}'

def load_json(filename: str) -> dict:
    """Loads a JSON file into a dict

    Args:
        filename (str): path to json file

    Returns:
        dict: _description_
    """
    with open(filename) as jsonf:
        return json.load(jsonf)

def plot_table(rows: list, columns: list, file_path: str):
    df = pd.DataFrame(rows, columns=columns)

    fig, ax = plt.subplots(dpi=300)
    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    tab = ax.table(cellText=df.values, colLabels=df.columns, loc='center')

    tab.auto_set_column_width(col=list(range(len(columns))))
    tab.auto_set_font_size(False)
    tab.set_fontsize(8)

    fig.tight_layout()

    plt.savefig(file_path)
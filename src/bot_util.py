import re
import json

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


def get_max_lvls(th_lvl: int, item_group: str, rq_th_key="RequiredTownHallLevel") -> dict:
    """Constructs a dict of max levels for each item in the item_group (ex: heroes)
    based on the Town Hall level

    Args:
        th_lvl (int): A player's current town hall level
        item_group (str): One of these item groups: "heroes", "characters", "buildings", "pets", "traps", "spells"
        rq_th_key (str, optional): The key used to access the list of "Required Townhall Levels". 
                                   It varies from file to file. Defaults to "RequiredTownHallLevel".

    Returns:
        dict: A mapping from item to max level. Ex: {"Archer Queen": 50}
    """
    max_lvls = {}

    item_group: dict = load_json(f"../assets/{item_group}.json")

    for key in item_group:
        max_lvls[key] = get_maxlvl_from_required_th(
            item_group[key][rq_th_key], th_lvl)

    return max_lvls


def get_maxlvl_from_required_th(required_th_lvls: list, th_lvl: int) -> int:
    """Deduce the maximum item level from a list of "required townhall levels" of the form: 
    [9, 9, 9, 9, 9, 10, 10, 10, ...]

    Args:
        required_th_lvls (list): A list of required town hall levels, where each index is the level of the item. 
                                 In this example, [9,9,9,10,10,11,11], a townhall level 10 is required for reaching level
                                 4, so the max level for th 9 is 3.
        th_lvl (int): A player's current town hall level

    Returns:
        int: The max level of a given item (hero, building, etc.)
    """
    # if smallest required th is larger than current th, max lvl is 0
    if required_th_lvls[0] > th_lvl:
        return 0

    # in case that curr_th_lvl == max_th_lvl
    init_max = len(required_th_lvls)

    for i, rq_th in enumerate(required_th_lvls):
        if rq_th == th_lvl+1:
            return i

    return init_max

def get_item_upgrade_cost_current() -> int:
    pass

def get_item_upgrade_cost_maxed() -> int:
    pass

def load_json(filename: str) -> dict:
    """Loads a JSON file into a dics

    Args:
        filename (str): path to json file

    Returns:
        dict: _description_
    """
    with open(filename) as jsonf:
        return json.load(jsonf)

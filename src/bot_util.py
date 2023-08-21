import re

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

def average_TH(members: list):
    n_members = len(members)
    avg_th = 0
    for member in members:
        avg_th += member["townhallLevel"] / n_members

    return round(avg_th, 2)
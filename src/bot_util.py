import re

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
        
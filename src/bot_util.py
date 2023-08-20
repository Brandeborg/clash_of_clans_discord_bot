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

def validate_playertag(tag: str):
    if len(tag) != 10:
        raise Exception(
            """
            Invalid player tag, should follow one of these formats:
            \"1BCDEFGH9\"
            \"#1BCDEFGH9\"
            """)
        
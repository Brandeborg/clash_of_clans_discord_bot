import re

def extract_playertag(displayname: str):
    """Get CoC usertag from Discord display name

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
    
    tag = match.group(1)

    if tag.startswith("#"):
        return tag
    
    return '#' + tag

def validate_playertag(tag: str):
    tag = tag[1:] if tag.startswith("#") else tag
    if len(tag) != 9:
        raise Exception(
            """
            Invalid player tag, should follow one of these formats:
            \"1BCDEFG8\"
            \"#1BCDEFG8\"
            """)
        
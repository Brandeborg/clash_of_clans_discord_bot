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

def validate_playertag(tag):
    if len(tag) != 9:
        raise Exception("""Invalid player tag, should follow this format:: 
                        \n 
                        \"A1BCD2EFG\"""")
        
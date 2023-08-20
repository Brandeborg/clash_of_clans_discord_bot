import os
import httpx
import urllib.parse

from dotenv import load_dotenv
load_dotenv()
COC_API_BASE_URL = os.getenv("COC_API_BASE_URL")
COC_API_TOKEN = os.getenv("COC_API_TOKEN")

class CoCAPI:
    def __init__(self) -> None:
        self.base_url = COC_API_BASE_URL
        self.headers = {'Authorization' : f"Bearer {COC_API_TOKEN}"}

    def player(self, playertag: str) -> dict:
        # replace # with %23 for a properly formatted url
        playertag = urllib.parse.quote(playertag)

        with httpx.Client() as client: 
            res = client.get(f"{self.base_url}/players/{playertag}", headers=self.headers)

        if res.status_code // 100 == 2:
            return res.json()
        else:
            raise Exception("Something went wrong. The passed playertag may not exist.")
        
    def clan(self, clantag: str) -> dict:
        # replace # with %23 for a properly formatted url
        clantag = urllib.parse.quote(clantag)

        with httpx.Client() as client: 
            res = client.get(f"{self.base_url}/clans/{clantag}", headers=self.headers)

        if res.status_code // 100 == 2:
            return res.json()
        else:
            raise Exception("Something went wrong. The passed clantag may not exist.")


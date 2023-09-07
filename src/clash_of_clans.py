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
        """Fetches a player's data using the CoC API

        Args:
            playertag (str): A CoC player tag

        Raises:
            Exception: If status code is not 2xx, raise an exception

        Returns:
            dict: Player data
        """
        # replace # with %23 for a properly formatted url
        playertag = urllib.parse.quote(playertag)

        with httpx.Client() as client: 
            res = client.get(f"{self.base_url}/players/{playertag}", headers=self.headers)

        if res.status_code // 100 == 2:
            return res.json()
        else:
            print(res.status_code)
            raise Exception("Something went wrong. The passed playertag may not exist.")
        
    def clan(self, clantag: str) -> dict:
        """Fetches a clan's data using the CoC API

        Args:
            clantag (str): A CoC clan tag

        Raises:
            Exception: If status code is not 2xx, raise an exception

        Returns:
            dict: Clan data
        """
        # replace # with %23 for a properly formatted url
        clantag = urllib.parse.quote(clantag)

        with httpx.Client() as client: 
            res = client.get(f"{self.base_url}/clans/{clantag}", headers=self.headers)

        if res.status_code // 100 == 2:
            return res.json()
        else:
            print(res.status_code)
            raise Exception("Something went wrong. The passed clantag may not exist.")
        
    def current_war(self, clantag: str) -> dict:
        """Fetches a clan's current war data using CoC API

        Args:
            clantag (str): A CoC clan tag

        Raises:
            Exception: If status code is not 2xx, raise an exception

        Returns:
            dict: Current clan war data
        """
        # replace # with %23 for a properly formatted url
        clantag = urllib.parse.quote(clantag)

        with httpx.Client() as client: 
            res = client.get(f"{self.base_url}/clans/{clantag}/currentwar", headers=self.headers)

        if res.status_code // 100 == 2:
            return res.json()
        else:
            print(res.status_code)
            raise Exception("Something went wrong. The passed clantag may not exist.")
        
    def current_league_group(self, clantag: str):
        """Fetches a clan's current war league group data using CoC API

        Args:
            clantag (str): A CoC clan tag

        Raises:
            Exception: If status code is not 2xx, raise an exception

        Returns:
            dict: Current clan war data
        """
        # replace # with %23 for a properly formatted url
        clantag = urllib.parse.quote(clantag)

        with httpx.Client() as client: 
            res = client.get(f"{self.base_url}/clans/{clantag}/currentwar/leaguegroup", headers=self.headers)

        if res.status_code // 100 == 2:
            return res.json()
        else:
            print(res.status_code)
            raise Exception("Something went wrong. The passed clantag may not exist.")
        
    def CWL_war(self, wartag: str) -> dict:
        """Fetches a CWL war using CoC API

        Args:
            clantag (str): A CoC CWL war tag

        Raises:
            Exception: If status code is not 2xx, raise an exception

        Returns:
            dict: Current clan war data
        """
        # replace # with %23 for a properly formatted url
        wartag = urllib.parse.quote(wartag)

        with httpx.Client() as client: 
            res = client.get(f"{self.base_url}/clanwarleagues/wars/{wartag}", headers=self.headers)

        if res.status_code // 100 == 2:
            return res.json()
        else:
            print(res.status_code)
            raise Exception("Something went wrong. The passed wartag may not exist.")


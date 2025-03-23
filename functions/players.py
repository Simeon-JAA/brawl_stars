"""Scripts that return player data"""

import re
from os import environ


#TODO Replace requests with asyncio, aiohttp
import requests as r
from dotenv import load_dotenv


def get_api_header(api_token: str) -> dict:
    """Returns api header data"""

    header = {
      "Accept": "application/json",
      "Authorization": f"Bearer {api_token}"
    }

    return header


def to_snake_case(text: str) -> str:
    """Formats text to snake_case"""

    if not isinstance(text, str):
        raise TypeError("Error: Text should be a string!")

    text = text.replace(" ", "")
    text = re.sub(r'([a-z0-9\s]{1})([A-Z]{1})', r'\1_\2', text)

    if not text:
        raise ValueError("Error: Text cannot be blank!")

    return text.lower()


def format_player_tag(player_tag: str) -> str:
    """Formats player tag"""

    if not isinstance(player_tag, str):
        raise TypeError("Error: Player tag must be a string format!")

    player_tag = player_tag.strip().replace("#", "").upper()

    if not player_tag:
        raise ValueError("Error: Player tag must not be empty!")

    return player_tag


def check_player_tag(player_tag: str) -> bool:
    """Returns true if player tage is accepted"""

    player_tag = format_player_tag(player_tag)

    if len(player_tag) < 3:
        return False

    allowed_characters = ['P', 'Y', 'L', 'Q', 'G', 'O', 'R', 'J', 'C', 'U', 'V', '0', '2', '8', '9']

    for character in player_tag:
        if character not in allowed_characters:
            return False

    return True


def format_club_tag(club_tag: str) -> str:
    """Formats club tag"""

    if not isinstance(club_tag, str):
        raise TypeError("Error: Club tag must be a string format!")

    club_tag = club_tag.strip().replace("#", "").upper()

    if not club_tag:
        raise ValueError("Error: Club tag must not be empty!")

    return club_tag


def get_player_data(api_header: dict, player_tag: str) -> dict:
    """Returns player data"""

    player_tag = format_player_tag(player_tag)

    if check_player_tag(player_tag):

        try:
            response = r.get(f"https://api.brawlstars.com/v1/players/%23{player_tag}",
                             headers=api_header, timeout=5)
            response_data = response.json()

        except:
            raise ConnectionError("Error: Unable to retrieve player data!")

        return response_data


def get_player_club_data(api_header: dict, club_tag: str) -> dict:
    """Returns basic club data to include in plater stats"""

    club_tag = format_club_tag(club_tag)

    try:
        response = r.get(f"https://api.brawlstars.com/v1/clubs/%23{club_tag}", 
                         headers=api_header, tiemout=5)
        response_data = response.json()

    except:
        raise Exception("Error: Unable to retrieve club data")

    return response_data


def refine_player_club_data(club_data: dict) -> dict:
    """Refined club data to returns desired data (to display alonsgide player info)"""

    club_data_keys = ["name", "trophies",]
    club_members = len(club_data["members"])

    club_data = {k: v for k, v in club_data.items() if k in club_data_keys}
    club_data["members"] = club_members

    return club_data


def refine_player_stats(player_data: dict) -> dict:
    """Refined player data and returns chosen stats"""

    player_stats_keys = ["name", "trophies", "highestTrophies", "expLevel", "3vs3Victories",
                         "soloVictories", "duoVictories", "club"]

    player_stats = {to_snake_case(k): v for k, v in player_data.items() if k in player_stats_keys}


    return player_stats


def refine_player_brawlers(player_data: dict) -> list[dict]:
    """Refines player data on brawler's and return a list of all brawlers"""

    player_brawler_data = player_data["brawlers"]

    player_brawlers = []

    brawler_keys = ["name", "power", "rank", "trophies", "starPowers", "gadgets", "gears"]


    for item in player_brawler_data:

        brawler_data = {to_snake_case(k): v for k, v in item.items() if k in brawler_keys}
        brawler_data["name"] = brawler_data["name"].title()

        for gear in brawler_data["gears"]:
            gear["name"] = gear["name"].title()

        for star_power in brawler_data["star_powers"]:
            star_power["name"] = star_power["name"].title()

        for gadget in brawler_data["gadgets"]:
            gadget["name"] = gadget["name"].title()

        player_brawlers.append(brawler_data)

    return player_brawlers


if __name__ =="__main__":

    load_dotenv()

    config = environ

    token = config["api_token"]

    api_header_data = get_api_header(token)

    #Curently using my playerID
    player_data = get_player_data(api_header_data, "8QC8RP02")

    player_stats = refine_player_stats(player_data)
    player_brawler_data = refine_player_brawlers(player_data)

    player_club_tag = format_club_tag(player_stats["club"]["tag"])

    player_club_data = get_player_club_data(api_header=api_header_data, club_tag=player_club_tag)
    player_club_data = refine_player_club_data(player_club_data)

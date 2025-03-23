"""Scripts that return info for all brawlers"""

from os import environ

import requests as r
from dotenv import load_dotenv


def get_api_header(api_token: str) -> dict:
    """Returns api header data"""

    header = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    return header


def get_all_brawler_data(api_header: dict) -> list[dict]:
    """returns all brawler data"""

    try:
        response = r.get("https://api.brawlstars.com/v1/brawlers", headers=api_header, timeout=5)
        response_data = response.json()
        brawler_data_all = response_data["items"]

    except:
        raise ConnectionError("Error: Unable to return brawler data")

    return brawler_data_all


def transform_all_brawler_names(brawler_data: list[dict]) -> list[str]:
    """Returns all brawler names from complete list of all brawler data"""

    if not isinstance(brawler_data, list):
        raise TypeError("Error: Brawler data is not a list!")

    if not brawler_data:
        raise ValueError("Error: Bralwer list is empty!")

    all_brawler_names = [brawler["name"].title() for brawler in brawler_data]

    for brawler_name in all_brawler_names:
        if not brawler_name:
            raise ValueError("Error: Brawler name is empty")

    return all_brawler_names


def all_brawler_ids(brawler_data: list[dict]) -> list[int]:
    """Returns all brawler id's"""

    return [brawler["id"] for brawler in brawler_data]


def refine_brawler_data(brawler_data: dict) -> dict:
    """Returns refined brawler data for a specific brawler to be used in frontend"""

    if not isinstance(brawler_data, dict):
        raise TypeError("Error: 'brawler data' parameter is not an object.")

    brawler_data_refined =  {}

    brawler_data_refined["id"] = brawler_data["id"]
    brawler_data_refined["name"] = brawler_data["name"].capitalize()
    brawler_data_refined["star_powers"] = [key["name"].capitalize()
                                           for key in brawler_data["starPowers"]]
    brawler_data_refined["gadgets"] = [key["name"].capitalize() for key in brawler_data["gadgets"]]

    return brawler_data_refined


if __name__ =="__main__":

    load_dotenv()

    config = environ

    token = config["api_token"]

    api_header_data = get_api_header(token)

    all_brawler_data = get_all_brawler_data(api_header_data)

    brawlers_refined = []

    for brawler in all_brawler_data:
        brawlers_refined.append(refine_brawler_data(brawler))

"""Extract script to extract data from brawl API and database"""

from os import environ

import psycopg2
import requests
import pandas as pd
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


## Non extraction functions

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

    if len(player_tag) < 3:
        return False

    allowed_characters = ['P', 'Y', 'L', 'Q', 'G', 'O', 'R', 'J', 'C', 'U', 'V', '0', '2', '8', '9']

    for character in player_tag:
        if character not in allowed_characters:
            return False

    return True


## Database Extraction
def get_db_connection(config_env) -> connection:
    """Establishes connection with the database"""

    try:
        db_connection = psycopg2.connect(dbname = config_env["dbname"],
                         user = config_env["user"],
                         password = config_env["password"],
                         host = config_env["host"],
                         port = config_env["port"]
        )

    except Exception as exc:
        raise psycopg2.DatabaseError("Error: Cannot establish connection to database!") from exc

    return db_connection


def get_most_recent_brawler_starpowers(db_connection: connection) -> pd.DataFrame:
    """Returns most recent brawler starpowers in database"""

    with db_connection.cursor(cursor_factory=RealDictCursor) as cur:
        try:
            cur.execute("""SELECT DISTINCT b.brawler_id, b.brawler_name,
                        sp.starpower_id, sp.starpower_version, sp.starpower_name
                        FROM brawler b
                        INNER JOIN (SELECT b_2.brawler_id, MAX(b_2.brawler_version) AS brawler_version
                                    FROM brawler b_2
                                    GROUP BY b_2.brawler_id) b_max
                        ON b.brawler_id = b_max.brawler_id 
                        AND b.brawler_version = b_max.brawler_version
                        INNER JOIN starpower sp ON b.brawler_id = sp.brawler_id
                        INNER JOIN (SELECT sp_2.starpower_id, MAX(sp_2.starpower_version) AS starpower_version
                                    FROM starpower sp_2
                                    GROUP BY sp_2.starpower_id) sp_max
                        ON sp.starpower_id = sp_max.starpower_id
                        AND sp.starpower_version = sp_max.starpower_version
                        GROUP BY b.brawler_id, b.brawler_version, b.brawler_name,
                        sp.starpower_id, sp.starpower_version, sp.starpower_name;""")

            most_recent_brawler_data = cur.fetchall()

        except Exception as exc:
            raise psycopg2.DatabaseError("Error: Unable to retrieve data from database!") from exc

    most_recent_brawler_data_df = pd.DataFrame(data=most_recent_brawler_data,
                                               columns=("brawler_id", "brawler_name",
                                                        "starpower_id", "starpower_version",
                                                        "starpower_name"))

    return most_recent_brawler_data_df


def get_most_recent_brawler_gadgets(db_connection: connection) -> pd.DataFrame:
    """Returns most recent brawler gadgets in database"""

    with db_connection.cursor(cursor_factory=RealDictCursor) as cur:
        try:
            cur.execute("""SELECT DISTINCT b.brawler_id, b.brawler_name,
                        g.gadget_id, g.gadget_version, g.gadget_name
                        FROM brawler b
                        INNER JOIN (SELECT b_2.brawler_id, MAX(b_2.brawler_version) AS brawler_version
                                    FROM brawler b_2
                                    GROUP BY b_2.brawler_id) b_max
                        ON b.brawler_id = b_max.brawler_id 
                        AND b.brawler_version = b_max.brawler_version
                        INNER JOIN gadget g ON b.brawler_id = g.brawler_id 
                        INNER JOIN (SELECT g_2.gadget_id, MAX(g_2.gadget_version) AS gadget_version
                                    FROM gadget g_2
                                    GROUP BY g_2.gadget_id) g_max
                        ON g.gadget_id = g_max.gadget_id
                        AND g.gadget_version = g_max.gadget_version
                        GROUP BY b.brawler_id, b.brawler_version, b.brawler_name,
                        g.gadget_id, g.gadget_version, g.gadget_name;""")

            most_recent_brawler_data = cur.fetchall()

        except Exception as exc:
            raise psycopg2.DatabaseError("Error: Unable to retrieve data from database!") from exc

    most_recent_brawler_data_df = pd.DataFrame(data=most_recent_brawler_data,
                                               columns=("brawler_id", "brawler_name",
                                               "gadget_id", "gadget_version",
                                               "gadget_name"))

    return most_recent_brawler_data_df


def get_most_recent_brawler_version(db_connection: connection, brawler_id: int) -> int:
    """Returns most recent brawler version"""

    if not isinstance(brawler_id, int):
        raise TypeError("Error: Brawler is is not an integer!")

    try:
        with db_connection.cursor() as cur:
            cur.execute("""SELECT MAX(brawler_version)
                        FROM brawler
                        WHERE brawler_id = %s;""",[brawler_id])
            max_brawler_version = cur.fetchone()[0]

    except Exception as exc:
        raise psycopg2.DatabaseError("Error: Unavle to retrieve data from database!") from exc

    if not max_brawler_version:
        return 0
    return max_brawler_version


def get_most_recent_starpower_version(db_connection: connection, starpower_id: int) -> int:
    """Returns most recent star power version"""

    if not isinstance(starpower_id, int):
        raise TypeError("Error: Star power is is not an integer!")

    try:
        with db_connection.cursor() as cur:
            cur.execute("""SELECT MAX(starpower_version)
                        FROM starpower
                        WHERE starpower_id = %s;""",[starpower_id])
            max_starpower_version = cur.fetchone()[0]

    except Exception as exc:
        raise psycopg2.DatabaseError("Error: Unavle to retrieve data from database!") from exc

    if not max_starpower_version:
        return 0
    return max_starpower_version


def get_most_recent_gadget_version(db_connection: connection, gadget_id: int) -> int:
    """Returns most recent gadget version"""

    if not isinstance(gadget_id, int):
        raise TypeError("Error: Gadget id is not an integer!")

    try:
        with db_connection.cursor() as cur:
            cur.execute("""SELECT MAX(gadget_version)
                        FROM gadget
                        WHERE gadget_id = %s;""", [gadget_id])
            max_gadget_version = cur.fetchone()[0]

    except Exception as exc:
        raise psycopg2.DatabaseError("Error: Unavle to retrieve data from database!") from exc

    if not max_gadget_version:
        return 0
    return max_gadget_version


def get_most_recent_brawler_data(db_connection: connection) -> pd.DataFrame:
    """Returns most recent brawler data in database"""

    with db_connection.cursor(cursor_factory=RealDictCursor) as cur:
        try:
            cur.execute("""SELECT DISTINCT b.brawler_id, b.brawler_name
                        FROM brawler b
                        INNER JOIN (SELECT b_2.brawler_id, MAX(b_2.brawler_version) AS brawler_version
                                    FROM brawler b_2
                                    GROUP BY b_2.brawler_id) b_max
                        ON b.brawler_id = b_max.brawler_id 
                        AND b.brawler_version = b_max.brawler_version
                        GROUP BY b.brawler_id, b.brawler_version, b.brawler_name;""")

            most_recent_brawler_data = cur.fetchall()

        except Exception as exc:
            raise psycopg2.DatabaseError("Error: Unable to retrieve data from database!") from exc

    most_recent_brawler_data_df = pd.DataFrame(data=most_recent_brawler_data,
                                               columns=("brawler_id", "brawler_name"))
    return most_recent_brawler_data_df


def extract_brawler_data_database(config_env) -> list[dict]:
    """Extracts brawler data from database"""

    db_connection = get_db_connection(config_env)

    most_recent_brawler_data_database = get_most_recent_brawler_data(db_connection)

    return most_recent_brawler_data_database


## API Extraction
def get_api_header(api_token: str) -> dict:
    """Returns api header data"""

    header = {
        # "Accept": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    return header


def get_all_brawler_data(api_header_data: dict) -> list[dict]:
    """Returns all brawler data"""

    try:
        response = requests.get("https://api.brawlstars.com/v1/brawlers",
                                headers=api_header_data, timeout=5)
        response_data = response.json()

    except Exception as exc:
        raise ConnectionError("Error: Unable to return brawler data from API!") from exc

    brawler_data_all = response_data["items"]
    return brawler_data_all


def get_api_player_data(api_header_data: str, player_tag: str) -> dict:
    """Fetches player data from api"""

    player_tag = format_player_tag(player_tag)

    if not check_player_tag(player_tag):
        raise ValueError("Error: Player tag is invlaid!")

    try:
        response = requests.get(f"https://api.brawlstars.com/v1/players/%23{player_tag}",
                          headers=api_header_data, timeout=5)
        response_data = response.json()

    except Exception as exc:
        raise ConnectionError("Error: Unable to retrieve player data from API!") from exc

    return response_data


def get_api_player_battle_log(api_header_data: str, player_tag: str) -> dict:
    """Fetches player battle log data from api"""

    player_tag = format_player_tag(player_tag)

    if not check_player_tag(player_tag):
        raise ValueError("Error: Player tag is invlaid!")

    try:
        response = requests.get(f"https://api.brawlstars.com/v1/players/%23{player_tag}/battlelog",
                          headers=api_header_data, timeout=5)
        response_data = response.json()

    except Exception as exc:
        raise ConnectionError("Error: Unable to retrieve player data from API!") from exc

    return response_data


#TODO DRY 
def extract_brawler_data_api(config_env: dict) -> list[dict]:
    """Extracts brawler data by get request to the brawl API"""

    token = config_env["api_token"]
    api_header_data = get_api_header(token)
    all_brawler_data = get_all_brawler_data(api_header_data)

    return all_brawler_data


#TODO DRY
def extract_player_data_api(config_env: dict, player_tag: str) -> list[dict]:
    """Extracts brawler data by get request to the brawl API"""
    
    token = config_env["api_token"]
    api_header_data = get_api_header(token)
    all_player_data = get_api_player_data(api_header_data, player_tag)

    return all_player_data


#TODO DRY
def extract_player_battle_log_api(config_env: dict, player_tag: str) -> list[dict]:
    """Extracts brawler data by get request to the brawl API"""
    
    token = config_env["api_token"]
    api_header_data = get_api_header(token)
    all_player_data = get_api_player_battle_log(api_header_data, player_tag)

    return all_player_data


if __name__ =="__main__":

    load_dotenv()

    config = environ

    api_header = get_api_header(config["api_token"])
    bs_player_tag  = config["player_tag"]

    brawler_data_database = extract_brawler_data_database(config)

    brawler_data_api = extract_brawler_data_api(config)

    player_data = get_api_player_data(api_header, bs_player_tag)
    player_battle_log = get_api_player_battle_log(api_header, bs_player_tag)

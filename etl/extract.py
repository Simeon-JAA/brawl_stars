"""Extract script to extract data from brawl API and database"""

from os import environ
import sqlite3
from sqlite3 import Connection, Cursor, DatabaseError

import requests
import pandas as pd
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
def get_db_connection(config_env) -> Connection:
    """Establishes connection with the sqlite3 database"""

    try:
        db_connection = sqlite3.connect(database = config_env["dbpath"],
                                        timeout = 10)

    except Exception as exc:
        raise DatabaseError("Error: Cannot establish connection to database!") from exc

    return db_connection


def get_starpowers_latest_version(db_connection: Connection) -> pd.DataFrame:
    """Get lastest version of all starpowers from database"""


    try:
        cur = db_connection.cursor(factory=Cursor)
        cur.execute("""
            SELECT DISTINCT b.brawler_id, b.brawler_name,
            sp.starpower_id, sp.starpower_version, sp.starpower_name
            FROM brawler b
            INNER JOIN (
                SELECT b_2.brawler_id, MAX(b_2.brawler_version) AS brawler_version
                FROM brawler b_2
                GROUP BY b_2.brawler_id) b_max
            ON b.brawler_id = b_max.brawler_id 
            AND b.brawler_version = b_max.brawler_version
            INNER JOIN starpower sp ON b.brawler_id = sp.brawler_id
            INNER JOIN (
                SELECT sp_2.starpower_id, MAX(sp_2.starpower_version) AS starpower_version
                FROM starpower sp_2
                GROUP BY sp_2.starpower_id) sp_max
            ON sp.starpower_id = sp_max.starpower_id
            AND sp.starpower_version = sp_max.starpower_version
            GROUP BY b.brawler_id, b.brawler_version, b.brawler_name,
            sp.starpower_id, sp.starpower_version, sp.starpower_name;""")

        starpowers_latest_version = cur.fetchall()

    except Exception as exc:
        raise DatabaseError("Error: Unable to retrieve data from database!") from exc

    starpowers_latest_version_df = pd.DataFrame(data=starpowers_latest_version,
                                                columns=("brawler_id", "brawler_name",
                                                         "starpower_id", "starpower_version", 
                                                         "starpower_name"))

    return starpowers_latest_version_df


def get_gadgets_latest_version(db_connection: Connection) -> pd.DataFrame:
    """Get latest version of all gadgets from database"""

    try:
        cur = db_connection.cursor(factory=Cursor)
        cur.execute("""
            SELECT DISTINCT b.brawler_id, b.brawler_name,
            g.gadget_id, g.gadget_version, g.gadget_name
            FROM brawler b
            INNER JOIN (
                SELECT b_2.brawler_id, MAX(b_2.brawler_version) AS brawler_version
                FROM brawler b_2
                GROUP BY b_2.brawler_id) b_max
            ON b.brawler_id = b_max.brawler_id 
            AND b.brawler_version = b_max.brawler_version
            INNER JOIN gadget g 
            ON b.brawler_id = g.brawler_id 
            INNER JOIN (
                SELECT g_2.gadget_id, MAX(g_2.gadget_version) AS gadget_version
                FROM gadget g_2
                GROUP BY g_2.gadget_id) g_max
            ON g.gadget_id = g_max.gadget_id
            AND g.gadget_version = g_max.gadget_version
            GROUP BY b.brawler_id, b.brawler_version, b.brawler_name,
            g.gadget_id, g.gadget_version, g.gadget_name;""")

        gadgets_latest_version = cur.fetchall()

    except Exception as exc:
        raise DatabaseError("Error: Unable to retrieve data from database!") from exc

    gadgets_latest_version_df = pd.DataFrame(data=gadgets_latest_version,
                                             columns=("brawler_id", "brawler_name",
                                                      "gadget_id", "gadget_version",
                                                      "gadget_name"))

    return gadgets_latest_version_df


def get_brawlers_latest_version(db_connection: Connection) -> pd.DataFrame:
    """Get latest version of all brawlers from database"""

    try:
        cur = db_connection.cursor(factory=Cursor)
        cur.execute("""
            WITH max_brawlers AS (
              SELECT *, ROW_NUMBER() OVER (PARTITION BY brawler_id ORDER BY brawler_version DESC) rn
              FROM brawler
            )
            SELECT brawler_id, brawler_name
            FROM max_brawlers mb
            WHERE rn = 1
            ORDER BY brawler_id;""")

        brawlers_latest_version = cur.fetchall()

    except Exception as exc:
        raise DatabaseError("Error: Unable to retrieve data from database!") from exc

    brawlers_latest_version_df = pd.DataFrame(data=brawlers_latest_version,
                                               columns=("brawler_id", "brawler_name"))
    return brawlers_latest_version_df


def get_events_latest_version(db_connection: Connection) -> pd.DataFrame:
    """Get latest version of all events from the database"""

    try:
        cur = db_connection.cursor(factory=Cursor)
        cur.execute("""
            SELECT e.bs_event_id, e.bs_event_version, e.mode, e.map
            FROM bs_event e
            INNER JOIN (
                SELECT e2.bs_event_id, MAX(e2.bs_event_version) AS bs_event_version
                FROM bs_event e2
                GROUP BY e2.bs_event_id) e_max
            ON e.bs_event_id = e_max.bs_event_id
            AND e.bs_event_version = e_max.bs_event_version
            GROUP BY e.bs_event_id, e.bs_event_version, e.mode, e.map;""")

        event_data_latest_version = cur.fetchall()

    except Exception as exc:
        raise DatabaseError("Error: Cannot retrieve event data from database!") from exc

    event_data_latest_version_df = pd.DataFrame(data=event_data_latest_version,
                                                columns=("bs_event_id", "bs_event_version",
                                                         "mode", "map")).rename(columns={
                                                             "bs_event_id": "event_id",
                                                             "bs_event_version": "event_version"})

    return event_data_latest_version_df[["event_id", "event_version", "mode", "map"]]


def get_brawler_latest_version_id(db_connection: Connection, brawler_id: int) -> int:
    """Gets latest version ID of a specified brawler"""

    if not isinstance(brawler_id, int):
        raise TypeError("Error: Brawler ID is not an integer!")

    try:
        cur = db_connection.cursor(factory=Cursor)
        cur.execute("""
            SELECT MAX(brawler_version)
            FROM brawler
            WHERE brawler_id = %s;""",[brawler_id])

        brawler_latest_version = cur.fetchone()[0]

    except Exception as exc:
        raise DatabaseError("Error: Unable to retrieve data from database!") from exc

    if not brawler_latest_version:
        return 0

    return brawler_latest_version


def get_starpower_latest_version_id(db_connection: Connection, starpower_id: int) -> int:
    """Get latest version ID of specified starpower"""

    if not isinstance(starpower_id, int):
        raise TypeError("Error: StarpowerID is not an integer!")

    try:
        cur = db_connection.cursor(factory=Cursor)
        cur.execute("""
            SELECT MAX(starpower_version)
            FROM starpower
            WHERE starpower_id = %s;""",[starpower_id])

        starpower_latest_version_id = cur.fetchone()[0]

    except Exception as exc:
        raise DatabaseError("Error: Unable to retrieve data from database!") from exc

    if not starpower_latest_version_id:
        return 0
    return starpower_latest_version_id


def get_gadget_latest_version_id(db_connection: Connection, gadget_id: int) -> int:
    """Get latest version ID of a specified gadget"""

    if not isinstance(gadget_id, int):
        raise TypeError("Error: Gadget ID is not an integer!")

    try:
        cur = db_connection.cursor(factory=Cursor)
        cur.execute("""
            SELECT MAX(gadget_version)
            FROM gadget
            WHERE gadget_id = %s;""", [gadget_id])
        gadget_latest_version_id = cur.fetchone()[0]

    except Exception as exc:
        raise DatabaseError("Error: Unable to retrieve data from database!") from exc

    if not gadget_latest_version_id:
        return 0

    return gadget_latest_version_id


## API Extraction
def get_api_header(api_token: str) -> dict:
    """Returns api header data"""

    header = {
        "Accept": "application/json",
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


def get_api_event_rotation_data(api_header_data: str) -> dict:
    """Sends get request to brawl stars api for event rotation data"""

    try:
        response = requests.get("https://api.brawlstars.com/v1/events/rotation",
                    headers=api_header_data, timeout=5)
        response_data = response.json()

    except Exception as exc:
        raise ConnectionError("Error: Unable to retrieve evebt rotation data from API!") from exc

    return response_data


#TODO DRY
def extract_brawler_data_api(config_env: dict) -> list[dict]:
    """Extracts brawler data by get request to the brawl API"""

    token = config_env["api_token"]
    api_header_data = get_api_header(token)
    all_brawler_data = get_all_brawler_data(api_header_data)

    return all_brawler_data


#TODO DRY
def extract_event_data_api(config_env:dict) -> list[dict]:
    """Extracts event rotation data from the brawl stars api """

    token = config_env["api_token"]
    api_header_data = get_api_header(token)
    event_rotation_data = get_api_event_rotation_data(api_header_data)

    return event_rotation_data


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

    conn = get_db_connection(config)

    # Extract - Brawler data database
    brawlers_db_df = get_brawlers_latest_version(conn)
    starpowers_db_df = get_starpowers_latest_version(conn)
    gadgets_db_df = get_gadgets_latest_version(conn)
    events_db_df = get_events_latest_version(conn)
    print(brawlers_db_df)

    # Extract - Brawler data database

    # api_header = get_api_header(config["api_token"])
    # bs_player_tag  = config["player_tag"]

    # brawler_data_api = extract_brawler_data_api(config)

    # player_data = get_api_player_data(api_header, bs_player_tag)
    # player_battle_log = get_api_player_battle_log(api_header, bs_player_tag)

    conn.close()

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
           WITH latest_starpowers AS (
              SELECT 
                *,
                ROW_NUMBER() OVER (PARTITION BY starpower_id ORDER BY starpower_version DESC) rn
                FROM starpower
            )
            SELECT 
              lsp.starpower_id, lsp.starpower_version, lsp.starpower_name,
                b.brawler_id, b.brawler_name
            FROM latest_starpowers lsp
            INNER JOIN brawler b
            ON lsp.brawler_id = b.brawler_id AND lsp.brawler_version = b.brawler_version
            WHERE rn = 1
            ORDER BY lsp.starpower_id;""")

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
           WITH latest_gadgets AS (
              SELECT 
                *,
                ROW_NUMBER() OVER (PARTITION BY gadget_id ORDER BY gadget_version DESC) rn
                FROM gadget
            )
            SELECT 
              lg.gadget_id, lg.gadget_version, lg.gadget_name,
                b.brawler_id, b.brawler_name
            FROM latest_gadgets lg
            INNER JOIN brawler b
            ON lg.brawler_id = b.brawler_id AND lg.brawler_version = b.brawler_version
            WHERE rn = 1
            ORDER BY lg.gadget_id;""")

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
            WITH latest_brawlers AS (
              SELECT *, ROW_NUMBER() OVER (PARTITION BY brawler_id ORDER BY brawler_version DESC) rn
              FROM brawler
            )
            SELECT lb.brawler_id, lb.brawler_name
            FROM latest_brawlers lb
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
            WITH latest_events AS (
              SELECT *, ROW_NUMBER() OVER (PARTITION BY bs_event_id ORDER BY bs_event_version DESC) rn
              FROM bs_event
            )
            SELECT le.bs_event_id, le.bs_event_version, le.mode, le.map
            FROM latest_events le
            WHERE rn = 1
            ORDER BY le.bs_event_id;""")

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


def get_most_recent_battle_log_time(db_connection: connection, player_tag: str):
    """Returns most recent battle log time for a 
    given player tag from the database"""

    with db_connection.cursor(cursor_factory=RealDictCursor) as cur:
        try:
            cur.execute("""SELECT MAX(battle_time) AS most_recent_battle_time
                        FROM battle
                        WHERE player_tag = %s
                        LIMIT 1;""", [player_tag])
            
        except Exception as exc:
            raise psycopg2.DatabaseError("Error: Unable to retrieve data from database!") from exc
        else:
            most_recent_battle_log_time = cur.fetchone()
            return most_recent_battle_log_time["most_recent_battle_time"]
            

def get_distinct_battle_types(db_connection: connection) -> list[str]:
    """Returns distinct battle types from the database"""

    with db_connection.cursor() as cur:
        try:
            cur.execute("""SELECT DISTINCT battle_type_name
                        FROM battle_type;""")

        except Exception as exc:
            raise psycopg2.DatabaseError("Error: Unable to retrieve data from database!") from exc

        else:
            battle_types = cur.fetchall()
            return battle_types


def get_distinct_event_ids(db_connection: connection) -> list[int]:
    """Returns distinct event ids from the database"""

    with db_connection.cursor() as cur:
        try:
            cur.execute("""SELECT DISTINCT bs_event_id
                        FROM bs_event;""")

        except Exception as exc:
            raise psycopg2.DatabaseError("Error: Unable to retrieve data from database!") from exc

        else:
            bs_event_ids = cur.fetchall()
            return bs_event_ids


def extract_brawler_data_database(config_env) -> list[dict]:
    """Extracts brawler data from database"""
    
    return

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

    # Extract - Brawler data api
    api_header = get_api_header(config["api_token"])
    bs_player_tag  = config["player_tag"]

    brawler_data_api = extract_brawler_data_api(config)

    player_data = get_api_player_data(api_header, bs_player_tag)
    player_battle_log = get_api_player_battle_log(api_header, bs_player_tag)

    conn.close()

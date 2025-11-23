"""Load file for loading changes into database"""

from os import environ
import sqlite3
from sqlite3 import Connection, Cursor, DatabaseError, Error

from dotenv import load_dotenv
from pandas import DataFrame


def get_db_connection(config_env) -> Connection:
    """Establish connection with the sqlite3 database"""

    try:
        db_conn = sqlite3.connect(database=config_env["dbpath"],
                                  timeout=10)

    except Exception as exc:
        raise Error("Error: Cannot establish connection to database!") from exc

    return db_conn


def insert_brawler_db(db_conn: Connection, brawler_data: DataFrame):
    """Insert new brawler data into the database"""

    if not isinstance(brawler_data, DataFrame):
        raise TypeError("Error: Brawler data is not a dataframe!")
    if brawler_data.empty:
        return

    for index, brawler in brawler_data.iterrows():
        try:
            cur = db_conn.cursor(factory=Cursor)
            cur.execute("""INSERT INTO brawler
                        (brawler_id, brawler_version, brawler_name)
                        VALUES (?, ?, ?);""", [brawler["brawler_id"],
                                                  brawler["brawler_version"] + 1,
                                                  brawler["brawler_name"]])

        except Exception as exc:
            raise DatabaseError("Error: Unable to insert brawler data!") from exc

    
def insert_new_battle_type_data(db_conn: Connection, battle_type: str):
    """Inserts new battle type data into the database"""

    with db_conn.cursor(factory=Cursor) as cur:
        try:
            cur.execute("""INSERT INTO battle_type
                        (battle_type_name)
                        VALUES (%s);""",[battle_type])

        except Exception as exc:
            raise DatabaseError("Error: Unable to insert data into database!") from exc


def insert_new_starpower_data(db_conn: Connection, starpower_data: DataFrame):
    """Inserts new starpower data into the database"""

    if not isinstance(starpower_data, DataFrame):
        raise TypeError("Error: Starpower data is not a dataframe!")
    if starpower_data.empty:
        return

    for index, starpower in starpower_data.iterrows():
        try:
            cur = db_conn.cursor(factory=Cursor)
            cur.execute("""INSERT INTO starpower
                        (starpower_id, starpower_version, starpower_name, brawler_id, brawler_version)
                        VALUES (?, ?, ?, ?, ?);""",
                        [starpower["starpower_id"],
                          starpower["starpower_version"] + 1,
                          starpower["starpower_name"],
                          starpower["brawler_id"],
                          starpower["brawler_version"]])

        except Exception as exc:
            raise DatabaseError("Error: Unable to insert starpower data!") from exc


def insert_new_gadget_data(db_conn: Connection, gadget_data: DataFrame):
    """Insert gadget data into the database"""

    if not isinstance(gadget_data, DataFrame):
        raise TypeError("Error: Gadget data is not a dataframe!")
    if gadget_data.empty:
        return

    for index, gadget in gadget_data.iterrows():
        try:
            cur = db_conn.cursor(factory=Cursor)
            cur.execute("""INSERT INTO gadget
                        (gadget_id, gadget_version, gadget_name, brawler_id, brawler_version)
                        VALUES (?, ?, ?, ?, ?);""",
                        [gadget["gadget_id"],
                          gadget["gadget_version"] + 1,
                          gadget["gadget_name"],
                          gadget["brawler_id"],
                          gadget["brawler_version"]])

        except Exception as exc:
            raise DatabaseError("Error: Unable to insert gadget data!") from exc


def insert_player_db(db_conn: Connection, player_data: dict):
    """Insert player data into database"""

    try:
        cur =  db_conn.cursor(factory=Cursor)
        cur.execute("""INSERT INTO player
                    (player_tag)
                    VALUES
                    (%s)""", player_data["tag"])

    except Exception as exc:
        raise DatabaseError("Error: Unable to insert player data!") from exc


def insert_player_name_db(db_conn: Connection, player_data: dict):
    """Insert data into player_name table"""

    try:
        cur = db_conn.cursor(factory=Cursor)
        cur.execute("""INSERT INTO player_name
                    (player_tag, player_name, player_name_version)
                    VALUES
                    (%s)""", player_data["tag"])

    except Exception as exc:
        raise DatabaseError("Error: Unable to insert player data!") from exc


def insert_battle_log_db(db_conn: Connection, battle_log_data: dict):
    """Insert battle log data into database"""

    try:
        cur = db_conn.cursor(factory=Cursor)

        for battle in battle_log_data:
            cur.execute("""INSERT INTO battle
                        (player_tag, battle_time, event_id, result,
                        duration, trophy_change, brawler_played_id, star_player)
                        VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s);""",
                        [battle["player_tag"], battle["time"], battle["event_id"],
                          battle["result"], battle["duration"], battle["trophy_change"],
                          battle["brawler_id"], battle["star_player"]])

    except Exception as exc:
        raise DatabaseError("Error: Unable to insert battle log data!") from exc
    
    finally:
        cur.close()


def insert_new_event_data(db_conn: Connection, event_log_data: DataFrame):
    """Insert event data into the database"""

    if not isinstance(event_log_data, DataFrame):
        raise TypeError("Error: Event log data is not a dataframe!")
    if event_log_data.empty:
        return

    try:
        cur = db_conn.cursor(factory=Cursor)
        
        for index, event in event_log_data.iterrows():
            cur.execute("""INSERT INTO bs_event
                        (bs_event_id, bs_event_version, mode, map)
                        VALUES
                        (?, ?, ?, ?);""",
                        [event["event_id"], event["event_version"],
                          event["mode"], event["map"]])

    except Exception as exc:
        raise DatabaseError("Error inserting event data into database!") from exc


if __name__ =="__main__":

    load_dotenv()

    config = environ

    conn = get_db_connection(config)

    conn.close()

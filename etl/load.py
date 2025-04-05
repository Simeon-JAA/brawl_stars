"""Load file for loading changes into database"""

from os import environ

import psycopg2
from psycopg2.extensions import connection
from dotenv import load_dotenv
from pandas import DataFrame


def get_db_connection(config_env) -> connection:
    """Establishes connection with the database"""

    try:
        db_conn = psycopg2.connect(dbname = config_env["dbname"],
                         user = config_env["user"],
                         password = config_env["password"],
                         host = config_env["host"],
                         port = config_env["port"]
        )

    except Exception as exc:
        raise ConnectionError("Error: Cannot establish connection to database!") from exc

    return db_conn


def insert_new_brawler_data(db_conn: connection, brawler_data: DataFrame):
    """Inserts new brawler data into the database"""

    if not isinstance(brawler_data, DataFrame):
        raise TypeError("Error: Brawler data is not a dataframe!")
    if brawler_data.empty:
        return

    for index, brawler in brawler_data.iterrows():
        with db_conn.cursor() as cur:
            try:
                cur.execute("""INSERT INTO brawler
                            (brawler_id, brawler_version, brawler_name)
                            VALUES (%s, %s, %s);""", [brawler["brawler_id"],
                                                      brawler["brawler_version"],
                                                      brawler["brawler_name"]])
            except Exception as exc:
                raise psycopg2.DatabaseError("Error: Unable to insert brawler data!") from exc


def insert_new_starpower_data(db_conn: connection, starpower_data: DataFrame):
    """Inserts new starpower data into the database"""

    if not isinstance(starpower_data, DataFrame):
        raise TypeError("Error: Starpower data is not a dataframe!")
    if starpower_data.empty:
        return

    with db_conn.cursor() as cur:
        for index, starpower in starpower_data.iterrows():
            try:
                cur.execute("""INSERT INTO starpower
                            (starpower_id, starpower_version, starpower_name, brawler_id, brawler_version)
                            VALUES (%s, %s, %s, %s, %s);""",
                            [starpower["starpower_id"],
                             starpower["starpower_version"] + 1,
                             starpower["starpower_name"],
                             starpower["brawler_id"],
                             starpower["brawler_version"]])
            except Exception as exc:
                raise psycopg2.DatabaseError("Error: Unable to insert starpower data!") from exc


def insert_new_gadget_data(db_conn: connection, gadget_data: DataFrame):
    """Inserts new gadget data into the database"""

    if not isinstance(gadget_data, DataFrame):
        raise TypeError("Error: Gadget data is not a dataframe!")
    if gadget_data.empty:
        return

    with db_conn.cursor() as cur:
        for index, gadget in gadget_data.iterrows():
            try:
                cur.execute("""INSERT INTO gadget
                            (gadget_id, gadget_version, gadget_name, brawler_id, brawler_version)
                            VALUES (%s, %s, %s, %s, %s);""",
                            [gadget["gadget_id"],
                             gadget["gadget_version"] + 1,
                             gadget["gadget_name"],
                             gadget["brawler_id"],
                             gadget["brawler_version"]])
            except Exception as exc:
                raise psycopg2.DatabaseError("Error: Unable to insert gadget data!") from exc


def insert_new_player_data(db_conn: connection, player_data: dict):
    """Insert new data into player table"""

    with db_conn.cursor() as cur:
        try:
            cur.execute("""INSERT INTO player 
                        (player_tag)
                        VALUES
                        (%s)""", player_data["tag"])
        except Exception as exc:
            raise psycopg2.DatabaseError("Error: Unable to insert player data!")


def insert_new_player_name(db_conn: connection, player_data: dict):
    """Insert new data into player_name table"""

    with db_conn.cursor() as cur:
        try:
            cur.execute("""INSERT INTO player_name 
                        (player_tag, player_name, player_name_version)
                        VALUES
                        (%s)""", player_data["tag"])
        except Exception as exc:
            raise psycopg2.DatabaseError("Error: Unable to insert player data!")


if __name__ =="__main__":

    load_dotenv()

    config = environ

    conn = get_db_connection(config)

    conn.close()

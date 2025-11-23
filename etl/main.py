"""Main.py will on a schedule and will run ETLs"""

from os import environ
from sqlite3 import Connection, Cursor, DatabaseError
from datetime import datetime as dt

from dotenv import load_dotenv

from extract import (extract_brawler_data_api, get_brawlers_latest_version,
                     get_gadgets_latest_version, get_starpowers_latest_version,
                     get_events_latest_version, extract_player_battle_log_api,
                     get_db_connection, extract_event_data_api)
from transform import (transform_brawl_data_api, generate_starpower_changes,
                       brawl_api_data_to_df, add_starpower_changes_version,
                       generate_gadget_changes, add_gadget_changes_version,
                       generate_brawler_changes, add_brawler_changes_version,
                       transform_player_data_api, transform_battle_log_api,
                       transform_event_data_api, generate_event_changes)
from load import (insert_brawler_db, insert_new_starpower_data, insert_new_gadget_data,
                  insert_new_event_data)


def get_process_id(conn: Connection, process_name: str) -> int:
    """Get process ID from database"""

    cur = conn.cursor(factory = Cursor)

    try:
        cur.execute(
            """SELECT process_id
            FROM process 
            WHERE process_name = ?;""", [process_name])
        process_id = cur.fetchone()

        if process_id:
            return process_id[0]

    except Exception as e:
        raise DatabaseError (f"Database error occurred: {e}") from e


def update_process_log(conn: Connection, process_id: int, process_status: str) -> None:
    """Update process log in database"""

    cur = conn.cursor(factory = Cursor)

    try:
        cur.execute(
            """INSERT INTO process_log
            (process_id, process_status)
            VALUES (?, ?);""",
            [process_id, process_status]
        )
        
        conn.commit()

    except DatabaseError as e:
        raise DatabaseError (f"Database error occurred: {e}") from e


def get_last_process_id_run(conn: Connection, process_id: int) -> dt:
    """Get last run time of a process from database"""

    cur = conn.cursor(factory = Cursor)

    try:
        cur.execute(
            """SELECT last_updated
            FROM process_log
            WHERE process_id = ?
            ORDER BY last_updated DESC
            LIMIT 1;""", [process_id])
        
        last_run = cur.fetchone()

        if last_run:
            return dt.fromisoformat(last_run[0])

    except Exception as e:
        raise DatabaseError (f"Database error occurred: {e}") from e


def etl_brawler(conn: Connection):
    """ETL for brawler data"""


    #Update Process Log - Start
    process_id = get_process_id(conn, "Brawler ETL")
    update_process_log(conn, process_id, "Start")
    conn.commit()

    # Extract - Brawler data
    brawler_data_database_df = get_brawlers_latest_version(conn)
    brawler_starpower_data_database_df = get_starpowers_latest_version(conn)
    brawler_gadget_data_database_df = get_gadgets_latest_version(conn)
    event_data_database_df = get_events_latest_version(conn)
    brawler_data_api = extract_brawler_data_api(config)
    event_data_api = extract_event_data_api(config)

    # Transform
    brawler_data_api = transform_brawl_data_api(brawler_data_api)
    brawler_data_api_df = brawl_api_data_to_df(brawler_data_api)
    brawler_starpower_data_api_df = brawl_api_data_to_df(brawler_data_api, "star_powers")
    brawler_gadget_data_api_df = brawl_api_data_to_df(brawler_data_api, "gadgets")
    event_data_api = transform_event_data_api(event_data_api)

    # Changes
    brawler_changes_df = generate_brawler_changes(brawler_data_database_df, brawler_data_api_df)
    brawler_changes_df = add_brawler_changes_version(conn, brawler_changes_df)
    event_changes_df = generate_event_changes(event_data_database_df, event_data_api)
    # Insert brawler updates/new data
    # This is required as brawler_version is pulled into
    # other dataframes, so this should be updated first so the most recent version is pulled)
    insert_brawler_db(conn, brawler_changes_df)

    starpower_changes_df = generate_starpower_changes(brawler_starpower_data_database_df,
                                                    brawler_starpower_data_api_df)
    starpower_changes_df = add_starpower_changes_version(conn, starpower_changes_df)

    gadget_changes_df = generate_gadget_changes(brawler_gadget_data_database_df,
                                                brawler_gadget_data_api_df)
    gadget_changes_df = add_gadget_changes_version(conn, gadget_changes_df)

    # Load
    insert_new_starpower_data(conn, starpower_changes_df)
    insert_new_gadget_data(conn, gadget_changes_df)
    insert_new_event_data(conn, event_changes_df)

    #Update Process Log - End
    update_process_log(conn, process_id, "End")

    conn.commit()


def run_etl(last_run: dt, threshold_mins: int) -> bool:  
    """Run ETL if last run was more than threshold"""

    if last_run is None:
        return True

    time_diff = int((dt.now() - last_run).total_seconds()/60)
    
    return True if time_diff >= threshold_mins else False


def etl_player():
    """ETL for player data"""

    load_dotenv()
    config = environ
    bs_player_tag = config["player_tag"]

    player_battle_log_api = extract_player_battle_log_api(config, bs_player_tag)
    player_data_api = transform_player_data_api(player_data_api)


def etl_battle_log():
    """ETL for player battle log"""

    load_dotenv()
    config = environ
    bs_player_tag = config["player_tag"]

    player_battle_log_api = extract_player_battle_log_api(config, bs_player_tag)
    player_battle_log_api = transform_battle_log_api(player_battle_log_api, bs_player_tag)
    for battle in player_battle_log_api:
        print(battle)


if __name__ =="__main__":
    
    load_dotenv()

    config = environ

    try:
        conn = get_db_connection(config)
        brawl_process_id = get_process_id(conn, "Brawler ETL")
        latest_brawler_etl = get_last_process_id_run(conn, brawl_process_id)

    except DatabaseError as e:
        raise DatabaseError(f"Database connection failed: {e}") from e

    if run_etl(latest_brawler_etl, 60):
        try:
            etl_brawler(conn)
        except Exception as e:
            raise ChildProcessError(f"ETL failed at {dt.now()}. {e}") from e
    else:
        print(f"ETL skipped at {dt.now()}. Last run was at {latest_brawler_etl}")
    # finally:
    #     print(f"ETL finished at {dt.now()}")

    # etl_battle_log()

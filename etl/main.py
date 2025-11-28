"""Main.py will on a schedule and will run ETLs"""

from os import environ
from sqlite3 import Connection, Cursor, DatabaseError
from datetime import datetime as dt

from dotenv import load_dotenv

from extract import (extract_brawler_data_api, get_brawlers_latest_version,
                     get_gadgets_latest_version, get_starpowers_latest_version,
                     get_events_latest_version, extract_player_battle_log_api,
                     get_db_connection, extract_event_data_api, get_api_player_data,
                     get_player_id)
from transform import (transform_brawl_data_api, generate_starpower_changes,
                       brawl_api_data_to_df, add_starpower_changes_version,
                       generate_gadget_changes, add_gadget_changes_version,
                       generate_brawler_changes, add_brawler_changes_version,
                       transform_player_data_api, transform_battle_log_api,
                       transform_event_data_api, generate_event_changes)
from load import (insert_brawler_db, insert_new_starpower_data, insert_new_gadget_data,
                  insert_new_event_data, insert_new_player_db, insert_player_exp,
                  insert_player_trophies, insert_player_victories)


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
            AND process_status = 'Start'
            ORDER BY last_updated DESC
            LIMIT 1;""", [process_id])

        last_run = cur.fetchone()

        if last_run:
            return dt.fromisoformat(last_run[0])

    except Exception as e:
        raise DatabaseError (f"Database error occurred: {e}") from e


def run_etl(last_run: dt, threshold_mins: int) -> bool:
    """Return true if last run time is greater than or
    equal to threshold. Or if last run is None"""

    if last_run is None:
        return True

    time_diff = round((dt.now() - last_run).total_seconds()/60)

    return True if time_diff >= threshold_mins else False


def etl_brawler(conn: Connection, config_parameters: dict):
    """ETL for brawler data"""

    #Update Process Log - Start
    process_id = get_process_id(conn, "Brawler ETL")
    update_process_log(conn, process_id, "Start")
    conn.commit()

    try:

        # Extract - Brawler data
        brawler_data_database_df = get_brawlers_latest_version(conn)
        brawler_starpower_data_database_df = get_starpowers_latest_version(conn)
        brawler_gadget_data_database_df = get_gadgets_latest_version(conn)
        event_data_database_df = get_events_latest_version(conn)
        brawler_data_api = extract_brawler_data_api(config_parameters)
        event_data_api = extract_event_data_api(config_parameters)

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

    except Exception as exc:
        conn.rollback()
        update_process_log(conn, process_id, "Failed")
        raise ChildProcessError("Error within Brawler ETL process!") from exc

    finally:
        conn.commit()


def etl_player(conn: Connection, config_parameters: dict):
    """ETL for player data"""

    #Update Process Log - Start
    process_id = get_process_id(conn, "Player ETL")
    update_process_log(conn, process_id, "Start")
    conn.commit()

    #Get parameters from .env
    bs_player_tag = config_parameters["player_tag"]
    api_token = config_parameters["api_token"]

    try:
        #Extract
        player_data_api = get_api_player_data(api_token, bs_player_tag)
        player_id = get_player_id(conn, player_data_api)

        #Transform
        player_data_api = transform_player_data_api(player_data_api)

        #Load
        if player_id == 0:
            insert_new_player_db(conn, player_data_api)

        insert_player_exp(conn, player_id, player_data_api)
        insert_player_trophies(conn, player_id, player_data_api)
        insert_player_victories(conn, player_id, player_data_api)

        #Update Process Log - End
        update_process_log(conn, process_id, "End")

    except Exception as exc:
        conn.rollback()
        update_process_log(conn, process_id, "Failed")
        raise ChildProcessError("Error within Player ETL process!") from exc

    finally:
        conn.commit()


def etl_battle_log(conn: Connection, config_parameters: dict):
    """ETL for player battle log"""

    bs_player_tag = config_parameters["player_tag"]

    player_battle_log_api = extract_player_battle_log_api(config_parameters, bs_player_tag)
    player_battle_log_api = transform_battle_log_api(player_battle_log_api, bs_player_tag)
    for battle in player_battle_log_api:
        print(battle)


if __name__ =="__main__":

    load_dotenv()

    config = environ

    print(f"ETL started at {dt.now()}")

    ## Establish DB Connection and get last process run times
    try:
        db_conn = get_db_connection(config)

        brawl_process_id = get_process_id(db_conn, "Brawler ETL")
        player_process_id = get_process_id(db_conn, "Player ETL")

        latest_brawler_etl = get_last_process_id_run(db_conn, brawl_process_id)
        latest_player_etl = get_last_process_id_run(db_conn, player_process_id)

    except DatabaseError as exc:
        raise DatabaseError(f"Database connection failed: {exc}") from exc

    ## Run ETLs based on last run times
    ## Bralwer ETL - every 60 minutes
    if run_etl(latest_brawler_etl, 60):
        try:
            etl_brawler(db_conn, config)
        except Exception as exc:
            raise ChildProcessError(f"ETL failed at {dt.now()}. {exc}") from exc
    else:
        print(f"Brawler ETL skipped at {dt.now()}. Last run was at {latest_brawler_etl}")

    ## Player ETL - every 60 minutes
    if run_etl(latest_player_etl, 60):
        try:
            etl_player(db_conn, config)
        except Exception as exc:
            raise ChildProcessError(f"ETL failed at {dt.now()}. {exc}") from exc
    else:
        print(f"Player ETL skipped at {dt.now()}. Last run was at {latest_player_etl}")

    ## Close DB Connection
    db_conn.close()
    print(f"ETL finished at {dt.now()}")

"""Main pipeline file to ru full etl on brawler data into the database"""

from os import environ
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
from load import (insert_brawler_db, insert_starpower_db, insert_gadget_db,
                  insert_event_db)


def etl_brawler():
    """ETL for brawler data"""

    load_dotenv()
    config = environ
    conn = get_db_connection(config)

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
    # event_changes_df = generate_event_changes(event_data_database_df, event_data_api)
    # # Insert brawler updates/new data
    # # This is required as brawler_version is pulled into
    # # other dataframes, so this should be updated first so the most recent version is pulled)
    # insert_brawler_db(conn, brawler_changes_df)

    # starpower_changes_df = generate_starpower_changes(brawler_starpower_data_database_df,
    #                                                 brawler_starpower_data_api_df)
    # starpower_changes_df = add_starpower_changes_version(conn, starpower_changes_df)

    # gadget_changes_df = generate_gadget_changes(brawler_gadget_data_database_df,
    #                                             brawler_gadget_data_api_df)
    # gadget_changes_df = add_gadget_changes_version(conn, gadget_changes_df)

    # ## Load
    # insert_starpower_db(conn, starpower_changes_df)
    # insert_gadget_db(conn, gadget_changes_df)
    # insert_event_db(conn, event_changes_df)

    # conn.commit()
    conn.close()


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

    etl_brawler()

    # etl_battle_log()

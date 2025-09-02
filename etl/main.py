"""Main pipeline file to ru full etl on brawler data into the database"""

from os import environ
from datetime import datetime as dt

from dotenv import load_dotenv

from extract import (extract_brawler_data_api, get_most_recent_brawler_data,
                     get_most_recent_brawler_gadgets, get_most_recent_brawler_starpowers,
                     get_most_recent_event_data, extract_player_battle_log_api,
                     get_db_connection, extract_event_data_api)
from transform import (transform_brawl_data_api, generate_starpower_changes,
                       brawl_api_data_to_df, add_starpower_changes_version,
                       generate_gadget_changes, add_gadget_changes_version,
                       generate_brawler_changes, add_brawler_changes_version,
                       transform_player_data_api, transform_battle_log_api,
                       transform_event_data_api, generate_event_changes)
from load import (insert_new_brawler_data, insert_new_starpower_data, insert_new_gadget_data,
                  insert_new_event_data)


def etl_brawl_data(config):
    """ETL for general brawl data"""

    conn = get_db_connection(config)

    # Extract - Brawler & Event data
    brawler_data_database_df = get_most_recent_brawler_data(conn)
    brawler_starpower_data_database_df = get_most_recent_brawler_starpowers(conn)
    brawler_gadget_data_database_df = get_most_recent_brawler_gadgets(conn)
    event_data_database_df = get_most_recent_event_data(conn)
    brawler_data_api = extract_brawler_data_api(config)
    event_data_api = extract_event_data_api(config)

    # Transform - Brawler & Event data
    brawler_data_api = transform_brawl_data_api(brawler_data_api)
    brawler_data_api_df = brawl_api_data_to_df(brawler_data_api)
    brawler_starpower_data_api_df = brawl_api_data_to_df(brawler_data_api, "star_powers")
    brawler_gadget_data_api_df = brawl_api_data_to_df(brawler_data_api, "gadgets")
    event_data_api = transform_event_data_api(event_data_api)

    # Changes/Missing data
    brawler_changes_df = generate_brawler_changes(brawler_data_database_df, brawler_data_api_df)
    brawler_changes_df = add_brawler_changes_version(conn, brawler_changes_df)
    event_changes_df = generate_event_changes(event_data_database_df, event_data_api)
  
    # Insert brawler data
    # This is required as brawler_version is pulled into other dataframes
    # This should be updated first so the most recent version is pulled
    insert_new_brawler_data(conn, brawler_changes_df)

    starpower_changes_df = generate_starpower_changes(brawler_starpower_data_database_df,
                                                    brawler_starpower_data_api_df)
    starpower_changes_df = add_starpower_changes_version(conn, starpower_changes_df)

    gadget_changes_df = generate_gadget_changes(brawler_gadget_data_database_df,
                                                brawler_gadget_data_api_df)
    gadget_changes_df = add_gadget_changes_version(conn, gadget_changes_df)

    ## Load - Brawler & Event data
    insert_new_starpower_data(conn, starpower_changes_df)
    insert_new_gadget_data(conn, gadget_changes_df)
    insert_new_event_data(conn, event_changes_df)

    conn.commit()
    conn.close()


def etl_player(config):
    """ETL for player data"""

    bs_player_tag = config["player_tag"]
    conn = get_db_connection(config)

    player_battle_log_api = extract_player_battle_log_api(config, bs_player_tag)
    player_data_api = transform_player_data_api(conn, player_data_api)

    conn.close()


def etl_battle_log(config, bs_player_tag):
    """ETL for player battle log"""

    conn = get_db_connection(config)

    # Extract - Player battle log
    player_battle_log_api = extract_player_battle_log_api(config, bs_player_tag)

    # Transform - Player battle log
    player_battle_log_api = transform_battle_log_api(conn, player_battle_log_api, bs_player_tag)

    # Load - Player battle log
    conn.close()


if __name__ =="__main__":

    load_dotenv()
    config = environ

    # print(f"ETL pipeline -> Start @ {dt.now()}")
    # etl_brawl_data(config)
    # print(f"ETL pipeline -> End @ {dt.now()}")

    player_tag = config["player_tag"]
    player_tag = player_tag.replace("(", "").replace(")", "").replace("\"", "")
        # print(f"ETL battle log for {tag} -> Start @ {dt.now()}")
    etl_battle_log(config, player_tag)
        # print(f"ETL battle log for {tag} -> End @ {dt.now()}")

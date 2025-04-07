"""Transform script to clean data received by brawl API"""

import re
from datetime import datetime as dt

import pandas as pd
from pandas import DataFrame, concat
from psycopg2.extensions import connection

from extract import (get_most_recent_starpower_version, get_most_recent_gadget_version, 
                     get_most_recent_brawler_version)


def brawler_name_value_to_title(brawler_data: dict) -> dict:
    """Apply title() to all values for the 'name' key"""

    if not isinstance(brawler_data, dict):
        raise TypeError("Error: Brawler data is an incorrect type!")

    brawler_data_keys = ("name", "id", "starPowers", "gadgets")

    for key in brawler_data.keys():
        if key not in brawler_data_keys:
            raise KeyError("Error: Missing key from brawler data!")

    brawler_data["name"] = brawler_data["name"].title()

    for star_power in brawler_data["starPowers"]:
        star_power["name"] = star_power["name"].title()

    for gadget in brawler_data["gadgets"]:
        gadget["name"] = gadget["name"].title()

    return brawler_data


def to_snake_case(text: str) -> str:
    """Formats keys to snake_case"""

    if not isinstance(text, str):
        raise TypeError("Error: Text should be a string!")

    text = text.replace(" ", "")
    text = re.sub(r'([a-z\s]{1})([A-Z]{1})', r'\1_\2', text)

    if not text:
        raise ValueError("Error: Text cannot be blank!")

    return text.lower()


def to_title(text: str) -> str:
    """Formats camelCase test to title"""
    
    if "5v5" in text:
        text = text.replace("5V5", "5v5")

    text = to_snake_case(text).replace("_", " ").title()

    return text


def format_datetime(time_api_format: str) -> str:
    """Formats the datetime object recieved by the brawl stars api"""

    read_time_format = dt.strptime(time_api_format, "%Y%m%dT%H%M%S.%fZ")
    format_dt = read_time_format.strftime("%Y-%m-%d %H:%M:%S")
    
    return format_dt


def transform_brawl_data_api(brawl_data_api: list[dict]) -> list[dict]:
    """Transform and clean API brawl data"""

    brawl_data_keys = ("starPowers", "name", "gadgets", "id")

    for index, brawler in enumerate(brawl_data_api):

        brawler = brawler_name_value_to_title(brawler)
        brawler = {to_snake_case(k): v for k, v in brawler.items() if k in brawl_data_keys}
        brawl_data_api[index] = brawler

    return brawl_data_api


def transform_event_data_api(event_data_api: list[dict]) -> DataFrame:
    """Transforms event data recieved from api"""
    
    event_data_api = [event["event"] for event in event_data_api]
    event_data_api = list(map(lambda event_dict: {**event_dict, 
                                                  "mode": to_title(event_dict["mode"])},
                                                  event_data_api))
    event_data_api_df = DataFrame(event_data_api)
    return event_data_api_df


def get_new_exploded_column_names(column_name: str) -> list[str]:
    """Returns new column names for exploded column name"""

    new_column_names = []
    column_extensions = ("id", "name")

    for extension in column_extensions:
        new_column_names.append(f"{column_name[:-1]}_{extension}")

    return new_column_names


def brawl_api_data_to_df(brawl_data_api, explode_column: str = '') -> DataFrame:
    """Returns brawl api data as a dataframe"""

    if not explode_column:
        brawl_data_api_df = pd.DataFrame(data = brawl_data_api,
                                     columns = ["id", "name"])
        brawl_data_api_df_rename = brawl_data_api_df.rename(columns={'id': 'brawler_id',
                                                                     'name': 'brawler_name'})
        return brawl_data_api_df_rename

    brawl_data_api_df = pd.DataFrame(data = brawl_data_api,
                                     columns = ["id", "name", explode_column])
    brawl_data_api_df_exploded = brawl_data_api_df.explode(column=explode_column)
    brawl_data_api_df_exploded[get_new_exploded_column_names(explode_column)] = brawl_data_api_df_exploded[explode_column].apply(pd.Series)
    brawl_data_api_df_exploded = brawl_data_api_df_exploded.drop(columns = explode_column)
    brawl_data_api_df_exploded = brawl_data_api_df_exploded.reset_index(drop=True)
    brawl_data_api_df_rename_columns = brawl_data_api_df_exploded.rename(columns={
        "id": "brawler_id",
        "name": "brawler_name",
        "star_power_id": "starpower_id",
        "star_power_name": "starpower_name"})

    return brawl_data_api_df_rename_columns


def filter_star_powers(brawler_data: dict) -> dict:
    """Returns data required for updating star power"""

    keys = ("id", "name", "star_powers")

    return {k: v for k, v in brawler_data.items() if k in keys}


def add_brawler_changes_version(db_connection: connection, brawler_changes_df: DataFrame) -> DataFrame:
    """Creates new column in dataframe with most recent brawler version"""

    brawler_changes_df["brawler_version"] = brawler_changes_df["brawler_id"].apply(lambda brawler_id: get_most_recent_brawler_version(db_connection, brawler_id))

    return brawler_changes_df


def add_starpower_changes_version(db_connection: connection, starpower_changes_df: DataFrame) -> DataFrame:
    """Creates new column in dataframe with most recent starpower version"""

    starpower_changes_df["starpower_version"] = starpower_changes_df["starpower_id"].apply(lambda sp_id: get_most_recent_starpower_version(db_connection, sp_id))
    starpower_changes_df = add_brawler_changes_version(db_connection, starpower_changes_df)
    return starpower_changes_df


def add_gadget_changes_version(db_connection: connection, gadget_changes_df: DataFrame) -> DataFrame:
    """Creates new column in dataframe with most recent gadget version"""

    gadget_changes_df["gadget_version"] = gadget_changes_df["gadget_id"].apply(lambda gadget_id: get_most_recent_gadget_version(db_connection, gadget_id))
    gadget_changes_df = add_brawler_changes_version(db_connection, gadget_changes_df)
    return gadget_changes_df


def generate_starpower_changes(starpower_db_df: DataFrame, starpower_api_df: DataFrame) -> DataFrame:
    """Compares data between database and api for starpowers and returns the difference to be inserted"""

    starpower_data_to_load = DataFrame(columns={"brawler_id": [],
                                                "brawler_name": [],
                                                "starpower_id": [],
                                                "starpower_name": []})

    for brawler_id in starpower_api_df["brawler_id"].unique():

        db_starpower_data = starpower_db_df[["brawler_id", "brawler_name",
                                              "starpower_id", "starpower_name"]].loc[(starpower_db_df["brawler_id"] == brawler_id)]
        db_starpower_data = db_starpower_data.reset_index(drop=True).sort_index(axis=1)

        api_starpower_data = starpower_api_df.loc[(starpower_api_df["brawler_id"] == brawler_id)]
        api_starpower_data = api_starpower_data.reset_index(drop=True).sort_index(axis=1)

        if db_starpower_data.empty:
            starpower_data_to_load = concat([starpower_data_to_load, api_starpower_data], ignore_index=True)

        else:
            comparison_df = db_starpower_data.compare(other=api_starpower_data,
                                            keep_shape=True, keep_equal=True,
                                            result_names=("databse", "api"))

            differences_df = comparison_df.loc[(comparison_df.xs("databse",axis=1, level=1) != comparison_df.xs("api", axis=1, level=1)).any(axis=1)]
            differences_filtered_df = differences_df.xs("api", axis=1, level=1)

            starpower_data_to_load = concat([starpower_data_to_load, differences_filtered_df], ignore_index=True)

    return starpower_data_to_load


def generate_gadget_changes(gadget_db_df: DataFrame, gadget_api_df: DataFrame) -> DataFrame:
    """Compares data between database and api for gadgets and returns the difference to be inserted"""

    gadget_data_to_load = DataFrame(columns={"brawler_id": [],
                                                "brawler_name": [],
                                                "gadget_id": [],
                                                "gadget_name": []})

    for brawler_id in gadget_api_df["brawler_id"].unique():

        db_gadget_data = gadget_db_df[["brawler_id", "brawler_name",
                                              "gadget_id", "gadget_name"]].loc[(gadget_db_df["brawler_id"] == brawler_id)]
        db_gadget_data = db_gadget_data.reset_index(drop=True).sort_index(axis=1)

        api_gadget_data = gadget_api_df.loc[(gadget_api_df["brawler_id"] == brawler_id)]
        api_gadget_data = api_gadget_data.reset_index(drop=True).sort_index(axis=1)

        if db_gadget_data.empty:
            gadget_data_to_load = concat([gadget_data_to_load, api_gadget_data], ignore_index=True)

        else:
            comparison_df = db_gadget_data.compare(other=api_gadget_data,
                                            keep_shape=True, keep_equal=True,
                                            result_names=("databse", "api"))

            differences_df = comparison_df.loc[(comparison_df.xs("databse",axis=1, level=1) != comparison_df.xs("api", axis=1, level=1)).any(axis=1)]
            differences_filtered_df = differences_df.xs("api", axis=1, level=1)

            gadget_data_to_load = concat([gadget_data_to_load, differences_filtered_df], ignore_index=True)

    return gadget_data_to_load


def generate_brawler_changes(brawler_db_df: DataFrame, brawler_api_df: DataFrame) -> DataFrame:
    """Compares data between database and api for brawlers and returns the difference to be inserted"""

    brawler_data_to_load = DataFrame(columns={"brawler_id": [],
                                                "brawler_name": []})

    for brawler_id in brawler_api_df["brawler_id"].unique():

        db_brawler_data = brawler_db_df[["brawler_id",
                                         "brawler_name"]].loc[(brawler_db_df["brawler_id"] == brawler_id)]
        db_brawler_data = db_brawler_data.reset_index(drop=True).sort_index(axis=1)

        api_brawler_data = brawler_api_df.loc[(brawler_api_df["brawler_id"] == brawler_id)]
        api_brawler_data = api_brawler_data.reset_index(drop=True).sort_index(axis=1)

        if db_brawler_data.empty:
            brawler_data_to_load = concat([brawler_data_to_load, api_brawler_data], ignore_index=True)

        else:
            comparison_df = db_brawler_data.compare(other=api_brawler_data,
                                            keep_shape=True, keep_equal=True,
                                            result_names=("databse", "api"))

            differences_df = comparison_df.loc[(comparison_df.xs("databse",axis=1, level=1) != comparison_df.xs("api", axis=1, level=1)).any(axis=1)]
            differences_filtered_df = differences_df.xs("api", axis=1, level=1)

            brawler_data_to_load = concat([brawler_data_to_load, differences_filtered_df], ignore_index=True)

    return brawler_data_to_load


def transform_player_data_api(player_data: dict) -> dict:
    """Transforms player data to be uploaded to db"""

    desired_keys = ('tag', 'name', 'trophies', 'highestTrophies',
                    'expLevel', 'expPoints', 'isQualifiedFromChampionshipChallenge',
                    '3vs3Victories', 'soloVictories', 'duoVictories', 'bestRoboRumbleTime')
    
    player_data = {to_snake_case(k): v for k, v in player_data.items() if k in desired_keys}
  

    return player_data


def get_battle_log_brawler(battle_teams: list[list[dict]], player_tag: str) -> int:
    """Gets the bralwer played by the player for a specific battle"""
    
    all_teams = []
    for team in battle_teams:
        all_teams.extend(team)

    try:
        for player_data in all_teams:
            if player_data["tag"] == f"#{player_tag}":
                return player_data["brawler"]["id"]
    except Exception as exc:
      raise ValueError("Error: Player not found in battle log!")


def is_star_player(star_player_data: dict, player_tag: str) -> bool:
    """Returns true if star player and false if not"""

    
    if star_player_data["tag"] == None:
        return False
    elif star_player_data["tag"] == f"#{player_tag}":
        return True
    else:
        return False


def transform_battle_log_api(battle_log_data: list[dict], player_tag: str) -> dict:
    """Transforms player battle log and returns desired values"""

    battle_log = []

    for battle in battle_log_data["items"]:
        battle_to_append = {}
        battle_to_append["battle_player_tag"] = player_tag
        battle_to_append["battle_time"] = format_datetime(battle["battleTime"])
        battle_to_append["battle_mode_id"] = battle["event"]["id"]
        battle_to_append["battle_map"] = battle["event"]["map"].title()
        battle_to_append["battle_type"] = battle["battle"]["type"].title()
        battle_to_append["battle_result"] = battle["battle"]["result"].title()
        battle_to_append["battle_duration"] = battle["battle"]["duration"]
        if "trophyChange" not in battle["battle"].keys():
            battle_to_append["battle_trophy_change"] = None
        else:
            battle_to_append["battle_trophy_change"] = battle["battle"]["trophyChange"]
        battle_to_append["brawler_id"] = get_battle_log_brawler(battle["battle"]["teams"], player_tag)
        battle_to_append["star_player"] = is_star_player(battle["battle"]["starPlayer"], player_tag)
        battle_log.append(battle_to_append)

    return battle_log


if __name__ =="__main__":

    pass

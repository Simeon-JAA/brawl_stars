"""Pytest fixtures file"""

import pytest
import pandas as pd

@pytest.fixture
def empty_dataframe():
    """Returns an empty dataframe"""

    return pd.DataFrame()

##TODO what is this?? should this not be a dictionary
@pytest.fixture
def mock_event_api_dataframe():
    """Return mock dataframe from API call"""

    data = {
        "event_id": [1, 2, 3],
        "event_version": [1, 1, 1],
        "mode": ["Brawl Ball", "Brawl Ball", "Gem Grab"],
        "map": ["Mock Map 1", "Mock Map 2", "Mock Map 3"],
    }

    return pd.DataFrame(data)


@pytest.fixture
def mock_brawl_api_data():
    """Return mock brawler api object"""

    brawl_data_api = {
        "tag": "mock_tag",
        "name": "mock_name",
        "trophies": 123,
        "highestTrophies": 200,
        "expLevel": 5000,
        "expPoints": 50000,
        "isQualifiedFromChampionshipChallenge": True,
        "3vs3Victories": 1000,
        "soloVictories": 0,
        "duoVictories": 0,
        "bestRoboRumbleTime": 400
    }

    return brawl_data_api

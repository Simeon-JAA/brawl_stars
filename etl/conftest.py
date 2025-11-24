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
def mock_player_data_api():
    """Return mock player api object"""

    player_data_api = {
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

    return player_data_api


@pytest.fixture
def mock_player_data_db():
    """Return mock player db response"""

    player_data_db = {
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

    return player_data_db


@pytest.fixture
def mock_single_bs_battle():
    """Returns a mock battle log entry"""

    return {'battleTime': '20250413T092206.000Z',
         'event': {'id': 15000132, 'mode': 'brawlBall',
                   'map': 'Center Stage'},
         'battle': {'mode': 'brawlBall', 'type': 'soloRanked',
                    'result': 'defeat', 'duration': 150,
                    'starPlayer': {'tag': '#LLPCV2GVP', 
                                   'name': 'chihiro.', 
                                   'brawler': {'id': 16000025,
                                               'name': 'CARL',
                                               'power': 11,
                                               'trophies': 16}},
                                  
                    'teams': [[{'tag': '#LLPCV2GVP', 'name': 'chihiro.', 'brawler': 
                                {'id': 16000025, 'name': 'CARL', 'power': 11, 'trophies': 16}},
                                {'tag': '#8QC8RP02', 'name': '🥀 | sͥimͣzͫ♑', 'brawler': 
                                {'id': 16000087, 'name': 'JUJU', 'power': 11, 'trophies': 16}}, 
                                {'tag': '#2LPRQUV92', 'name': '嗄𝐟𝐚𝐳𝐞𝐕𝐲𝐭', 'brawler':
                                 {'id': 16000020, 'n       ame': 'FRANK', 'power': 11, 'trophies': 15}}],
                              [{'tag': '#2R8Q9LPLY', 'name': 'Crow', 'brawler': 
                                {'id': 16000034, 'name': 'JACKY', 'power': 11, 'trophies': 14}},
                                {'tag': '#J8J8L20UL', 'name': 'mikikikiriki', 'brawler': 
                                 {'id': 16000029, 'name': 'BEA', 'power': 11, 'trophies': 16}},
                                 {'tag': '#Y98JQCQJ8', 'name': 'Benji', 'brawler':
                                  {'id': 16000002, 'name': 'BULL', 'power': 11, 'trophies': 16}}]]}}

"""Pytest fixtures file"""

import pytest
import pandas as pd

@pytest.fixture
def empty_dataframe():
    """Returns an empty dataframe"""

    return pd.DataFrame()

@pytest.fixture
def mock_event_api_dataframe():
    """Returns a mock dataframe from API call"""

    data = {
        'event_id': [1, 2, 3],
        'event_version': [1, 1, 1],
        'mode': ['Brawl Ball', 'Brawl Ball', 'Gem Grab'],
        'map': ['Mock Map 1', 'Mock Map 2', 'Mock Map 3'],
    }

    return pd.DataFrame(data)

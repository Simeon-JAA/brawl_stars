"""Pytest fixtures file"""

import pytest
import pandas as pd

@pytest.fixture
def empty_dataframe():
    """Returns an empty dataframe"""
    
    return pd.DataFrame()
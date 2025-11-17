"""Testing file for transform.py"""

from unittest.mock import MagicMock

import pytest

from load import insert_new_event_data, insert_brawler_db

def test_insert_new_event_empty_dataframe_returns_none(empty_dataframe):
    """Tests insert_new_event_data with an empty dataframe returns none"""

    mock_db_conn = MagicMock()
    assert insert_new_event_data(mock_db_conn, empty_dataframe) is None

def test_insert_new_event_empty_dataframe_does_not_create_cursor(empty_dataframe):
    """Tests insert_new_event_data with an empty dataframe does not create a cursor"""

    mock_db_conn = MagicMock()
    insert_new_event_data(mock_db_conn, empty_dataframe)
    assert mock_db_conn.cursor.call_count == 0

def test_insert_new_event_wrong_data_type():
    """Tests insert_new_event_data with an incorrect data type raises a TypeError"""

    with pytest.raises(TypeError):
        mock_db_conn = MagicMock()
        insert_new_event_data(mock_db_conn, "not_a_dataframe")

def test_insert_new_event_creates_cursor(mock_event_api_dataframe):
    """Tests insert_new_event_data with a valid dataframe creates a cursor"""

    mock_db_conn = MagicMock()
    insert_new_event_data(mock_db_conn, mock_event_api_dataframe)

    assert mock_db_conn.cursor.call_count == 1

def test_insert_new_brawler_data_empty_dataframe_returns_none(empty_dataframe):
    """Tests insert_new_brawler_data with an empty dataframe returns none"""

    mock_db_conn = MagicMock()
    assert insert_brawler_db(mock_db_conn, empty_dataframe) is None

def test_insert_new_brawler_data_wrong_data_type():
    """Tests insert_new_brawler_data with an incorrect data type raises a TypeError"""

    with pytest.raises(TypeError):
        mock_db_conn = MagicMock()
        insert_brawler_db(mock_db_conn, "not_a_dataframe")

if __name__ == "__main__":

    pytest.main()

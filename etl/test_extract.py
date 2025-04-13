"""Testing file for extract.py"""

from unittest.mock import MagicMock

import pytest
from pandas import DataFrame
from psycopg2 import DatabaseError

from extract import get_most_recent_brawler_data, get_most_recent_brawler_version


def test_get_most_recent_brawler_data_calls_fetchall():
    """Tests get_most_recent_brawler_data calls the fetchall function"""

    mock_db_conn = MagicMock()
    mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value
    get_most_recent_brawler_data(mock_db_conn)

    assert mock_cursor.fetchall.call_count == 1

def test_get_most_recent_brawler_data_returns_dataframe_if_emtpy():
    """Tests that if get_most_recent_brawler_data returns an empty dictionary,
    a dataframe is still returned"""

    mock_db_conn = MagicMock()
    mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value
    mock_cursor.fetchall.return_value = []
    result = get_most_recent_brawler_data(mock_db_conn)

    assert isinstance(result, DataFrame)

def test_get_most_recent_brawler_data_returns_dataframe_with_correct_columns():
    """Tests that if get_most_recent_brawler_data returns an empty dictionary,
    the dataframe returned contains the correct columns"""

    mock_db_conn = MagicMock()
    mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value
    mock_cursor.fetchall.return_value = []
    result = get_most_recent_brawler_data(mock_db_conn)
    result_columns = result.columns.tolist()

    assert "brawler_id" in result_columns
    assert "brawler_name" in result_columns

def test_get_most_recent_brawler_data_failed_execute_raises_database_error():
    """Tests that if get_most_recent_brawler_data database request throws an error,
    an database error is raised"""

    mock_db_conn = MagicMock()
    mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value
    mock_cursor.execute.side_effect = Exception("Database error")

    with pytest.raises(DatabaseError):
        get_most_recent_brawler_data(mock_db_conn)

def test_get_most_recent_brawler_version_wrong_input_data_type():
    """Tests that type error is raised when get_most_recent_brawler_version
    is called with the wrong input data type"""

    mock_db_conn = MagicMock()
    with pytest.raises(TypeError):
        get_most_recent_brawler_version(mock_db_conn, "this is not a brawler_id")

def test_get_most_recent_brawler_version_calls_execute():
    """Tests cursor.execute is called by get_most_recent_brawler_version
    when a valid input is passed into function"""

    mock_db_conn = MagicMock()
    mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value
    get_most_recent_brawler_version(mock_db_conn, 1)

    assert mock_cursor.execute.call_count == 1

def test_get_most_recent_brawler_version_calls_fetchone():
    """Tests fetchone is called by cursor in get_most_recent_brawler_version
    when a valid input is passed into function"""

    mock_db_conn = MagicMock()
    mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value
    get_most_recent_brawler_version(mock_db_conn, 1)

    assert mock_cursor.fetchone.call_count == 1


if __name__ == "__main__":

    pytest.main()

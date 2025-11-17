"""Testing file for extract.py"""

from unittest.mock import MagicMock
from sqlite3 import DatabaseError

import pytest
from pandas import DataFrame

from extract import get_brawlers_latest_version, get_brawler_latest_version_id


#TODO Fix me
# def test_get_brawlers_latest_version_calls_fetchall():
#     """Tests get_brawlers_latest_version calls the fetchall function"""

#     mock_db_conn = MagicMock()
#     mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value
#     get_brawlers_latest_version(mock_db_conn)

#     assert mock_cursor.fetchall.call_count == 1


def test_get_brawlers_latest_version_returns_dataframe_if_emtpy():
    """Tests that if get_brawlers_latest_version returns an empty dictionary,
    a dataframe is still returned"""

    mock_db_conn = MagicMock()
    mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value
    mock_cursor.fetchall.return_value = []
    result = get_brawlers_latest_version(mock_db_conn)

    assert isinstance(result, DataFrame)


def test_get_brawlers_latest_version_returns_dataframe_with_correct_columns():
    """Tests that if get_brawlers_latest_version returns an empty dictionary,
    the dataframe returned contains the correct columns"""

    mock_db_conn = MagicMock()
    mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value
    mock_cursor.fetchall.return_value = []
    result = get_brawlers_latest_version(mock_db_conn)
    result_columns = result.columns.tolist()

    assert "brawler_id" in result_columns
    assert "brawler_name" in result_columns


#TODO Fix me
# def test_get_brawlers_latest_version_failed_execute_raises_database_error():
#     """Tests get_brawlers_latest_version() raises database exception if error encoutnered"""

#     mock_db_conn = MagicMock()
#     mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value
#     mock_cursor.execute.side_effect = Exception("Database error")

#     with pytest.raises(DatabaseError):
#         get_brawlers_latest_version(mock_db_conn)


def test_get_brawler_latest_version_id_wrong_input_data_type():
    """Tests that type error is raised when get_brawler_latest_version_id
    is called with the wrong input data type"""

    mock_db_conn = MagicMock()
    with pytest.raises(TypeError):
        get_brawler_latest_version_id(mock_db_conn, "this is not a brawler_id")


#TODO Fix me
# def test_get_brawler_latest_version_id_calls_execute():
#     """Tests cursor.execute is called by get_brawler_latest_version_id
#     when a valid input is passed into function"""

#     mock_db_conn = MagicMock()
#     mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value
#     get_brawler_latest_version_id(mock_db_conn, 1)

#     assert mock_cursor.execute.call_count == 1


#TODO Fix me
# def test_get_brawler_latest_version_id_calls_fetchone():
#     """Tests fetchone is called by cursor in get_brawler_latest_version_id
#     when a valid input is passed into function"""

#     mock_db_conn = MagicMock()
#     mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value
#     get_brawler_latest_version_id(mock_db_conn, 1)

#     assert mock_cursor.fetchone.call_count == 1


if __name__ == "__main__":

    pytest.main()

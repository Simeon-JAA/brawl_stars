"""Testing file for extract.py"""

from unittest.mock import MagicMock

import pytest

from extract import get_most_recent_brawler_data, get_most_recent_brawler_version


def test_get_most_recent_brawler_data_calls_fetchall():
    """Tests get_most_recent_brawler_data calls the fetchall function"""

    conn = MagicMock()
    mock_fetchall = conn.cursor().__enter__().fetchall
    get_most_recent_brawler_data(conn)

    assert mock_fetchall.call_count == 1


def test_get_most_recent_brawler_version_edge_case_1():
    """Tests exception raised for wrong input type get_most_recent_brawler_version"""

    conn = MagicMock()
    with pytest.raises(TypeError):
        get_most_recent_brawler_version(conn, "this is not a brawler_id")


def test_get_most_recent_brawler_version_calls_execute():
    """Tests execute is called by cursor for get_most_recent_brawler_version"""

    conn = MagicMock()
    mock_execute = conn.cursor().__enter__().execute
    get_most_recent_brawler_version(conn, 1)

    assert mock_execute.call_count == 1


def test_get_most_recent_brawler_version_calls_fetchone():
    """Tests execute is called by cursor for get_most_recent_brawler_version"""

    conn = MagicMock()
    mock_fetchone = conn.cursor().__enter__().fetchone
    get_most_recent_brawler_version(conn, 1)

    assert mock_fetchone.call_count == 1

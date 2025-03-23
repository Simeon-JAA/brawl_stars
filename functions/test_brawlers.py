"""Testing file for brawlers.py"""

import pytest

from brawlers import transform_all_brawler_names

def test_all_brawler_names_base_case_1():
    """Tests base case for all_brawler_names"""

    result = transform_all_brawler_names([{"name": "TEST"}])

    assert result == ["Test"]


def test_all_brawler_names_base_case_2():
    """Tests base case for all_brawler_names"""

    result = transform_all_brawler_names([{"name": "TEST"}, {"name": "TEST 2"}])

    assert result == ["Test", "Test 2"]


def test_all_brawler_names_base_case_3():
    """Tests base case for all_brawler_names"""

    result = transform_all_brawler_names([{"name": "EXAMPLE NAME"},
                                          {"name": "EXAMPLENAME"}])

    assert result == ["Example Name", "Examplename"]


def test_all_brawler_names_edge_case_1():
    """Tests edge case for all_brawler_names"""

    with pytest.raises(Exception):
        transform_all_brawler_names("this is not a list")


def test_all_brawler_names_edge_case_2():
    """Tests edge case for all_brawler_names"""

    with pytest.raises(Exception):
        transform_all_brawler_names([])


def test_all_brawler_names_edge_case_3():
    """Tests edge case for all_brawler_names"""

    with pytest.raises(Exception):
        transform_all_brawler_names(["name_1", "name_2", "sp_1", "sp_2"])


def test_all_brawler_names_edge_case_4():
    """Tests edge case for all_brawler_names"""

    with pytest.raises(Exception):
        transform_all_brawler_names([{"not_name": "not_name"},
                                     {"names": "name_1"},
                                     {"name1": 123}])


def test_all_brawler_names_edge_case_5():
    """Tests edge case for all_brawler_names"""

    with pytest.raises(Exception):
        transform_all_brawler_names([{"name": ""},
                                    {"name": ""}])



if __name__ =="__main__":

    pass

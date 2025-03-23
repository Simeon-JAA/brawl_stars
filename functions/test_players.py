"""Testing file for players.py"""

import pytest

from players import check_player_tag, format_player_tag, to_snake_case

def test_check_player_tag_base_case_1():
    """Tests base case for check_player_tag"""

    result = check_player_tag("#2P0LV8PV")

    assert result is True


def test_check_player_tag_base_case_2():
    """Tests base case for check_player_tag"""

    result = check_player_tag("8QC8RP02")

    assert result is True


def test_check_player_tag_base_case_3():
    """Tests base case for check_player_tag"""

    result = check_player_tag("#8QC8RP02")

    assert result is True


def test_check_player_tag_base_case_4():
    """Tests base case for check_player_tag"""

    result = check_player_tag("#2POLV8PV")

    assert result is True


def test_check_player_tag_base_case_5():
    """Tests base case for check_player_tag"""
    with pytest.raises(Exception):
        check_player_tag("")


def test_check_player_tag_base_case_6():
    """Tests base case for check_player_tag"""

    with pytest.raises(Exception):
        check_player_tag("     ")


def test_check_player_tag_base_case_7():
    """Tests base case for check_player_tag"""

    with pytest.raises(Exception):
        check_player_tag(12345)


def test_check_player_tag_base_case_8():
    """Tests base case for check_player_tag"""

    result = check_player_tag("1")

    assert result is False


def test_check_player_tag_base_case_9():
    """Tests base case for check_player_tag"""

    result = check_player_tag("12")

    assert result is False


def test_check_player_tag_base_case_10():
    """Tests base case for check_player_tag"""

    result = check_player_tag("#12")

    assert result is False


def test_check_player_tag_edge_case_1():
    """Tests edge case for check_player_tag"""

    result = check_player_tag("2POLV8PV        ")

    assert result is True


def test_check_player_tag_edge_case_2():
    """Tests edge case for check_player_tag"""

    result = check_player_tag("    2POLV8PV        ")

    assert result is True


def test_check_player_tag_edge_case_3():
    """Tests edge case for check_player_tag"""

    result = check_player_tag("    #2POLV8PV")

    assert result is True


def test_format_player_tag_base_case_1():
    """Tests base case for format_player_tag"""

    result = format_player_tag("#8QC8RP02")

    assert result == "8QC8RP02"


def test_format_player_tag_base_case_2():
    """Tests base case for format_player_tag"""

    result = format_player_tag("#8QC8RP02      ")

    assert result == "8QC8RP02"


def test_format_player_tag_base_case_3():
    """Tests base case for format_player_tag"""

    result = format_player_tag("    #8QC8RP02      ")

    assert result == "8QC8RP02"


def test_format_player_tag_base_case_4():
    """Tests base case for format_player_tag"""

    result = format_player_tag("    8QC8RP02      ")

    assert result == "8QC8RP02"


def test_format_player_tag_base_case_5():
    """Tests base case for format_player_tag"""

    result = format_player_tag("    8QC8RP02")

    assert result == "8QC8RP02"


def test_format_player_tag_base_case_6():
    """Tests base case for format_player_tag"""

    result = format_player_tag("  8QC8RP02")

    assert result == "8QC8RP02"


def test_format_player_tag_base_case_7():
    """Tests base case for format_player_tag"""

    result = format_player_tag("  #8Qc8rP02")

    assert result == "8QC8RP02"


def test_format_player_tag_base_case_8():
    """Tests base case for format_player_tag"""

    result = format_player_tag("  #8Qc8rv02")

    assert result == "8QC8RV02"


def test_format_player_tag_edge_case_1():
    """Tests edge case for format_player_tag"""

    with pytest.raises(Exception):
        format_player_tag("")


def test_format_player_tag_edge_case_2():
    """Tests edge case for format_player_tag"""

    with pytest.raises(Exception):
        format_player_tag({})


def test_format_player_tag_edge_case_3():
    """Tests edge case for format_player_tag"""

    with pytest.raises(Exception):
        format_player_tag(12345)


def test_to_snake_case_base_case_1():
    """Tests base case for to_snake_case"""

    result = to_snake_case("camelCase")

    assert result == "camel_case"


def test_to_snake_case_base_case_2():
    """Tests base case for to_snake_case"""

    result = to_snake_case("camelCasecamelCase")

    assert result == "camel_casecamel_case"


def test_to_snake_case_base_case_3():
    """Tests base case for to_snake_case"""

    result = to_snake_case("snakecase")

    assert result == "snakecase"


def test_to_snake_case_base_case_4():
    """Tests base case for to_snake_case"""

    result = to_snake_case("snakeCase")

    assert result == "snake_case"


def test_to_snake_case_base_case_5():
    """Tests base case for to_snake_case"""

    result = to_snake_case("snake1Case")

    assert result == "snake1_case"


def test_to_snake_case_base_case_6():
    """Tests base case for to_snake_case"""

    result = to_snake_case("snake1 Case")

    assert result == "snake1_case"


def test_to_snake_case_base_case_7():
    """Tests base case for to_snake_case"""

    result = to_snake_case("UpperCamelCase")

    assert result == "upper_camel_case"


def test_to_snake_case_base_case_8():
    """Tests base case for to_snake_case"""

    result = to_snake_case("Upper Camel Case")

    assert result == "upper_camel_case"


def test_to_snake_case_edge_case_1():
    """Tests esge case for to_snake_case"""

    with pytest.raises(Exception):
        to_snake_case("")


def test_to_snake_case_edge_case_2():
    """Tests esge case for to_snake_case"""

    with pytest.raises(Exception):
        to_snake_case(" ")


def test_to_snake_case_edge_case_3():
    """Tests esge case for to_snake_case"""

    with pytest.raises(Exception):
        to_snake_case(1)

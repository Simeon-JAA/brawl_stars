"""Testing file for transform.py"""

import pytest

from transform import (to_snake_case, brawler_name_value_to_title,
                       transform_brawl_data_api, transform_single_battle_entry)


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

def test_to_snake_case_leading_spaces():
    """Tests to_snake_case with leading spaces"""

    result = to_snake_case("     upperCamelCase")
    assert result == "upper_camel_case"

def test_to_snake_case_normal_spaces():
    """Tests to_snake_case with normal spacing"""

    result = to_snake_case("Upper Camel Case")
    assert result == "upper_camel_case"

def test_to_snake_case_trailing_spaces():
    """Tests to_snake_case with trailing spaces"""

    result = to_snake_case("starPowers     ")
    assert result == "star_powers"

def test_to_snake_case_value_error_raised_with_empty_string():
    """Tests value error is raised for to_snake_case
     having an input of an empty string"""

    with pytest.raises(ValueError):
        to_snake_case("")

def test_to_snake_case_value_error_raised_with_whitespace():
    """Tests value error is raised for to_snake_case
    when input is whitespace"""

    with pytest.raises(ValueError):
        to_snake_case(" ")

def test_to_snake_case_type_error_with_wrong_input():
    """Tests type input is raised for to_snake_case
    with an input that is not a string"""

    with pytest.raises(TypeError):
        to_snake_case(1)

def test_to_snake_case_5v5():
    """Tests case for to_snake_case 5v5 game mode"""

    result = to_snake_case("brawlBall5V5")
    assert result == "brawl_ball_5v5"

def test_to_snake_case_5v5_trailing_space():
    """Tests case for to_snake_case with 5v5 game mode
    and trailing spaces"""

    result = to_snake_case("brawlBall5V5   ")
    assert result == "brawl_ball_5v5"

def test_to_snake_case_5v5_leading_space():
    """Tests case for to_snake_case with 5v5 game mode
    and leading spaces"""

    result = to_snake_case("    brawlBall5V5")
    assert result == "brawl_ball_5v5"

def test_brawler_name_value_to_title_base_case_1():
    """Tests base case for brawler_name_value_to_title"""

    result = brawler_name_value_to_title({'id': 16000000,
                                           'name': 'SHELLY', 
                                           'starPowers': [{'id': 23000076, 
                                                           'name': 'SHELL SHOCK'}, 
                                                           {'id': 23000135,
                                                            'name': 'BAND-AID'}], 
                                            'gadgets': [{'id': 23000255, 
                                                         'name': 'FAST FORWARD'}, 
                                                         {'id': 23000288,
                                                          'name': 'CLAY PIGEONS'}
                                                        ]
                                            })

    assert result == {'id': 16000000,
                      'name': 'Shelly',
                      'starPowers': [{'id': 23000076, 
                                      'name': 'Shell Shock'}, 
                                      {'id': 23000135,
                                      'name': 'Band-Aid'}], 
                      'gadgets': [{'id': 23000255,
                                    'name': 'Fast Forward'}, 
                                    {'id': 23000288,
                                    'name': 'Clay Pigeons'}
                                  ]
                      }

def test_brawler_name_value_to_title_base_case_2():
    """Tests base case for brawler_name_value_to_title"""

    result = brawler_name_value_to_title({'id': 16000000,
                                           'name': 'shelly',
                                           'starPowers': [{'id': 23000076,
                                                           'name': 'SHeLl ShocK'}, 
                                                           {'id': 23000135,
                                                            'name': 'baND-aiD'}], 
                                            'gadgets': [{'id': 23000255,
                                                         'name': 'fAST fORWARD'}, 
                                                         {'id': 23000288,
                                                          'name': 'clay PIGEONS'}
                                                        ]
                                            })

    assert result == {'id': 16000000,
                      'name': 'Shelly',
                      'starPowers': [{'id': 23000076,
                                      'name': 'Shell Shock'},
                                      {'id': 23000135,
                                      'name': 'Band-Aid'}],
                      'gadgets': [{'id': 23000255,
                                    'name': 'Fast Forward'},
                                    {'id': 23000288,
                                    'name': 'Clay Pigeons'}
                                  ]
                      }

def test_brawler_name_value_to_title_base_case_3():
    """Tests base case for brawler_name_value_to_title"""

    with pytest.raises(KeyError):
        brawler_name_value_to_title({'id': 16000000,
                                           'name': 'shelly'
                                            })

def test_brawler_name_value_to_title_base_case_4():
    """Tests base case for brawler_name_value_to_title"""

    with pytest.raises(TypeError):
        brawler_name_value_to_title("This is not a dictionary!")

def test_transform_brawl_data_api_base_case_1():
    """Tests base case for transform_brawl_data_api"""

    result = transform_brawl_data_api([{'id': 16000000,
                                           'name': 'SHELLY', 
                                           'starPowers': [{'id': 23000076, 
                                                           'name': 'SHELL SHOCK'}, 
                                                           {'id': 23000135,
                                                            'name': 'BAND-AID'}], 
                                            'gadgets': [{'id': 23000255, 
                                                         'name': 'FAST FORWARD'}, 
                                                         {'id': 23000288,
                                                          'name': 'CLAY PIGEONS'}
                                                        ]
                                            }])

    assert result == [{'id': 16000000,
                      'name': 'Shelly',
                      'star_powers': [{'id': 23000076, 
                                      'name': 'Shell Shock'}, 
                                      {'id': 23000135,
                                      'name': 'Band-Aid'}], 
                      'gadgets': [{'id': 23000255, 
                                    'name': 'Fast Forward'}, 
                                    {'id': 23000288,
                                    'name': 'Clay Pigeons'}
                                  ]
                      }]


if __name__ == "__main__":

    pytest.main()

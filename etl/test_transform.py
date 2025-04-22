"""Testing file for transform.py"""

import pytest

from pandas import DataFrame

from transform import (to_snake_case, brawler_name_value_to_title, to_title,
                       valid_trophy_change, transform_brawl_data_api, battle_to_df,
                       format_datetime)


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

def test_to_title_raises_value_error_with_empty_string():
    """Tests value error is raised for to_title
    if input is an empty string"""

    with pytest.raises(ValueError):
        to_title("")

def test_to_title_raises_type_error_with_empty_string():
    """Tests type error is raised for to_title
    if input is not a string"""

    with pytest.raises(TypeError):
        to_title([2, 3, 4])

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

def test_format_datetime_wrong_input_raises_type_error():
    """Tests type error is raised for format_datetime
    if the input is not a string"""

    with pytest.raises(TypeError):
        format_datetime(5)

def test_format_datetime_empty_input_raises_value_error():
    """Tests value error is raised for format_datetime
    if the input is and empty string"""

    with pytest.raises(ValueError):
        format_datetime("")

def test_format_datetime_whitepace_input_raises_value_error():
    """Tests value error is raised for format_datetime
    if the input only whitespace"""

    with pytest.raises(ValueError):
        format_datetime("    ")

def test_valid_trophy_change_empty_dictionary_raises_value_error():
    """Tests value error is raised for valid_trophy_change
    if the input is an empty dictionary"""
    
    with pytest.raises(ValueError):
        valid_trophy_change({})

def test_valid_trophy_change_wrong_input_raises_type_error():
    """Tests type error is raised for valid_trophy_change
    if the input is not a dictionary"""
    
    with pytest.raises(TypeError):
        valid_trophy_change("This is not a dictionary!")

def test_valid_trophy_change_returns_true_with_trophy_change_key():
    """Tests valid_trophy_change returns true if the input
    dictionary has a trophyChange key"""

    result = valid_trophy_change({"battle" : {"trophyChange": 0}})
    assert result == True

def test_valid_trophy_change_returns_false_without_trophy_change_key(mock_single_bs_battle):
    """Tests valid_trophy_change returns false if the input
    dictionary does not have a trophyChange key"""

    result = valid_trophy_change(mock_single_bs_battle)
    assert result == False

def test_battle_to_df_raises_type_error_with_wrong_input():
    """Tests type error is raised for battle_to_df
    if the input is not a dictionary"""

    with pytest.raises(TypeError):
        battle_to_df("This is not a dictionary!")

def test_battle_to_df_raises_value_error_with_empty_dictionary():
    """Tests value error is raised for battle_to_df
    if the dictionary input is empty"""

    with pytest.raises(ValueError):
        battle_to_df({})

def test_battle_to_df_returns_dataframe(mock_single_bs_battle):
    """Tests battle_to_df returns a dataframe"""

    result = battle_to_df(mock_single_bs_battle, "")
    assert isinstance(result, DataFrame)

def test_battle_to_df_returns_correct_columns(mock_single_bs_battle):
    """Tests battle_to_df returns the correct columns"""

    desired_columns = ["battle_time", "event_id", "result", 
                       "duration", "battle_type", "trophy_change"]
    result = battle_to_df(mock_single_bs_battle)
    assert result.columns.tolist() == desired_columns

if __name__ == "__main__":

    pytest.main()

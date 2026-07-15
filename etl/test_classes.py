import pytest

from classes import Player


def test_player_from_api_with_all_fields(mock_player_data_api):

    data = mock_player_data_api
    player = Player.from_api(data)

    assert player.tag == mock_player_data_api["tag"]
    assert player.name == mock_player_data_api["name"]
    assert player.trophies == mock_player_data_api["trophies"]
    assert player.highest_trophies == mock_player_data_api["highestTrophies"]
    assert player.exp_level == mock_player_data_api["expLevel"]
    assert player.exp_points == mock_player_data_api["expPoints"]
    assert player.qualified_from_cc == mock_player_data_api["isQualifiedFromChampionshipChallenge"]
    assert player.victories_3v3 == mock_player_data_api["3vs3Victories"]
    assert player.victories_solo == mock_player_data_api["soloVictories"]
    assert player.victories_duo == mock_player_data_api["duoVictories"]


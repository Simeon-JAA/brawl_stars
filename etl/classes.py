"""Classes Script for the ETL process."""


from dataclasses import dataclass

@dataclass
class Brawler:
    """Class representing a Brawler."""

    name: str
    star_powers: list[str]
    gadgets: list[str]
    hypercharge: str
    buffies: list[str]
  

    @classmethod
    def from_api_response(cls, api_response: dict) -> "Brawler":
        """Create a Brawler instance from an API response."""
        return cls(
          name=api_response.get("name", ""))
    


    # def __repr__(self):
    #     """Return string representation of the Brawler."""
    #     return f"Brawler(name={self.name})"


@dataclass
class Player:
    """Class representing a Player."""

    tag: str
    name: str
    trophies: int
    highest_trophies: int
    exp_level: int
    exp_points: int
    qualified_from_cc: bool
    victories_3v3: int
    victories_solo: int
    victories_duo: int
    bestRoboRumbleTime: int

    @classmethod
    def from_api(cls, data: dict) -> "Player":
        """Create a Player instance from API data."""
        return cls(
            tag=data["tag"],
            name=data["name"],
            trophies=data["trophies"],
            highest_trophies=data["highestTrophies"],
            exp_level=data["expLevel"],
            exp_points=data["expPoints"],
            qualified_from_cc=data.get("isQualifiedFromChampionshipChallenge", False),
            victories_3v3=data.get("3vs3Victories"),
            victories_solo=data.get("soloVictories"),
            victories_duo=data.get("duoVictories"),
            bestRoboRumbleTime=data.get("bestRoboRumbleTime", 0)
        )
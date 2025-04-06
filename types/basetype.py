from typing import List

class PokemonType:
    """Base class for all Pokémon types."""

    def __init__(self, name: str, weaknesses: List[str], resistances: List[str], immunities: List[str], color: List[str]):
        self.name = name
        self.weaknesses = weaknesses
        self.resistances = resistances
        self.immunities = immunities
        self.color = color

    def __str__(self):
        return self.name
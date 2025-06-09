from enum import Enum


class AnimalSpecies(Enum):
    WOLF = "Wolf"
    SHEEP = "Sheep"
    CYBER_SHEEP = "Cyber_Sheep"
    FOX = "Fox"
    TURTLE = "Turtle"
    ANTELOPE = "Antelope"
    HUMAN = "Human"
    NONE = "None"

    @staticmethod
    def from_string(animal: str):
        animal_upper = animal.upper()
        mapping = {
            "WOLF": AnimalSpecies.WOLF,
            "SHEEP": AnimalSpecies.SHEEP,
            "CYBER_SHEEP": AnimalSpecies.CYBER_SHEEP,
            "FOX": AnimalSpecies.FOX,
            "TURTLE": AnimalSpecies.TURTLE,
            "ANTELOPE": AnimalSpecies.ANTELOPE,
            "HUMAN": AnimalSpecies.HUMAN,
        }
        return mapping.get(animal_upper, AnimalSpecies.NONE)

    def __str__(self):
        return self.value

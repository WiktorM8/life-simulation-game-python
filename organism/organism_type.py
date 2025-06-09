from enum import Enum


class OrganismType(Enum):
    ANIMAL = "Animal"
    PLANT = "Plant"
    NONE = "None"

    @staticmethod
    def from_string(organism: str):
        organism_upper = organism.upper()
        mapping = {
            "ANIMAL": OrganismType.ANIMAL,
            "PLANT": OrganismType.PLANT,
            "NONE": OrganismType.NONE
        }
        return mapping.get(organism_upper, OrganismType.NONE)

    def __str__(self):
        return self.value

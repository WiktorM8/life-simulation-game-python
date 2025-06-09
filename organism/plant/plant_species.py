from enum import Enum


class PlantSpecies(Enum):
    DANDELION = "Dandelion"
    GRASS = "Grass"
    NIGHTSHADE = "Nightshade"
    GUARANA = "Guarana"
    HOGWEED = "Hogweed"
    NONE = "None"

    @staticmethod
    def from_string(plant: str):
        plant_upper = plant.upper()
        mapping = {
            "DANDELION": PlantSpecies.DANDELION,
            "GRASS": PlantSpecies.GRASS,
            "GUARANA": PlantSpecies.GUARANA,
            "NIGHTSHADE": PlantSpecies.NIGHTSHADE,
            "HOGWEED": PlantSpecies.HOGWEED,
        }
        return mapping.get(plant_upper, PlantSpecies.NONE)

    def __str__(self):
        return self.value

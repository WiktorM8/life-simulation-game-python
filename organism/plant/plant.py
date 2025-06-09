from abc import abstractmethod

from organism.organism import Organism
from organism.organism_type import OrganismType
from organism.plant.plant_species import PlantSpecies
from world.position import Position


class Plant(Organism):
    def __init__(self, position, strength, initiative, species, world):
        super().__init__(position, strength, initiative, OrganismType.PLANT, world)
        self.species = species

    def action(self):
        if not self.alive:
            return
        self.spread()
        self.increase_age()

    def get_species(self):
        return self.species

    def spread(self):
        from random import randint, choice
        if randint(0, 99) < 10:
            neighbours = self.world.get_free_neighbours(self.position, 1)
            if neighbours:
                pos = choice(neighbours)
                new_plant = self.make_child()
                new_plant.set_position(pos)
                self.world.add_new_organism(new_plant)

    def collision(self, other):
        if other.type == OrganismType.ANIMAL:
            self.alive = False

    def serialize(self):
        return f"{self.type} {self.species} {self.position.x} {self.position.y} " \
               f"{self.strength} {self.initiative} {self.age} "

    @staticmethod
    def deserialize_plant(data, world):
        parts = data.split(" ")
        species = PlantSpecies.from_string(parts[1])
        position = Position(int(parts[2]), int(parts[3]))
        strength = int(parts[4])
        initiative = int(parts[5])
        age = int(parts[6])

        from organism.plant.grass import Grass
        from organism.plant.dandelion import Dandelion
        from organism.plant.guarana import Guarana
        from organism.plant.nightshade_berry import NightshadeBerry
        from organism.plant.hogweed import Hogweed

        plant_class = {
            "GRASS": Grass,
            "DANDELION": Dandelion,
            "GUARANA": Guarana,
            "NIGHTSHADE": NightshadeBerry,
            "HOGWEED": Hogweed
        }[species.name]
        plant = plant_class(position, world)
        plant.strength = strength
        plant.initiative = initiative
        plant.age = age
        return plant

    @abstractmethod
    def make_child(self):
        pass

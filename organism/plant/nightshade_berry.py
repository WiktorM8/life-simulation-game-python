from organism.plant.plant import Plant
from organism.plant.plant_species import PlantSpecies
from event.nightshade_berry_eaten_event import NightshadeBerryEatenEvent
from event.human.human_eat_dangerous_plant_and_survived_event import HumanEatDangerousPlantAndSurvivedEvent
from organism.organism_type import OrganismType
from organism.animal.animal_species import AnimalSpecies


class NightshadeBerry(Plant):
    def __init__(self, position, world):
        super().__init__(position, 99, 0, PlantSpecies.NIGHTSHADE, world)

    def make_child(self):
        return NightshadeBerry(self.get_position(), self.world)

    def get_texture(self):
        return "berry.png"

    def collision(self, other):
        if other.type == OrganismType.ANIMAL:
            if not other.defend_attack(self):
                other.set_alive(False)
                self.world.dispatch_world_event(NightshadeBerryEatenEvent(self, other))
            elif other.species == AnimalSpecies.HUMAN:
                self.world.dispatch_world_event(HumanEatDangerousPlantAndSurvivedEvent(other, self))
            self.set_alive(False)

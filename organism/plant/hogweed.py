from organism.plant.plant import Plant
from organism.plant.plant_species import PlantSpecies
from organism.organism_type import OrganismType
from organism.animal.animal_species import AnimalSpecies


class Hogweed(Plant):
    def __init__(self, position, world):
        super().__init__(position, 10, 0, PlantSpecies.HOGWEED, world)

    def make_child(self):
        return Hogweed(self.get_position(), self.world)

    def get_texture(self):
        return "hogweed-wildflower.png"

    def collision(self, other):
        if other.type == OrganismType.ANIMAL:
            if not other.defend_attack(self):
                other.set_alive(False)
                from event.hogweed_eaten_event import HogweedEatenEvent
                self.world.dispatch_world_event(HogweedEatenEvent(self, other))
            elif other.species == AnimalSpecies.HUMAN:
                from event.human.human_eat_dangerous_plant_and_survived_event import \
                    HumanEatDangerousPlantAndSurvivedEvent
                self.world.dispatch_world_event(HumanEatDangerousPlantAndSurvivedEvent(other, self))
            self.set_alive(False)

    def kill_nearby_animals(self):
        for pos in self.world.get_neighbours(self.position, 1):
            organism = self.world.get_organism_at(pos)
            if organism and organism.type == OrganismType.ANIMAL:
                if not organism.defend_attack(self):
                    organism.set_alive(False)
                    if organism.species == AnimalSpecies.HUMAN:
                        from event.hogweed_burn_human_event import HogweedBurnHumanEvent
                        self.world.dispatch_world_event(HogweedBurnHumanEvent(self, organism))

    def action(self):
        if not self.alive:
            return
        super().action()
        self.kill_nearby_animals()

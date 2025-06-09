from organism.plant.plant import Plant
from organism.plant.plant_species import PlantSpecies
from organism.organism_type import OrganismType


class Guarana(Plant):
    def __init__(self, position, world):
        super().__init__(position, 0, 0, PlantSpecies.GUARANA, world)

    def make_child(self):
        return Guarana(self.get_position(), self.world)

    def get_texture(self):
        return "guarana.png"

    def collision(self, other):
        if other.type == OrganismType.ANIMAL:
            other.strength += 3
            self.alive = False
            from event.guarana_eaten_event import GuaranaEatenEvent
            self.world.dispatch_world_event(GuaranaEatenEvent(self, other))
        else:
            super().collision(other)

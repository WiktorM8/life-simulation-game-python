from organism.plant.plant import Plant
from organism.plant.plant_species import PlantSpecies


class Dandelion(Plant):
    def __init__(self, position, world):
        super().__init__(position, 0, 0, PlantSpecies.DANDELION, world)

    def make_child(self):
        return Dandelion(self.get_position(), self.world)

    def get_texture(self):
        return "dandelion.png"

    def action(self):
        if not self.alive:
            return
        for _ in range(3):
            self.spread()
        self.age += 1

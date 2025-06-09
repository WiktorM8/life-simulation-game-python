from organism.plant.plant import Plant
from organism.plant.plant_species import PlantSpecies


class Grass(Plant):
    def __init__(self, position, world):
        super().__init__(position, 0, 0, PlantSpecies.GRASS, world)

    def make_child(self):
        return Grass(self.get_position(), self.world)

    def get_texture(self):
        return "grass.png"

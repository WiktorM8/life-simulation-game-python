from organism.animal.animal import Animal
from organism.animal.animal_species import AnimalSpecies


class Wolf(Animal):
    def __init__(self, position, world):
        super().__init__(position, AnimalSpecies.WOLF, 9, 5, world)

    def make_child(self):
        return Wolf(self.get_position(), self.get_world())

    def get_texture(self):
        return "wolf.png"

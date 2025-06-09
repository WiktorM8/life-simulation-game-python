from organism.animal.animal import Animal
from organism.animal.animal_species import AnimalSpecies
from world.position import Position
from world.base_world import BaseWorld


class Sheep(Animal):
    def __init__(self, position: Position, world: BaseWorld):
        super().__init__(position, AnimalSpecies.SHEEP, 4, 4, world)

    def make_child(self):
        return Sheep(self.get_position(), self.get_world())

    def get_texture(self):
        return "sheep.png"

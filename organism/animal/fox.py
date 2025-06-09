from organism.animal.animal import Animal
from organism.animal.animal_species import AnimalSpecies
from world.position import Position
from world.base_world import BaseWorld

import random


class Fox(Animal):
    def __init__(self, position: Position, world: BaseWorld):
        super().__init__(position, AnimalSpecies.FOX, 3, 7, world)

    def make_child(self):
        return Fox(self.get_position(), self.get_world())

    def get_texture(self):
        return "fox.png"

    def is_field_safe(self, x, y):
        for organism in self.get_world().get_organisms():
            if organism.get_position().x == x and organism.get_position().y == y:
                if organism.get_strength() > self.get_strength():
                    return False
        return True

    def make_move(self):
        possible_moves = self.get_world().get_neighbours(self.get_position(), 1)
        while possible_moves:
            new_position = random.choice(possible_moves)
            if self.is_field_safe(new_position.x, new_position.y):
                self.set_position(new_position)
                break
            possible_moves.remove(new_position)

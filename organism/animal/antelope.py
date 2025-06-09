from organism.animal.animal import Animal
from organism.organism import Organism
from organism.organism_type import OrganismType
from organism.animal.animal_species import AnimalSpecies
from event.antelope_escape_event import AntelopeEscapeEvent
from world.position import Position
from world.base_world import BaseWorld

import random


class Antelope(Animal):
    def __init__(self, position: Position, world: BaseWorld):
        super().__init__(position, AnimalSpecies.ANTELOPE, 4, 4, world)

    def make_child(self):
        return Antelope(self.get_position(), self.get_world())

    def get_texture(self):
        return "antelope.png"

    def collision(self, other: Organism):
        if other.get_type() == OrganismType.ANIMAL:
            other_animal = other
            if other_animal.get_strength() > self.get_strength():
                if random.randint(0, 99) < 50:
                    new_positions = self.get_world().get_free_neighbours(self.get_position(), 1)
                    if new_positions:
                        new_position = random.choice(new_positions)
                        self.move_to(new_position)
                        self.get_world().dispatch_world_event(AntelopeEscapeEvent(self, other_animal))
                        return
        super().collision(other)

    def defend_attack(self, attacker: Organism):
        if attacker.get_type() == OrganismType.PLANT:
            return False

        animal_attacker = attacker
        if animal_attacker.get_strength() > self.get_strength():
            if random.randint(0, 99) < 50:
                new_positions = self.get_world().get_free_neighbours(self.get_position(), 1)
                if new_positions:
                    new_position = random.choice(new_positions)
                    self.move_to(new_position)
                    self.get_world().dispatch_world_event(AntelopeEscapeEvent(self, animal_attacker))
                    return True
        return False

    def make_move(self):
        neighbours = self.get_world().get_neighbours(self.get_position(), 2)
        if neighbours:
            self.move_to(random.choice(neighbours))

from organism.animal.animal import Animal
from organism.organism import Organism
from organism.organism_type import OrganismType
from organism.animal.animal_species import AnimalSpecies
from event.turtle_defended_attack_event import TurtleDefendedAttackEvent
from world.position import Position
from world.base_world import BaseWorld

import random


class Turtle(Animal):
    def __init__(self, position: Position, world: BaseWorld):
        super().__init__(position, AnimalSpecies.TURTLE, 2, 1, world)

    def make_child(self):
        return Turtle(self.get_position(), self.get_world())

    def get_texture(self):
        return "turtle.png"

    def attack(self, other: 'Animal'):
        if self.strength < other.get_strength() < 5:
            self.move_to(self.get_last_position())
            return
        super().attack(other)

    def defend_attack(self, attacker: Organism):
        if attacker.get_type() == OrganismType.PLANT:
            return False

        if attacker.get_strength() < 5:
            attacker.move_to(attacker.get_last_position())
            self.get_world().dispatch_world_event(TurtleDefendedAttackEvent(self, attacker))
            return True
        return False

    def make_move(self):
        if random.random() > 0.25:
            return
        super().make_move()

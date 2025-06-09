import random

from organism.animal.animal import Animal
from organism.animal.animal_species import AnimalSpecies
from organism.organism_type import OrganismType
from organism.plant.plant_species import PlantSpecies
from world.position import Position
from world.base_world import BaseWorld
from organism.plant.hogweed import Hogweed


class CyberSheep(Animal):
    def __init__(self, position: Position, world: BaseWorld):
        super().__init__(position, AnimalSpecies.CYBER_SHEEP, 10, 4, world)

    def make_child(self):
        return CyberSheep(self.get_position(), self.get_world())

    def get_texture(self):
        return "cyber-sheep.png"

    def calculate_distance(self, pos: Position):
        dx = abs(self.get_position().x - pos.x)
        dy = abs(self.get_position().y - pos.y)
        return dx + dy

    def defend_attack(self, attacker):
        if attacker.get_type() == OrganismType.PLANT and attacker.get_species() == PlantSpecies.HOGWEED:
            return True
        super().defend_attack(attacker)

    def move_toward(self, target_pos: Position):
        current = self.get_position()
        dx = target_pos.x - current.x
        dy = target_pos.y - current.y

        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)

        if dx != 0 and dy != 0:
            rand = random.randint(1, 2)
            if rand == 1:
                step_x = 0
            else:
                step_y = 0

        new_pos = Position(current.x + step_x, current.y + step_y)

        if self.get_world().is_position_valid_obj(new_pos):
            self.move_to(new_pos)

    def make_move(self):
        hogweeds = [org for org in self.get_world().get_organisms()
                    if isinstance(org, Hogweed) and org.is_alive()]

        if hogweeds:
            target = min(hogweeds, key=lambda h: self.calculate_distance(h.get_position()))
            self.move_toward(target.get_position())
        else:
            super().make_move()


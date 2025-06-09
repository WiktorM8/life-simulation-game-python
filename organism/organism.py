from abc import ABC, abstractmethod
from world.position import Position
from world.base_world import BaseWorld
from organism.organism_type import OrganismType


class Organism(ABC):
    def __init__(self, position: Position, strength: int, initiative: int,
                 organism_type: OrganismType, world: BaseWorld):
        self.position = position
        self.age = 0
        self.strength = strength
        self.initiative = initiative
        self.alive = True
        self.type = organism_type
        self.world = world

    def set_position(self, position: Position):
        self.position = position

    def set_position_x(self, x: int):
        self.position.x = x

    def set_position_y(self, y: int):
        self.position.y = y

    def set_age(self, age: int):
        self.age = age

    def increase_age(self):
        self.age += 1

    def set_strength(self, strength: int):
        self.strength = strength

    def set_initiative(self, initiative: int):
        self.initiative = initiative

    def set_alive(self, alive: bool):
        self.alive = alive

    def set_type(self, organism_type: OrganismType):
        self.type = organism_type

    def set_world(self, world: BaseWorld):
        self.world = world

    def get_position(self) -> Position:
        return self.position

    def get_position_x(self) -> int:
        return self.position.x

    def get_position_y(self) -> int:
        return self.position.y

    def get_age(self) -> int:
        return self.age

    def get_strength(self) -> int:
        return self.strength

    def get_initiative(self) -> int:
        return self.initiative

    def is_alive(self) -> bool:
        return self.alive

    def get_type(self) -> OrganismType:
        return self.type

    def get_world(self) -> BaseWorld:
        return self.world

    def draw(self):
        self.world.get_game_manager().draw_texture_on_map(
            self.position.x, self.position.y, self.get_texture()
        )

    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def collision(self, other: 'Organism'):
        pass

    @abstractmethod
    def get_texture(self) -> str:
        pass

    @abstractmethod
    def serialize(self) -> str:
        pass

    @staticmethod
    def deserialize(data: str, world: BaseWorld) -> 'Organism':
        parts = data.split()
        org_type = OrganismType.from_string(parts[0])
        if org_type == OrganismType.PLANT:
            from organism.plant.plant import Plant
            return Plant.deserialize_plant(data, world)
        elif org_type == OrganismType.ANIMAL:
            from organism.animal.animal import Animal
            return Animal.deserialize_animal(data, world)
        else:
            raise ValueError(f"Unknown organism type: {parts[0]}")


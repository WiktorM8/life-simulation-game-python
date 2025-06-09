from abc import ABC, abstractmethod


from organism.organism import Organism
from organism.organism_type import OrganismType
from organism.animal.animal_species import AnimalSpecies
from world.position import Position


class Animal(Organism, ABC):
    BREED_COOLDOWN = 5

    def __init__(self, position, species, strength, initiative, world):
        super().__init__(position, strength, initiative, OrganismType.ANIMAL, world)
        self.species = species
        self.last_position = position
        self.breed_cooldown = 0

    def set_species(self, species: AnimalSpecies):
        self.species = species

    def get_species(self):
        return self.species

    def get_breed_cooldown(self):
        return self.breed_cooldown

    def move_to(self, new_position):
        self.last_position = self.position
        self.position = new_position

    def is_ready_to_breed(self):
        return self.breed_cooldown == 0

    def decrement_breed_cooldown(self):
        if self.breed_cooldown > 0:
            self.breed_cooldown -= 1

    def get_last_position(self):
        return self.last_position

    def action(self):
        if not self.alive:
            return
        self.make_move()
        self.check_for_collision()
        self.increase_age()
        self.decrement_breed_cooldown()

    def make_move(self):
        neighbours = self.world.get_neighbours(self.position, 1)
        if neighbours:
            from random import choice
            self.move_to(choice(neighbours))

    def check_for_collision(self):
        all_organisms = self.world.organisms + self.world.new_organisms
        for organism in all_organisms:
            if organism is not self and organism.is_alive():
                if self.position.is_position_same(organism.position):
                    self.collision(organism)

    def collision(self, other):
        if other.type == OrganismType.PLANT:
            other.collision(self)
            return
        if isinstance(other, Animal):
            if self.species == other.species:
                self.breed(other)
            else:
                self.attack(other)

    def attack(self, other):
        if other.defend_attack(self):
            return
        if self.strength >= other.strength:
            other.set_alive(False)
            from event.animal_kill_event import AnimalKillEvent
            self.world.dispatch_world_event(AnimalKillEvent(self, other))
        else:
            self.set_alive(False)
            from event.animal_kill_event import AnimalKillEvent
            self.world.dispatch_world_event(AnimalKillEvent(other, self))

    def breed(self, other):
        self.move_to(self.last_position)
        if not (self.is_ready_to_breed() and other.is_ready_to_breed()):
            return
        free = self.world.get_free_neighbours(other.position, 1)
        if not free:
            return
        from random import choice
        child_position = choice(free)
        child = self.make_child()
        child.set_position(child_position)
        child.breed_cooldown = self.BREED_COOLDOWN
        self.world.add_new_organism(child)
        self.breed_cooldown = self.BREED_COOLDOWN
        other.breed_cooldown = self.BREED_COOLDOWN
        from event.animal_breed_event import AnimalBreedEvent
        self.world.dispatch_world_event(AnimalBreedEvent(other, child))

    def defend_attack(self, attacker):
        return False

    def serialize(self):
        return f"{self.type} {self.species} {self.position.x} {self.position.y} " \
               f"{self.last_position.x} {self.last_position.y} {self.strength} {self.initiative} " \
               f"{self.age} {self.breed_cooldown} "

    @staticmethod
    def deserialize_animal(data, world):
        parts = data.split(" ")
        species = AnimalSpecies.from_string(parts[1])
        position = Position(int(parts[2]), int(parts[3]))
        last_position = Position(int(parts[4]), int(parts[5]))
        strength = int(parts[6])
        initiative = int(parts[7])
        age = int(parts[8])
        cooldown = int(parts[9])

        from organism.animal.human import Human
        if species.name == "HUMAN":
            return Human.deserialize_human(data, world)

        from organism.animal.wolf import Wolf
        from organism.animal.sheep import Sheep
        from organism.animal.cyber_sheep import CyberSheep
        from organism.animal.turtle import Turtle
        from organism.animal.fox import Fox
        from organism.animal.antelope import Antelope

        animal_class = {
            "ANTELOPE": Antelope,
            "SHEEP": Sheep,
            "CYBER_SHEEP": CyberSheep,
            "WOLF": Wolf,
            "FOX": Fox,
            "TURTLE": Turtle
        }[species.name]
        animal = animal_class(position, world)
        animal.last_position = last_position
        animal.strength = strength
        animal.initiative = initiative
        animal.age = age
        animal.breed_cooldown = cooldown
        return animal

    @abstractmethod
    def make_child(self):
        pass

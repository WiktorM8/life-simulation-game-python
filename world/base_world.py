from abc import ABC, abstractmethod
import random

from world.position import Position


class BaseWorld(ABC):
    def __init__(self, width, height, game_manager):
        self.width = width
        self.height = height
        self.game_manager = game_manager
        self.organisms = []
        self.new_organisms = []
        self.listener = None

    def set_width(self, width):
        self.width = width

    def get_width(self):
        return self.width

    def set_height(self, height):
        self.height = height

    def get_height(self):
        return self.height

    def add_organism(self, organism):
        self.organisms.append(organism)

    def get_organisms(self):
        return self.organisms

    def remove_dead_organisms(self):
        self.organisms = [org for org in self.organisms if org.is_alive()]

    def sort_organisms(self):
        self.organisms.sort(key=lambda o: (-o.get_initiative(), -o.get_age()))

    def add_new_organism(self, organism):
        self.new_organisms.append(organism)

    def get_game_manager(self):
        return self.game_manager

    def set_game_manager(self, game_manager):
        self.game_manager = game_manager

    def clear_world(self):
        self.organisms.clear()
        self.new_organisms.clear()

    def set_event_listener(self, listener):
        self.listener = listener

    def make_turn(self):
        self.sort_organisms()
        for organism in self.organisms:
            if organism.is_alive():
                organism.action()
        self.remove_dead_organisms()
        self.merge_new_organisms()
        for organism in self.organisms:
            organism.draw()

    def merge_new_organisms(self):
        self.organisms.extend(self.new_organisms)
        self.new_organisms.clear()

    def get_new_organisms(self):
        return self.new_organisms

    @abstractmethod
    def get_neighbours(self, position, radius):
        pass

    def generate_starting_organisms(self):
        from organism.animal.wolf import Wolf
        from organism.animal.sheep import Sheep
        from organism.animal.cyber_sheep import CyberSheep
        from organism.animal.fox import Fox
        from organism.animal.turtle import Turtle
        from organism.animal.antelope import Antelope

        from organism.plant.grass import Grass
        from organism.plant.dandelion import Dandelion
        from organism.plant.guarana import Guarana
        from organism.plant.nightshade_berry import NightshadeBerry
        from organism.plant.hogweed import Hogweed

        from organism.animal.human import Human

        for i in range(5):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            grass = Grass(Position(x, y), self)
            self.new_organisms.append(grass)
        for i in range(5):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            dandelion = Dandelion(Position(x, y), self)
            self.new_organisms.append(dandelion)
        for i in range(5):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            guarana = Guarana(Position(x, y), self)
            self.new_organisms.append(guarana)
        for i in range(5):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            nightshade_berry = NightshadeBerry(Position(x, y), self)
            self.new_organisms.append(nightshade_berry)
        for i in range(5):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            hogweed = Hogweed(Position(x, y), self)
            self.new_organisms.append(hogweed)
        for i in range(5):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            wolf = Wolf(Position(x, y), self)
            self.new_organisms.append(wolf)
        for i in range(5):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            sheep = Sheep(Position(x, y), self)
            self.new_organisms.append(sheep)
        for i in range(3):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            cyber_sheep = CyberSheep(Position(x, y), self)
            self.new_organisms.append(cyber_sheep)
        for i in range(5):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            fox = Fox(Position(x, y), self)
            self.new_organisms.append(fox)
        for i in range(5):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            turtle = Turtle(Position(x, y), self)
            self.new_organisms.append(turtle)
        for i in range(5):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            antelope = Antelope(Position(x, y), self)
            self.new_organisms.append(antelope)

        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        human = Human(Position(x, y), self)
        self.new_organisms.append(human)

    def dispatch_world_event(self, event):
        if self.listener:
            self.listener.dispatch(event)

    def get_organism_at(self, pos):
        for org in self.organisms + self.new_organisms:
            if pos.is_position_same(org.get_position()):
                return org
        return None

    def get_free_neighbours(self, pos, radius):
        return [p for p in self.get_neighbours(pos, radius) if self.get_organism_at(p) is None]

    @abstractmethod
    def is_position_valid(self, x, y):
        pass

    def is_position_valid_obj(self, pos):
        return self.is_position_valid(pos.get_x(), pos.get_y())

    @abstractmethod
    def get_new_position_in_direction(self, position, direction):
        pass

    def get_human(self):
        for org in self.organisms:
            from organism.animal.human import Human
            if isinstance(org, Human):
                return org
        return None

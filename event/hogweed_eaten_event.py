from event.event_interface import EventInterface
from organism.animal.animal import Animal
from organism.plant.hogweed import Hogweed


class HogweedEatenEvent(EventInterface):
    def __init__(self, hogweed: Hogweed, animal: Animal):
        self.hogweed = hogweed
        self.animal = animal

    def get_event_message(self):
        return (f"Sosnowsky hogweed eaten by {str(self.animal.get_species())}({self.animal.get_strength()}) "
                f"at position {self.hogweed.get_position().get_x()}, {self.hogweed.get_position().get_y()}. "
                f"The animal died.")

from event.event_interface import EventInterface
from organism.animal.animal import Animal


class AnimalBreedEvent(EventInterface):
    def __init__(self, parent: Animal, child: Animal):
        self.parent = parent
        self.child = child

    def get_event_message(self):
        return (f"Two animals {str(self.parent.get_species())} bred at position "
                f"{self.parent.get_position().get_x()}, {self.parent.get_position().get_y()} "
                f"and born a child at position {self.child.get_position().get_x()}, {self.child.get_position().get_y()}")


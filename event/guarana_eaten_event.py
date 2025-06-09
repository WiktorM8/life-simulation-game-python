from event.event_interface import EventInterface
from organism.animal.animal import Animal
from organism.plant.guarana import Guarana


class GuaranaEatenEvent(EventInterface):
    def __init__(self, guarana: Guarana, animal: Animal):
        self.guarana = guarana
        self.animal = animal

    def get_event_message(self):
        return (f"Guarana eaten by {str(self.animal.get_species())}({self.animal.get_strength()}) "
                f"at position {self.guarana.get_position().get_x()}, {self.guarana.get_position().get_y()}")

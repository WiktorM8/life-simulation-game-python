from event.event_interface import EventInterface
from organism.animal.animal import Animal


class AntelopeEscapeEvent(EventInterface):
    def __init__(self, defender: Animal, attacker: Animal):
        self.defender = defender
        self.attacker = attacker

    def get_event_message(self):
        return (f"Antelope escaped from {str(self.attacker.get_species())}({self.attacker.get_strength()}) "
                f"from position {self.attacker.get_position().get_x()}, {self.attacker.get_position().get_y()} "
                f"to position {self.defender.get_position().get_x()}, {self.defender.get_position().get_y()}")

from event.event_interface import EventInterface
from organism.animal.animal import Animal


class AnimalKillEvent(EventInterface):
    def __init__(self, attacker: Animal, victim: Animal):
        self.attacker = attacker
        self.victim = victim

    def get_event_message(self):
        return (f"{str(self.attacker.get_species())} killed {str(self.victim.get_species())} "
                f"at position {self.victim.get_position().get_x()}, {self.victim.get_position().get_y()}")

from event.event_interface import EventInterface
from organism.animal.animal import Animal
from organism.animal.human import Human


class HumanEscapeTheFightEvent(EventInterface):
    def __init__(self, human: Human, attacker: Animal):
        self.human = human
        self.attacker = attacker

    def get_event_message(self):
        return (f"Human escaped from the fight with {self.attacker.get_species()} "
                f"at position {self.attacker.get_position().get_x()}, "
                f"{self.attacker.get_position().get_y()} and moved to "
                f"{self.human.get_position().get_x()}, {self.human.get_position().get_y()}")

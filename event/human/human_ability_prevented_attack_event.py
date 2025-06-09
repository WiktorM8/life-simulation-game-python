from event.event_interface import EventInterface
from organism.animal.animal import Animal
from organism.animal.human import Human


class HumanAbilityPreventedAttackEvent(EventInterface):
    def __init__(self, human: Human, attacker: Animal):
        self.human = human
        self.attacker = attacker

    def get_event_message(self):
        return f"Human ability prevented attack from {self.attacker.get_species()}({self.attacker.get_strength()})"

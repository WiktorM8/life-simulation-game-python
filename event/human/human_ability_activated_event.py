from event.event_interface import EventInterface
from organism.animal.human import Human


class HumanAbilityActivatedEvent(EventInterface):
    def __init__(self, human: Human):
        self.human = human

    def get_event_message(self):
        return f"Human ability activated! Ability last for {self.human.get_ability_expiration_time()} turns."

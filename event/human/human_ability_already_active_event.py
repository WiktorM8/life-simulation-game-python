from event.event_interface import EventInterface
from organism.animal.human import Human


class HumanAbilityAlreadyActiveEvent(EventInterface):
    def __init__(self, human: Human):
        self.human = human

    def get_event_message(self):
        return f"Human ability is already active! It will expire in {self.human.get_ability_expiration_time()} turns."

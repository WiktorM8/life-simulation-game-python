from event.event_interface import EventInterface
from organism.animal.human import Human


class HumanAbilityExpiredEvent(EventInterface):
    def __init__(self, human: Human):
        self.human = human

    def get_event_message(self):
        return f"Human ability expired! Ability will be available again in {self.human.get_ability_cooldown()} turns."


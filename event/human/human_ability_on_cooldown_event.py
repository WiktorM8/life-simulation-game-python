from event.event_interface import EventInterface
from organism.animal.human import Human


class HumanAbilityOnCooldownEvent(EventInterface):
    def __init__(self, human: Human):
        self.human = human

    def get_event_message(self):
        return f"Human ability is on cooldown! Ability will be available in {self.human.get_ability_cooldown()} turns."

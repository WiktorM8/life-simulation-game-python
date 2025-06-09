from event.event_interface import EventInterface


class TurtleDefendedAttackEvent(EventInterface):
    def __init__(self, defender, attacker):
        self.defender = defender
        self.attacker = attacker

    def get_event_message(self) -> str:
        return (f"Turtle defended against attack from {self.attacker.get_species()}"
                f"({self.attacker.get_strength()}) at position "
                f"{self.defender.get_position().get_x()}, {self.defender.get_position().get_y()}")
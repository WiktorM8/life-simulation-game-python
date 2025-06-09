from event.event_interface import EventInterface
from organism.animal.human import Human
from organism.plant.hogweed import Hogweed


class HogweedBurnHumanEvent(EventInterface):
    def __init__(self, hogweed: Hogweed, human: Human):
        self.hogweed = hogweed
        self.human = human

    def get_event_message(self):
        return (f"Human went to close to Sosnowsky's hogweed and got burned to death at position: "
                f"{self.human.get_position().get_x()}, {self.human.get_position().get_y()}.")

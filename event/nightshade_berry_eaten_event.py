from event.event_interface import EventInterface


class NightshadeBerryEatenEvent(EventInterface):
    def __init__(self, berry, animal):
        self.berry = berry
        self.animal = animal

    def get_event_message(self) -> str:
        return (f"Nightshade berry eaten by {self.animal.get_species()}({self.animal.get_strength()}) "
                f"at position {self.berry.get_position().get_x()}, {self.berry.get_position().get_y()}. "
                f"The animal died.")

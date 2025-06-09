from event.event_interface import EventInterface


class InvalidHumanMoveEvent(EventInterface):
    def get_event_message(self):
        return "Invalid human move! human either wanted to go outside the border or chose invalid direction"

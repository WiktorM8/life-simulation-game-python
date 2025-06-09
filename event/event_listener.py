from typing import List

from event.event_handler_interface import EventHandlerInterface
from event.event_interface import EventInterface
from event.event_listener_interface import EventListenerInterface


class EventListener(EventListenerInterface):
    def __init__(self):
        self.event_buffer: List[EventInterface] = []

    def dispatch(self, event: EventInterface):
        self.event_buffer.append(event)

    def process_events(self, event_handler: EventHandlerInterface):
        for event in self.event_buffer:
            event_handler.handle_event(event)
        self.event_buffer.clear()

from abc import ABC, abstractmethod

from event.event_handler_interface import EventHandlerInterface
from event.event_interface import EventInterface


class EventListenerInterface(ABC):
    @abstractmethod
    def dispatch(self, event: EventInterface):
        pass

    @abstractmethod
    def process_events(self, event_handler: EventHandlerInterface):
        pass

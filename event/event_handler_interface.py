from abc import ABC, abstractmethod

from event.event_interface import EventInterface


class EventHandlerInterface(ABC):
    @abstractmethod
    def handle_event(self, event: EventInterface):
        pass

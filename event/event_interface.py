from abc import ABC, abstractmethod


class EventInterface(ABC):
    @abstractmethod
    def get_event_message(self) -> str:
        pass

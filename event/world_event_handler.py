from typing import List

from event.event_handler_interface import EventHandlerInterface
from event.event_interface import EventInterface


class WorldEventHandler(EventHandlerInterface):
    def __init__(self, message_list: List[str]):
        self.message_list = message_list

    def handle_event(self, event: EventInterface):
        self.log_message(event.get_event_message())

    def log_message(self, message: str):
        self.message_list.append(message)

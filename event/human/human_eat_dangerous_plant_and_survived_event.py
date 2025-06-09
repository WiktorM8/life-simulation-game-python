from event.event_interface import EventInterface
from organism.animal.human import Human
from organism.plant.plant import Plant


class HumanEatDangerousPlantAndSurvivedEvent(EventInterface):
    def __init__(self, human: Human, plant: Plant):
        self.human = human
        self.plant = plant

    def get_event_message(self):
        return f"Human ate a dangerous plant {self.plant.get_species()} but he survived thanks to his ability!"

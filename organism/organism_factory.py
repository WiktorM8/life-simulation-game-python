class OrganismFactory:
    @staticmethod
    def create(name, position, world):
        from organism.animal.wolf import Wolf
        from organism.animal.sheep import Sheep
        from organism.animal.cyber_sheep import CyberSheep
        from organism.animal.fox import Fox
        from organism.animal.turtle import Turtle
        from organism.animal.antelope import Antelope
        from organism.animal.human import Human
        from organism.plant.dandelion import Dandelion
        from organism.plant.grass import Grass
        from organism.plant.guarana import Guarana
        from organism.plant.nightshade_berry import NightshadeBerry
        from organism.plant.hogweed import Hogweed

        organism_map = {
            "Wolf": Wolf,
            "Sheep": Sheep,
            "CyberSheep": CyberSheep,
            "Fox": Fox,
            "Turtle": Turtle,
            "Antelope": Antelope,
            "Dandelion": Dandelion,
            "Grass": Grass,
            "Guarana": Guarana,
            "Nightshade": NightshadeBerry,
            "SosnowskyHogweed": Hogweed,
            "Human": Human
        }

        organism_class = organism_map.get(name)
        if organism_class:
            return organism_class(position, world)
        return None

class OrganismRegistry:
    @staticmethod
    def get_available_organism_names(human_alive):
        base_organisms = [
            "Wolf", "Sheep", "CyberSheep", "Fox", "Turtle", "Antelope",
            "Dandelion", "Grass", "Guarana", "Nightshade", "SosnowskyHogweed"
        ]

        if human_alive:
            return base_organisms
        else:
            return base_organisms + ["Human"]

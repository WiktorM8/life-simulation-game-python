from game.game_manager import GameManager


class LifeSimulationGame:
    def __init__(self, game_manager):
        self.game_manager = game_manager

    def start_game(self):
        self.game_manager.run()


game_manager = GameManager()
life_simulation_game = LifeSimulationGame(game_manager)

life_simulation_game.start_game()

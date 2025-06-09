from world.base_world import BaseWorld
from world.position import Position
from world.player_direction import PlayerDirection


class SquareWorld(BaseWorld):
    def __init__(self, width, height, game_manager):
        super().__init__(width, height, game_manager)

    def is_position_valid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_neighbours(self, position, radius):
        neighbours = []
        x, y = position.x, position.y
        radius_squared = radius * radius

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue
                if dx * dx + dy * dy > radius_squared:
                    continue

                new_x = x + dx
                new_y = y + dy

                if self.is_position_valid(new_x, new_y):
                    neighbours.append(Position(new_x, new_y))

        return neighbours

    def get_new_position_in_direction(self, position, direction):
        dx, dy = 0, 0

        if direction == PlayerDirection.UP:
            dy = -1
        elif direction == PlayerDirection.DOWN:
            dy = 1
        elif direction == PlayerDirection.LEFT:
            dx = -1
        elif direction == PlayerDirection.RIGHT:
            dx = 1
        else:
            return None

        new_x = position.x + dx
        new_y = position.y + dy

        if self.is_position_valid(new_x, new_y):
            return Position(new_x, new_y)
        return None

from world.base_world import BaseWorld
from world.position import Position
from world.player_direction import PlayerDirection


def _get_radius2_ring(y):
    if y % 2 == 0:
        return [
            (+2, 0), (+1, -1), (0, -2), (-1, -2), (-2, -1), (-2, 0),
            (-2, +1), (-1, +2), (0, +2), (+1, +1), (+2, +1), (+1, -1)
        ]
    else:
        return [
            (+2, 0), (+2, -1), (+1, -2), (0, -2), (-1, -1), (-2, -1),
            (-2, 0), (-1, +1), (0, +2), (+1, +2), (+2, +1), (+1, +1)
        ]


class HexWorld(BaseWorld):
    def __init__(self, width, height, game_manager):
        super().__init__(width, height, game_manager)

    def is_position_valid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_neighbours(self, position, radius):
        neighbours = []
        x, y = position.x, position.y

        if y % 2 == 0:
            offsets1 = [(+1, 0), (0, -1), (-1, -1), (-1, 0), (-1, +1), (0, +1)]
        else:
            offsets1 = [(+1, 0), (+1, -1), (0, -1), (-1, 0), (0, +1), (+1, +1)]

        if radius == 1:
            for dx, dy in offsets1:
                nx, ny = x + dx, y + dy
                if self.is_position_valid(nx, ny):
                    neighbours.append(Position(nx, ny))

        elif radius == 2:
            ring2 = _get_radius2_ring(y)
            for dx, dy in ring2 + offsets1:
                nx, ny = x + dx, y + dy
                if self.is_position_valid(nx, ny):
                    neighbours.append(Position(nx, ny))

        else:
            for dx_base, dy_base in offsets1:
                for r in range(1, radius + 1):
                    nx = x + dx_base * r
                    ny = y + dy_base * r
                    if self.is_position_valid(nx, ny):
                        neighbours.append(Position(nx, ny))

        return neighbours

    def get_new_position_in_direction(self, position, direction):
        x, y = position.x, position.y
        is_even_row = (y % 2 == 0)

        dx, dy = 0, 0
        if direction == PlayerDirection.LEFT:
            dx = -1
        elif direction == PlayerDirection.RIGHT:
            dx = 1
        elif direction == PlayerDirection.UP_LEFT:
            dy = -1
            dx = -1 if is_even_row else 0
        elif direction == PlayerDirection.UP_RIGHT:
            dy = -1
            dx = 0 if is_even_row else 1
        elif direction == PlayerDirection.DOWN_LEFT:
            dy = 1
            dx = -1 if is_even_row else 0
        elif direction == PlayerDirection.DOWN_RIGHT:
            dy = 1
            dx = 0 if is_even_row else 1
        else:
            return None

        new_x, new_y = x + dx, y + dy
        if self.is_position_valid(new_x, new_y):
            return Position(new_x, new_y)
        return None

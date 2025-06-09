from enum import Enum


class PlayerDirection(Enum):
    UP = "Up"
    DOWN = "Down"
    LEFT = "Left"
    RIGHT = "Right"
    UP_LEFT = "Up_Left"
    UP_RIGHT = "Up_Right"
    DOWN_LEFT = "Down_Left"
    DOWN_RIGHT = "Down_Right"
    NONE = "None"

    @staticmethod
    def from_string(direction: str):
        direction_upper = direction.upper()
        mapping = {
            "UP": PlayerDirection.UP,
            "DOWN": PlayerDirection.DOWN,
            "LEFT": PlayerDirection.LEFT,
            "RIGHT": PlayerDirection.RIGHT,
            "UP_LEFT": PlayerDirection.UP_LEFT,
            "UPRIGHT": PlayerDirection.UP_RIGHT,
            "UP_RIGHT": PlayerDirection.UP_RIGHT,
            "DOWN_LEFT": PlayerDirection.DOWN_LEFT,
            "DOWNRIGHT": PlayerDirection.DOWN_RIGHT,
            "DOWN_RIGHT": PlayerDirection.DOWN_RIGHT,
        }
        return mapping.get(direction_upper, PlayerDirection.NONE)

    def __str__(self):
        return self.value

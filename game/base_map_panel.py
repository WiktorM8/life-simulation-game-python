from abc import ABC, abstractmethod
import pygame
import os


class BaseMapPanel(ABC):
    class DrawRequest:
        def __init__(self, x, y, texture):
            self.x = x
            self.y = y
            self.texture = texture

    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.draw_requests = []
        self.texture_cache = {}

    def add_draw_request(self, x, y, texture_name):
        self.draw_requests.append(self.DrawRequest(x, y, texture_name))

    def get_draw_requests(self):
        return self.draw_requests

    def clear_draw_requests(self):
        self.draw_requests.clear()

    def paint_component(self, surface):
        for request in self.draw_requests:
            self.draw_texture_at(surface, request.x, request.y, request.texture)
        self.clear_draw_requests()

    def get_texture(self, name):
        if name in self.texture_cache:
            return self.texture_cache[name]

        try:
            path = os.path.join("textures/", name)
            img = pygame.image.load(path).convert_alpha()
            self.texture_cache[name] = img
            return img
        except pygame.error as e:
            print(f"Nie można załadować tekstury: {name} ({e})")
            return None

    @abstractmethod
    def screen_to_map_coordinates(self, point):
        raise NotImplementedError()

    @abstractmethod
    def draw_texture_at(self, surface, x, y, texture_name):
        raise NotImplementedError()

import pygame

from game.base_map_panel import BaseMapPanel


class SquareMapPanel(BaseMapPanel):
    def __init__(self, world_width, world_height, game_manager):
        super().__init__(game_manager)
        self.world_width = world_width
        self.world_height = world_height
        self.cell_size = 0
        self.background_color = (255, 255, 255)

    def paint_component(self, surface):
        surface.fill(self.background_color)

        self.calculate_cell_size(surface)
        self.draw_grid(surface)
        super().paint_component(surface)

    def calculate_cell_size(self, surface):
        width, height = surface.get_size()
        map_width = int(width * 2 / 3)
        map_height = height

        cell_width = map_width // self.world_width
        cell_height = map_height // self.world_height

        self.cell_size = min(cell_width, cell_height)

    def draw_grid(self, surface):
        color = (211, 211, 211)
        for i in range(self.world_width + 1):
            x = i * self.cell_size
            pygame.draw.line(surface, color, (x, 0), (x, self.cell_size * self.world_height))
        for i in range(self.world_height + 1):
            y = i * self.cell_size
            pygame.draw.line(surface, color, (0, y), (self.cell_size * self.world_width, y))

    def draw_texture_at(self, surface, x, y, texture_name):
        center_x, center_y = self.get_cell_center(x, y)
        img = self.get_texture(texture_name)
        if img is not None:
            img_scaled = pygame.transform.scale(img, (self.cell_size, self.cell_size))
            surface.blit(img_scaled, (center_x - self.cell_size // 2, center_y - self.cell_size // 2))

    def get_cell_center(self, x, y):
        screen_x = x * self.cell_size + self.cell_size // 2
        screen_y = y * self.cell_size + self.cell_size // 2
        return screen_x, screen_y

    def get_cell_size(self):
        return self.cell_size

    def screen_to_map_coordinates(self, point):
        x, y = point
        map_x = x // self.cell_size
        map_y = y // self.cell_size

        if 0 <= map_x < self.world_width and 0 <= map_y < self.world_height:
            return map_x, map_y
        else:
            return None

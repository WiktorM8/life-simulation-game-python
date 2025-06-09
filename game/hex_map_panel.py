import pygame
import math

from game.base_map_panel import BaseMapPanel


class HexMapPanel(BaseMapPanel):
    def __init__(self, world_width, world_height, game_manager):
        super().__init__(game_manager)
        self.world_width = world_width
        self.world_height = world_height
        self.offset_x = 0
        self.offset_y = 0
        self.hex_size = 0
        self.background_color = (255, 255, 255)

    def paint_component(self, surface):
        surface.fill(self.background_color)
        self.calculate_hex_size(surface)

        for y in range(self.world_height):
            for x in range(self.world_width):
                center = self.get_hex_center(x, y)
                hex_points = self.create_hexagon(center)
                pygame.draw.polygon(surface, (211, 211, 211), hex_points, width=1)

        super().paint_component(surface)

    def calculate_hex_size(self, surface):
        width, height = surface.get_size()

        map_width = int(width * 2 / 3)
        map_height = height

        hex_width = map_width / (self.world_width + 0.5)
        hex_height = map_height / (self.world_height * 0.75 + 0.25)

        self.hex_size = int(min(hex_width / math.sqrt(3), hex_height / 2.0))

        total_grid_width = self.world_width * math.sqrt(3) * self.hex_size + math.sqrt(3) * self.hex_size / 2
        total_grid_height = (self.world_height - 1) * 1.5 * self.hex_size + 2 * self.hex_size

        self.offset_x = int((map_width - total_grid_width) / 2) + self.hex_size
        self.offset_y = int((map_height - total_grid_height) / 2) + self.hex_size

    def create_hexagon(self, center):
        cx, cy = center
        points = []
        for i in range(6):
            angle = math.radians(60 * i - 30)
            x = cx + int(self.hex_size * math.cos(angle))
            y = cy + int(self.hex_size * math.sin(angle))
            points.append((x, y))
        return points

    def draw_texture_at(self, surface, x, y, texture_name):
        center = self.get_hex_center(x, y)
        img = self.get_texture(texture_name)
        if img is not None:
            img_scaled = pygame.transform.scale(img, (self.hex_size, self.hex_size))
            surface.blit(img_scaled, (center[0] - self.hex_size // 2, center[1] - self.hex_size // 2))

    def get_hex_center(self, x, y):
        w = math.sqrt(3) * self.hex_size
        h = 2 * self.hex_size
        horiz_spacing = w
        vert_spacing = 0.75 * h

        screen_x = self.offset_x + x * horiz_spacing + (y % 2) * (horiz_spacing / 2)
        screen_y = self.offset_y + y * vert_spacing

        return int(screen_x), int(screen_y)

    def get_hex_size(self):
        return self.hex_size

    def screen_to_map_coordinates(self, point):
        x, y = point
        w = math.sqrt(3) * self.hex_size
        h = 2 * self.hex_size
        horiz_spacing = w
        vert_spacing = 0.75 * h

        approx_y = int((y - self.offset_y) / vert_spacing)
        approx_x = int((x - self.offset_x - ((approx_y % 2) * horiz_spacing / 2)) / horiz_spacing)

        for dy in range(-1, 2):
            for dx in range(-1, 2):
                test_x = approx_x + dx
                test_y = approx_y + dy

                if not (0 <= test_x < self.world_width and 0 <= test_y < self.world_height):
                    continue

                center = self.get_hex_center(test_x, test_y)
                hex_points = self.create_hexagon(center)
                polygon = pygame.draw.polygon(pygame.Surface((1, 1)), (0, 0, 0), hex_points)
                if self.point_in_polygon((x, y), hex_points):
                    return test_x, test_y

        return None

    @staticmethod
    def point_in_polygon(point, polygon):
        x, y = point
        inside = False
        n = len(polygon)
        px1, py1 = polygon[0]
        for i in range(n + 1):
            px2, py2 = polygon[i % n]
            if y > min(py1, py2):
                if y <= max(py1, py2):
                    if x <= max(px1, px2):
                        if py1 != py2:
                            xinters = (y - py1) * (px2 - px1) / (py2 - py1) + px1
                        if px1 == px2 or x <= xinters:
                            inside = not inside
            px1, py1 = px2, py2
        return inside

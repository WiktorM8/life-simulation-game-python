import pygame
import sys
import os
from enum import Enum
from typing import Optional

from organism.organism import Organism
from organism.organism_factory import OrganismFactory
from organism.organism_registry import OrganismRegistry
from world.base_world import BaseWorld
from world.hex_world import HexWorld
from world.square_world import SquareWorld
from world.player_direction import PlayerDirection
from game.base_map_panel import BaseMapPanel
from game.hex_map_panel import HexMapPanel
from game.square_map_panel import SquareMapPanel
from world.position import Position
from event.event_listener import EventListener
from event.event_handler_interface import EventHandlerInterface
from event.world_event_handler import WorldEventHandler


class GameScreenState(Enum):
    MENU = 0
    GAME = 1
    WORLD_CREATION = 2


class InputActive(Enum):
    NONE = 0
    WIDTH = 1
    HEIGHT = 2


class DialogType(Enum):
    NONE = 0
    SAVE = 1
    LOAD = 2
    ORGANISM_SELECTION = 3


class WorldType(Enum):
    SQUARE = "Kwadratowy"
    HEX = "Heksagonalny"


class GameScreen:
    def __init__(self, game_manager):
        pygame.init()
        self.game_manager = game_manager
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game")
        self.font = pygame.font.Font(None, 24)
        self.visible = False

    def set_visible(self, visible):
        self.visible = visible

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height


class GameManager:
    def __init__(self):
        self.player_direction = PlayerDirection.NONE
        self.player_alive = False
        self.world: Optional[BaseWorld] = None
        self.map_panel: Optional[BaseMapPanel] = None
        self.game_screen = GameScreen(self)
        self.event_listener = EventListener()
        self.messages = []
        self.event_handler: EventHandlerInterface = WorldEventHandler(self.messages)
        self.player_status_label = "Player:"
        self.player_direction_label = "Direction:"
        self.running = True
        self.current_state = GameScreenState.MENU
        self.clock = pygame.time.Clock()

        self.width_input = "20"
        self.height_input = "20"
        self.world_type_selected = WorldType.SQUARE
        self.input_active = None

        self.dialog_active = False
        self.dialog_type = None
        self.dialog_input = ""
        self.organism_names = []
        self.selected_click_pos = None

    def set_player_direction(self, direction: PlayerDirection):
        self.player_direction = direction

    def get_player_direction(self) -> PlayerDirection:
        return self.player_direction

    def set_player_alive(self, alive: bool):
        self.player_alive = alive

    def is_player_alive(self) -> bool:
        return self.player_alive

    def menu(self):
        self.current_state = GameScreenState.MENU

    def show_world_creation_form(self):
        self.current_state = GameScreenState.WORLD_CREATION

    def start_game(self):
        self.current_state = GameScreenState.GAME
        if self.world:
            self.world.merge_new_organisms()
            for organism in self.world.get_organisms():
                if organism.is_alive():
                    organism.draw()
            self.update_player_info_labels()

    def game_main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_mouse_click(event.pos)

                elif event.type == pygame.TEXTINPUT:
                    if self.dialog_active:
                        self.dialog_input += event.text
                    elif self.current_state == GameScreenState.WORLD_CREATION and self.input_active:
                        if self.input_active == InputActive.WIDTH:
                            if event.text.isdigit():
                                self.width_input += event.text
                        elif self.input_active == InputActive.HEIGHT:
                            if event.text.isdigit():
                                self.height_input += event.text

            self.render()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def handle_keydown(self, event):
        if self.dialog_active:
            if event.key == pygame.K_RETURN:
                self.handle_dialog_confirm()
            elif event.key == pygame.K_ESCAPE:
                self.dialog_active = False
            elif event.key == pygame.K_BACKSPACE:
                self.dialog_input = self.dialog_input[:-1]
            return

        if self.current_state == GameScreenState.MENU:
            if event.key == pygame.K_1:
                self.show_world_creation_form()
            elif event.key == pygame.K_2:
                self.load_game_dialog()
            elif event.key == pygame.K_3:
                self.running = False

        elif self.current_state == GameScreenState.WORLD_CREATION:
            if event.key == pygame.K_RETURN:
                self.create_world_and_start()
            elif event.key == pygame.K_TAB:
                if self.world_type_selected == WorldType.SQUARE:
                    self.world_type_selected = WorldType.HEX
                else:
                    self.world_type_selected = WorldType.SQUARE
            elif event.key == pygame.K_BACKSPACE:
                if self.input_active == InputActive.WIDTH:
                    self.width_input = self.width_input[:-1]
                elif self.input_active == InputActive.HEIGHT:
                    self.height_input = self.height_input[:-1]

        elif self.current_state == GameScreenState.GAME:
            self.handle_game_keys(event)

    def handle_game_keys(self, event):
        if event.key == pygame.K_KP8:
            self.set_player_direction(PlayerDirection.UP)
        elif event.key == pygame.K_KP2:
            self.set_player_direction(PlayerDirection.DOWN)
        elif event.key == pygame.K_KP4:
            self.set_player_direction(PlayerDirection.LEFT)
        elif event.key == pygame.K_KP6:
            self.set_player_direction(PlayerDirection.RIGHT)
        elif event.key == pygame.K_KP7:
            self.set_player_direction(PlayerDirection.UP_LEFT)
        elif event.key == pygame.K_KP9:
            self.set_player_direction(PlayerDirection.UP_RIGHT)
        elif event.key == pygame.K_KP1:
            self.set_player_direction(PlayerDirection.DOWN_LEFT)
        elif event.key == pygame.K_KP3:
            self.set_player_direction(PlayerDirection.DOWN_RIGHT)

        elif event.key == pygame.K_UP:
            self.set_player_direction(PlayerDirection.UP)
        elif event.key == pygame.K_DOWN:
            self.set_player_direction(PlayerDirection.DOWN)
        elif event.key == pygame.K_LEFT:
            self.set_player_direction(PlayerDirection.LEFT)
        elif event.key == pygame.K_RIGHT:
            self.set_player_direction(PlayerDirection.RIGHT)

        elif event.key == pygame.K_t:
            self.next_turn()
        elif event.key == pygame.K_s:
            self.save_game_dialog()
        elif event.key == pygame.K_l:
            self.load_game_dialog()
        elif event.key == pygame.K_p:
            self.activate_human_ability()

        self.update_player_info_labels()

    def next_turn(self):
        if self.world:
            self.clear_messages()
            self.world.make_turn()
            self.event_listener.process_events(self.event_handler)
            self.call_draw_on_organisms()

    def activate_human_ability(self):
        if self.world and self.world.get_human():
            self.world.get_human().activate_ability()
            self.call_draw_on_organisms()
            self.event_listener.process_events(self.event_handler)

    def handle_mouse_click(self, pos):
        if self.current_state == GameScreenState.MENU:
            button_height = 60
            button_y_start = 300
            if button_y_start <= pos[1] <= button_y_start + button_height:
                self.show_world_creation_form()
            elif button_y_start + 80 <= pos[1] <= button_y_start + 80 + button_height:
                self.load_game_dialog()
            elif button_y_start + 160 <= pos[1] <= button_y_start + 160 + button_height:
                self.running = False

        elif self.current_state == GameScreenState.WORLD_CREATION:
            input_y = 250
            if 300 <= pos[0] <= 500:
                if input_y <= pos[1] <= input_y + 30:
                    self.input_active = InputActive.WIDTH
                elif input_y + 50 <= pos[1] <= input_y + 80:
                    self.input_active = InputActive.HEIGHT
                elif input_y + 100 <= pos[1] <= input_y + 130:
                    if self.world_type_selected == WorldType.SQUARE:
                        self.world_type_selected = WorldType.HEX
                    else:
                        self.world_type_selected = WorldType.SQUARE
            if 400 <= pos[0] <= 500 and 400 <= pos[1] <= 440:
                self.create_world_and_start()

        elif self.current_state == GameScreenState.GAME:
            if self.map_panel and pos[0] < 900:
                self.handle_map_click(pos)

    def handle_map_click(self, screen_point):
        if not self.map_panel:
            return

        map_coords = self.map_panel.screen_to_map_coordinates(screen_point)
        if map_coords is None:
            return

        map_x, map_y = map_coords
        self.selected_click_pos = (map_x, map_y)

        is_human_alive = self.is_player_alive()
        self.show_organism_selection_dialog(is_human_alive)

    def show_organism_selection_dialog(self, human_alive):
        self.organism_names = OrganismRegistry.get_available_organism_names(human_alive)
        self.dialog_active = True
        self.dialog_type = DialogType.ORGANISM_SELECTION
        self.dialog_input = ""

    def create_world_and_start(self):
        try:
            w = int(self.width_input) if self.width_input else 20
            h = int(self.height_input) if self.height_input else 20
            is_hex = self.world_type_selected == WorldType.HEX

            if self.world:
                self.world.clear_world()

            if is_hex:
                self.world = HexWorld(w, h, self)
                self.map_panel = HexMapPanel(w, h, self)
            else:
                self.world = SquareWorld(w, h, self)
                self.map_panel = SquareMapPanel(w, h, self)

            self.world.set_event_listener(self.event_listener)
            self.world.generate_starting_organisms()
            self.world.merge_new_organisms()

            self.start_game()

        except ValueError:
            print("Niepoprawne liczby!")

    def save_game_dialog(self):
        self.dialog_active = True
        self.dialog_type = DialogType.SAVE
        self.dialog_input = ""

    def load_game_dialog(self):
        self.dialog_active = True
        self.dialog_type = DialogType.LOAD
        self.dialog_input = ""

    def handle_dialog_confirm(self):
        if self.dialog_type == DialogType.SAVE:
            self.save_game_to_file(self.dialog_input)
        elif self.dialog_type == DialogType.LOAD:
            self.load_game_from_file(self.dialog_input)
        elif self.dialog_type == DialogType.ORGANISM_SELECTION:
            try:
                choice = int(self.dialog_input)
                if 0 <= choice < len(self.organism_names):
                    organism_name = self.organism_names[choice]
                    if self.selected_click_pos:
                        map_x, map_y = self.selected_click_pos
                        new_organism = OrganismFactory.create(organism_name, Position(map_x, map_y), self.world)
                        if new_organism:
                            self.set_organism_at(map_x, map_y, new_organism)
                            self.world.merge_new_organisms()
                            self.call_draw_on_organisms()
                            self.clear_messages()
            except ValueError:
                pass

        self.dialog_active = False

    def set_organism_at(self, x, y, organism):
        try:
            self.remove_organism_at(x, y)
            self.world.add_new_organism(organism)
        except Exception as e:
            print(f"Error: {e}")

    def remove_organism_at(self, x, y):
        organisms_to_remove = []
        for organism in self.world.get_organisms():
            if organism.get_position().get_x() == x and organism.get_position().get_y() == y:
                organisms_to_remove.append(organism)

        for organism in organisms_to_remove:
            self.world.get_organisms().remove(organism)

    def call_draw_on_organisms(self):
        if self.world:
            for organism in self.world.get_organisms():
                if organism.is_alive():
                    organism.draw()

    def update_player_info_labels(self):
        alive_text = "Alive" if self.is_player_alive() else "Dead"
        direction_text = self.get_player_direction().value.replace('_', ' ')

        self.player_status_label = f"Player: {alive_text}"
        self.player_direction_label = f"Direction: {direction_text}"

        self.call_draw_on_organisms()

    def get_world(self) -> BaseWorld:
        return self.world

    def draw_texture_on_map(self, x, y, texture):
        if self.map_panel:
            self.map_panel.add_draw_request(x, y, texture)

    def clear_messages(self):
        self.messages.clear()

    def save_game_to_file(self, filename):
        if not filename or filename.strip() == "":
            print("Zapisywanie anulowane lub niepoprawna nazwa pliku.")
            return

        if not filename.endswith(".dat"):
            filename += ".dat"

        if os.path.exists(filename):
            print(f"Plik {filename} już istnieje. Nadpisuję...")

        try:
            with open(filename, 'w') as writer:
                world_type = "Hex" if isinstance(self.world, HexWorld) else "Square"
                line = f"{world_type} {self.world.get_width()} {self.world.get_height()}"
                writer.write(line + "\n")

                for organism in self.world.get_organisms():
                    if organism.is_alive():
                        writer.write(organism.serialize() + "\n")

            print(f"Gra została pomyślnie zapisana do pliku: {filename}")

        except Exception as e:
            print(f"Błąd podczas zapisu gry do pliku: {e}")

    def load_game_from_file(self, filename):
        if not filename or filename.strip() == "":
            print("Wczytywanie anulowane lub niepoprawna nazwa pliku.")
            return

        if not filename.endswith(".dat"):
            filename += ".dat"

        if not os.path.exists(filename):
            print(f"Plik nie został znaleziony: {filename}")
            return

        try:
            with open(filename, 'r') as reader:
                header = reader.readline().strip().split()
                if len(header) < 3:
                    raise ValueError("Niepoprawny format pliku.")

                world_type = header[0]
                width = int(header[1])
                height = int(header[2])

                if world_type.lower() == "hex":
                    self.world = HexWorld(width, height, self)
                    self.map_panel = HexMapPanel(width, height, self)
                else:
                    self.world = SquareWorld(width, height, self)
                    self.map_panel = SquareMapPanel(width, height, self)

                self.world.set_event_listener(self.event_listener)

                for line in reader:
                    line = line.strip()
                    if line:
                        organism = Organism.deserialize(line, self.world)
                        if organism:
                            self.world.add_organism(organism)

            print(f"Gra została pomyślnie wczytana z pliku: {filename}")

            self.current_state = GameScreenState.GAME
            self.world.merge_new_organisms()
            self.call_draw_on_organisms()
            self.clear_messages()
            self.update_player_info_labels()

        except Exception as e:
            print(f"Błąd podczas wczytywania gry: {e}")

    def render(self):
        self.game_screen.screen.fill((0, 0, 0))

        if self.current_state == GameScreenState.MENU:
            self.render_menu()
        elif self.current_state == GameScreenState.WORLD_CREATION:
            self.render_world_creation()
        elif self.current_state == GameScreenState.GAME:
            self.render_game()

        if self.dialog_active:
            self.render_dialog()

        pygame.display.flip()

    def render_menu(self):
        font = pygame.font.Font(None, 48)
        title = font.render("Game Menu", True, (255, 255, 255))
        self.game_screen.screen.blit(title, (500, 200))

        button_font = pygame.font.Font(None, 32)
        buttons = [
            "1. Nowa gra",
            "2. Wczytaj grę",
            "3. Wyjdź"
        ]

        for i, button_text in enumerate(buttons):
            button = button_font.render(button_text, True, (255, 255, 255))
            self.game_screen.screen.blit(button, (500, 300 + i * 80))

    def render_world_creation(self):
        font = pygame.font.Font(None, 36)
        title = font.render("Tworzenie świata", True, (255, 255, 255))
        self.game_screen.screen.blit(title, (400, 150))

        input_font = pygame.font.Font(None, 24)

        width_label = input_font.render("Szerokość:", True, (255, 255, 255))
        self.game_screen.screen.blit(width_label, (200, 250))

        width_color = (255, 255, 0) if self.input_active == InputActive.WIDTH else (255, 255, 255)
        width_text = input_font.render(self.width_input, True, width_color)
        pygame.draw.rect(self.game_screen.screen, (50, 50, 50), (300, 250, 200, 30))
        self.game_screen.screen.blit(width_text, (305, 255))

        height_label = input_font.render("Wysokość:", True, (255, 255, 255))
        self.game_screen.screen.blit(height_label, (200, 300))

        height_color = (255, 255, 0) if self.input_active == InputActive.HEIGHT else (255, 255, 255)
        height_text = input_font.render(self.height_input, True, height_color)
        pygame.draw.rect(self.game_screen.screen, (50, 50, 50), (300, 300, 200, 30))
        self.game_screen.screen.blit(height_text, (305, 305))

        world_type_label = input_font.render("Typ świata:", True, (255, 255, 255))
        self.game_screen.screen.blit(world_type_label, (200, 350))

        selected_type = input_font.render(self.world_type_selected.value, True, (255, 255, 0))
        self.game_screen.screen.blit(selected_type, (300, 350))

        pygame.draw.rect(self.game_screen.screen, (0, 100, 0), (400, 400, 100, 40))
        start_text = input_font.render("Start", True, (255, 255, 255))
        self.game_screen.screen.blit(start_text, (430, 410))

    def render_wrapped_text(self, surface, text, font, color, x, y, max_width, line_height):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            test_width, _ = font.size(test_line)
            if test_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "

        if current_line:
            lines.append(current_line)

        for i, line in enumerate(lines):
            rendered = font.render(line.strip(), True, color)
            surface.blit(rendered, (x, y + i * line_height))

    def render_game(self):
        self.call_draw_on_organisms()

        if self.map_panel:
            self.map_panel.paint_component(self.game_screen.screen)

        info_x = 920
        font = pygame.font.Font(None, 20)

        status_text = font.render(self.player_status_label, True, (0, 0, 0))
        self.game_screen.screen.blit(status_text, (info_x, 10))

        direction_text = font.render(self.player_direction_label, True, (0, 0, 0))
        self.game_screen.screen.blit(direction_text, (info_x, 35))

        pygame.draw.rect(self.game_screen.screen, (220, 220, 200), (910, 60, 280, 600))

        pygame.draw.rect(self.game_screen.screen, (255, 255, 255), (910, 60, 280, 600), 2)

        font = pygame.font.Font(None, 14)
        message_y = 80
        y = message_y
        for message in self.messages[-20:]:
            self.render_wrapped_text(
                self.game_screen.screen,
                str(message),
                font,
                (0, 0, 0),
                info_x,
                y,
                max_width=260,
                line_height=15
            )

            lines = len(str(message).split()) // 6 + 1
            y += lines * 15

    def render_dialog(self):
        overlay = pygame.Surface((self.game_screen.width, self.game_screen.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.game_screen.screen.blit(overlay, (0, 0))

        dialog_width, dialog_height = 400, 200
        if self.dialog_type == DialogType.ORGANISM_SELECTION:
            dialog_height = 400
        dialog_x = (self.game_screen.width - dialog_width) // 2
        dialog_y = (self.game_screen.height - dialog_height) // 2

        pygame.draw.rect(self.game_screen.screen, (50, 50, 50),
                         (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(self.game_screen.screen, (255, 255, 255),
                         (dialog_x, dialog_y, dialog_width, dialog_height), 2)

        font = pygame.font.Font(None, 24)

        if self.dialog_type == DialogType.SAVE:
            title = font.render("Zapisz grę - podaj nazwę pliku:", True, (255, 255, 255))
            self.game_screen.screen.blit(title, (dialog_x + 20, dialog_y + 20))
        elif self.dialog_type == DialogType.LOAD:
            title = font.render("Wczytaj grę - podaj nazwę pliku:", True, (255, 255, 255))
            self.game_screen.screen.blit(title, (dialog_x + 20, dialog_y + 20))
        elif self.dialog_type == DialogType.ORGANISM_SELECTION:
            title = font.render("Wybierz organizm (podaj numer):", True, (255, 255, 255))
            self.game_screen.screen.blit(title, (dialog_x + 20, dialog_y + 20))

            for i, name in enumerate(self.organism_names):
                option_text = font.render(f"{i}: {name}", True, (255, 255, 255))
                self.game_screen.screen.blit(option_text, (dialog_x + 20, dialog_y + 50 + i * 20))

        input_text = font.render(self.dialog_input, True, (255, 255, 255))
        pygame.draw.rect(self.game_screen.screen, (30, 30, 30),
                         (dialog_x + 20, dialog_y + dialog_height - 60, dialog_width - 40, 30))
        self.game_screen.screen.blit(input_text, (dialog_x + 25, dialog_y + dialog_height - 55))

    def run(self):
        self.game_screen.set_visible(True)
        self.menu()
        self.game_main_loop()

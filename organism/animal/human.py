import random
from organism.animal.animal import Animal
from world.player_direction import PlayerDirection
from world.position import Position
from organism.organism_type import OrganismType
from organism.animal.animal_species import AnimalSpecies


class Human(Animal):
    ABILITY_COOLDOWN = 5
    ABILITY_EXPIRATION_TIME = 5

    def __init__(self, position, world):
        super().__init__(position, AnimalSpecies.HUMAN, 5, 4, world)
        self.ability_cooldown = 0
        self.ability_expiration_time = 0
        self.ability_active = False
        self.set_alive(True)

    def set_ability_active(self, value: bool):
        self.ability_active = value

    def is_ability_active(self):
        return self.ability_active

    def set_ability_cooldown(self, value: int):
        self.ability_cooldown = value

    def get_ability_cooldown(self):
        return self.ability_cooldown

    def set_ability_expiration_time(self, value: int):
        self.ability_expiration_time = value

    def get_ability_expiration_time(self):
        return self.ability_expiration_time

    def make_child(self):
        return Human(self.get_position(), self.get_world())

    def get_texture(self):
        return "player.png"

    def make_move(self):
        direction = self.get_world().get_game_manager().get_player_direction()
        if direction == PlayerDirection.NONE:
            return

        new_pos = self.get_world().get_new_position_in_direction(self.get_position(), direction)
        if new_pos:
            self.move_to(new_pos)
        else:
            from event.human.invalid_human_move_event import InvalidHumanMoveEvent
            self.get_world().dispatch_world_event(InvalidHumanMoveEvent())

    def action(self):
        super().action()

        if self.ability_cooldown > 0:
            self.ability_cooldown -= 1

        if self.ability_expiration_time > 0:
            self.ability_expiration_time -= 1
            if self.ability_expiration_time == 0:
                self.ability_active = False
                self.ability_cooldown = Human.ABILITY_COOLDOWN
                from event.human.human_ability_expired_event import HumanAbilityExpiredEvent
                self.get_world().dispatch_world_event(HumanAbilityExpiredEvent(self))

    def collision(self, other):
        if self.is_ability_active():
            if other.get_type() == OrganismType.ANIMAL and self.get_strength() < other.get_strength():
                self.move_to(self.get_last_position())
                from event.human.human_escape_the_fight_event import HumanEscapeTheFightEvent
                self.get_world().dispatch_world_event(HumanEscapeTheFightEvent(self, other))
                return
        super().collision(other)

    def defend_attack(self, attacker):
        if self.is_ability_active():
            if attacker.get_type() == OrganismType.PLANT:
                return True
            if attacker.get_strength() >= self.get_strength():
                from event.human.human_ability_prevented_attack_event import HumanAbilityPreventedAttackEvent
                self.get_world().dispatch_world_event(
                    HumanAbilityPreventedAttackEvent(self, attacker)
                )
                free_positions = self.get_world().get_free_neighbours(self.get_position(), 1)
                if not free_positions:
                    attacker.move_to(attacker.get_last_position())
                else:
                    self.move_to(random.choice(free_positions))
                return True
        return False

    def activate_ability(self):
        if self.get_ability_cooldown() == 0 and not self.is_ability_active():
            self.ability_active = True
            self.ability_expiration_time = Human.ABILITY_EXPIRATION_TIME
            from event.human.human_ability_activated_event import HumanAbilityActivatedEvent
            self.get_world().dispatch_world_event(HumanAbilityActivatedEvent(self))
        elif self.is_ability_active():
            from event.human.human_ability_already_active_event import HumanAbilityAlreadyActiveEvent
            self.get_world().dispatch_world_event(HumanAbilityAlreadyActiveEvent(self))
        else:
            from event.human.human_ability_on_cooldown_event import HumanAbilityOnCooldownEvent
            self.get_world().dispatch_world_event(HumanAbilityOnCooldownEvent(self))

    def set_alive(self, alive):
        super().set_alive(alive)
        gm = self.get_world().get_game_manager()
        gm.set_player_alive(alive)
        gm.update_player_info_labels()

    def serialize(self):
        return f"{self.get_type()} {self.get_species()} {self.get_position().x} {self.get_position().y} " \
               f"{self.get_last_position().x} {self.get_last_position().y} {self.get_strength()} " \
               f"{self.get_initiative()} {self.get_age()} {self.get_breed_cooldown()} " \
               f"{self.is_ability_active()} {self.get_ability_expiration_time()} {self.get_ability_cooldown()}"

    @staticmethod
    def deserialize_human(data: str, world):
        parts = data.split()
        human = Human(Position(0, 0), world)
        human.set_position(Position(int(parts[2]), int(parts[3])))
        human.set_ability_active(parts[10] == "True")
        human.set_ability_expiration_time(int(parts[11]))
        human.set_ability_cooldown(int(parts[12]))
        return human

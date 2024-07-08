from utils.dice import roll_dice

class Character:
    def __init__(self, name, ac, hp, initiative_mod, attack_bonus, damage_dice, damage_bonus, speed):
        self.name = name
        self.ac = ac
        self.hp = hp
        self.max_hp = hp
        self.initiative_mod = initiative_mod
        self.attack_bonus = attack_bonus
        self.damage_dice = damage_dice
        self.damage_bonus = damage_bonus
        self.speed = speed
        self.position = (0, 0)
        self.initiative = 0
        self.reset_turn()

    def reset_turn(self):
        self.action_used = False
        self.bonus_action_used = False
        self.reaction_used = False
        self.movement_remaining = self.speed

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def roll_initiative(self):
        self.initiative = roll_dice(1, 20) + self.initiative_mod
        return self.initiative

    def move(self, distance):
        if distance <= self.movement_remaining:
            self.movement_remaining -= distance
            return f"{self.name} moves {distance} feet."
        else:
            return f"{self.name} can't move that far."

    def dash(self):
        self.movement_remaining += self.speed
        return f"{self.name} dashes, doubling their movement speed."
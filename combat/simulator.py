from combat.turn_manager import TurnManager
from actions.attack import perform_attack
from actions.move import perform_move
from actions.dash import perform_dash
from utils.map_generator import create_battle_map
import random
import pygame
import time

class CombatSimulator:
    def __init__(self, map_width=20, map_height=15, cell_size=30):
        self.characters = []
        self.turn_manager = None
        self.battle_map = create_battle_map(map_width, map_height, cell_size)

    def add_character(self, character):
        self.characters.append(character)

    def setup_combat(self):
        self.turn_manager = TurnManager(self.characters)
        self.turn_manager.roll_initiative()
        
        # Place characters on the map
        for character in self.characters:
            x, y = self.battle_map.get_random_valid_position()
            character.position = (x, y)

    def simulate_combat(self):
        self.setup_combat()
        print("Combat begins!")
        self.battle_map.draw_map(self.characters)
        
        running = True
        while running and len([c for c in self.characters if c.is_alive()]) > 1:
            current_character = self.turn_manager.next_turn()
            if not current_character.is_alive():
                continue

            targets = [c for c in self.characters if c.is_alive() and c != current_character]
            if not targets:
                break

            print(f"\nRound {self.turn_manager.round}, {current_character.name}'s turn:")
            
            # Movement
            move_distance = random.randint(0, min(current_character.movement_remaining, 5))
            self._perform_move(current_character, move_distance)

            # Action
            if not current_character.action_used:
                action_choice = random.choice(['attack', 'dash'])
                if action_choice == 'attack':
                    target = self._get_nearest_target(current_character, targets)
                    print(perform_attack(current_character, target))
                elif action_choice == 'dash':
                    print(perform_dash(current_character))
                current_character.action_used = True

            # Simplified Bonus Action and Reaction
            if not current_character.bonus_action_used:
                print(f"{current_character.name} uses a bonus action.")
                current_character.bonus_action_used = True

            if random.random() > 0.7 and not current_character.reaction_used:
                print(f"{current_character.name} uses their reaction.")
                current_character.reaction_used = True

            # Check for defeated characters
            for character in self.characters:
                if not character.is_alive() and character.hp > 0:
                    character.hp = 0
                    print(f"{character.name} has been defeated!")

            # Update the map
            self.battle_map.draw_map(self.characters)
            time.sleep(1)  # Pause to allow viewing of each turn
            running = self.battle_map.handle_events()

        winner = next((c for c in self.characters if c.is_alive()), None)
        if winner:
            print(f"\n{winner.name} wins the combat!")
        else:
            print("\nAll characters have been defeated. It's a draw!")

        # Keep the final map visible
        while running:
            running = self.battle_map.handle_events()

    def _perform_move(self, character, distance):
        for _ in range(distance):
            dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            new_x, new_y = character.position[0] + dx, character.position[1] + dy
            if self.battle_map.is_valid_position(new_x, new_y):
                character.position = (new_x, new_y)
                character.movement_remaining -= 1
            if character.movement_remaining == 0:
                break
        print(f"{character.name} moves to position {character.position}.")

    def _get_nearest_target(self, attacker, targets):
        return min(targets, key=lambda t: self._distance(attacker.position, t.position))

    def _distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
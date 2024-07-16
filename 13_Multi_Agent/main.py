import tkinter as tk
import logging
from dotenv import load_dotenv
import os
import json
import random
from chat_utils import chat_with_claude, ColoredFormatter
from dnd_tools import tools
from gui import DnDChatbotGUI
from character_data import characters
from prompts import SYSTEM_PROMPT, CHARACTER_INFO_PROMPT, INITIAL_USER_QUERY
from debug_console import DebugConsole

# Load environment variables
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Character:
    def __init__(self, name, char_data):
        self.name = name
        self.max_hp = char_data['hit_points']
        self.current_hp = self.max_hp
        self.armor_class = char_data['armor_class']
        self.attack_bonus = char_data['abilities']['STR']['modifier']
        self.damage_dice = char_data['actions'][0]['damage_dice']
        self.damage_bonus = char_data['actions'][0]['damage_bonus']

    def take_damage(self, damage):
        self.current_hp = max(0, self.current_hp - damage)

    def is_alive(self):
        return self.current_hp > 0

class CombatManager:
    def __init__(self, characters):
        self.characters = characters
        self.turn_count = 0

    def simulate_combat_turn(self, attacker, defender):
        self.turn_count += 1
        attack_roll = random.randint(1, 20) + attacker.attack_bonus
        if attack_roll >= defender.armor_class:
            damage = sum(random.randint(1, int(attacker.damage_dice.split('d')[1])) 
                         for _ in range(int(attacker.damage_dice.split('d')[0]))) + attacker.damage_bonus
            defender.take_damage(damage)
            return f"{attacker.name} hits {defender.name} for {damage} damage. {defender.name}'s HP: {defender.current_hp}/{defender.max_hp}"
        else:
            return f"{attacker.name} misses {defender.name}."

    def is_combat_over(self):
        return not all(char.is_alive() for char in self.characters.values())

def process_tool_call(tool_name, tool_input, combat_manager):
    logger.debug(f"Processing tool call: {tool_name}")
    logger.debug(f"Tool input: {tool_input}")
    
    if tool_name == "simulate_combat_turn":
        attacker = combat_manager.characters[tool_input["attacker"]]
        defender = combat_manager.characters[tool_input["defender"]]
        result = combat_manager.simulate_combat_turn(attacker, defender)
        
        # Update the GUI with the tool input and output
        gui.update_tool_display(tool_name, json.dumps(tool_input, indent=2), result)
        
        gui.update_combat_info(combat_manager.turn_count, combat_manager.characters)
        return result
    else:
        return f"Unknown tool: {tool_name}"

def chat_function(conversation, combat_manager, model_name):
    def tool_call_wrapper(tool_name, tool_input):
        return process_tool_call(tool_name, tool_input, combat_manager)
    
    response = chat_with_claude(conversation, ANTHROPIC_API_KEY, tools, tool_call_wrapper, model_name, SYSTEM_PROMPT)
    return response

def initialize_conversation(combat_manager):
    character_info = "Here are the available characters and their stats for the D&D combat simulation:\n\n"
    for char_name, char_data in combat_manager.characters.items():
        character_info += f"{char_name.capitalize()}:\n"
        character_info += json.dumps(vars(char_data), indent=2, default=str)
        character_info += "\n\n"
    
    character_info += CHARACTER_INFO_PROMPT

    initial_conversation = [
        {"role": "user", "content": INITIAL_USER_QUERY},
        {"role": "assistant", "content": character_info}
    ]

    return initial_conversation

def main():
    root = tk.Tk()
    
    # Create debug console
    debug_console = DebugConsole(root)
    logger.addHandler(debug_console)
    
    # Set up colored formatter for console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)
    
    # Initialize characters and combat manager
    combat_characters = {name: Character(name, data) for name, data in characters.items()}
    combat_manager = CombatManager(combat_characters)
    
    initial_conversation = initialize_conversation(combat_manager)
    
    global gui  # Make gui a global variable so it can be accessed in process_tool_call
    gui = DnDChatbotGUI(
        root,
        lambda conv, model: chat_function(initial_conversation + conv, combat_manager, model),
        lambda tool_name, tool_input: process_tool_call(tool_name, tool_input, combat_manager)
    )
    
    root.mainloop()

if __name__ == "__main__":
    main()
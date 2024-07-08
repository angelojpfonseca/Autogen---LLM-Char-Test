import tkinter as tk
import logging
from dotenv import load_dotenv
import os
import json
from chat_utils import chat_with_claude
from dnd_tools import tools, simulate_melee_attack, simulate_ranged_attack
from gui import DnDChatbotGUI
from character_data import characters

# Load environment variables
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='debug.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_tool_call(tool_name, tool_input):
    if tool_name == "simulate_melee_attack":
        return simulate_melee_attack(tool_input["attacker"], tool_input["defender"])
    elif tool_name == "simulate_ranged_attack":
        return simulate_ranged_attack(tool_input["attacker"], tool_input["defender"])
    else:
        return f"Unknown tool: {tool_name}"

def chat_function(conversation, process_tool_call, model_name):
    return chat_with_claude(conversation, ANTHROPIC_API_KEY, tools, process_tool_call, model_name)

def initialize_conversation():
    # Create an initial message that includes all character data
    character_info = "Here are the available characters and their stats for the D&D combat simulation:\n\n"
    for char_name, char_data in characters.items():
        character_info += f"{char_name.capitalize()}:\n"
        character_info += json.dumps(char_data.to_dict(), indent=2)
        character_info += "\n\n"
    
    character_info += ("You can use these characters in combat simulations. "
                       "When a user requests a combat simulation, use either the simulate_melee_attack "
                       "or simulate_ranged_attack tool with the appropriate character names as attacker and defender.")

    # Start with a user message asking about available characters
    initial_conversation = [
        {"role": "user", "content": "What characters are available for the D&D combat simulation?"},
        {"role": "assistant", "content": character_info}
    ]

    return initial_conversation

def main():
    root = tk.Tk()
    initial_conversation = initialize_conversation()
    
    gui = DnDChatbotGUI(
        root,
        lambda conv, ptc, model: chat_function(initial_conversation + conv, ptc, model),
        process_tool_call
    )
    
    root.mainloop()

if __name__ == "__main__":
    main()
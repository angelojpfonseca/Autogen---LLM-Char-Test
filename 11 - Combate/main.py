import tkinter as tk
import logging
from dotenv import load_dotenv
import os
import json
from chat_utils import chat_with_claude, ColoredFormatter
from dnd_tools import tools, simulate_melee_attack, simulate_ranged_attack
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

def process_tool_call(tool_name, tool_input):
    if tool_name == "simulate_melee_attack":
        output = simulate_melee_attack(tool_input["attacker"], tool_input["defender"])
    elif tool_name == "simulate_ranged_attack":
        output = simulate_ranged_attack(tool_input["attacker"], tool_input["defender"])
    else:
        output = f"Unknown tool: {tool_name}"
    
    # Update the tool display in the GUI
    gui.update_tool_display(tool_name, json.dumps(tool_input, indent=2), output)
    
    return output

def chat_function(conversation, process_tool_call, model_name):
    return chat_with_claude(conversation, ANTHROPIC_API_KEY, tools, process_tool_call, model_name, SYSTEM_PROMPT)

def initialize_conversation():
    character_info = "Here are the available characters and their stats for the D&D combat simulation:\n\n"
    for char_name, char_data in characters.items():
        character_info += f"{char_name.capitalize()}:\n"
        character_info += json.dumps(char_data.to_dict(), indent=2)
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
    
    initial_conversation = initialize_conversation()
    
    global gui  # Make gui a global variable so it can be accessed in process_tool_call
    gui = DnDChatbotGUI(
        root,
        lambda conv, ptc, model: chat_function(initial_conversation + conv, ptc, model),
        process_tool_call
    )
    
    root.mainloop()

if __name__ == "__main__":
    main()
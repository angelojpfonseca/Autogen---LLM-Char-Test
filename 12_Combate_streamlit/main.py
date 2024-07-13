import streamlit as st
import logging
import sys
from dotenv import load_dotenv
import os
import json
from chat_utils import chat_with_claude, ColoredFormatter
from dnd_tools import tools, simulate_melee_attack, simulate_ranged_attack
from gui import create_gui
from character_data import characters
from prompts import SYSTEM_PROMPT, CHARACTER_INFO_PROMPT, INITIAL_USER_QUERY

# Load environment variables
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add file handler
file_handler = logging.FileHandler('debug.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Add console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

def process_tool_call(tool_name, tool_input):
    logger.debug(f"Processing tool call: {tool_name}")
    logger.debug(f"Tool input: {tool_input}")
    
    if tool_name == "simulate_melee_attack":
        output = simulate_melee_attack(tool_input["attacker"], tool_input["defender"])
    elif tool_name == "simulate_ranged_attack":
        output = simulate_ranged_attack(tool_input["attacker"], tool_input["defender"])
    else:
        output = f"Unknown tool: {tool_name}"
    
    logger.debug(f"Tool output: {output}")
    
    # Update the tool display in the GUI
    st.session_state.gui.update_tool_display(tool_name, json.dumps(tool_input, indent=2), output)
    
    return output

def chat_function(conversation, process_tool_call, model_name):
    logger.debug(f"Calling chat function with model: {model_name}")
    try:
        response = chat_with_claude(conversation, ANTHROPIC_API_KEY, tools, process_tool_call, model_name, SYSTEM_PROMPT)
        logger.debug(f"Received response: {response[:100]}...")  # Log first 100 chars of response
        return response
    except Exception as e:
        logger.error(f"Error in chat function: {str(e)}")
        raise

def initialize_conversation():
    logger.debug("Initializing conversation")
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
    logger.info("Starting D&D Combat Simulator")
    
    initial_conversation = initialize_conversation()
    
    if 'gui' not in st.session_state:
        st.session_state.gui = create_gui(
            lambda conv, ptc, model: chat_function(initial_conversation + conv, ptc, model),
            process_tool_call
        )
    
    st.session_state.gui.display_greeting()

if __name__ == "__main__":
    main()
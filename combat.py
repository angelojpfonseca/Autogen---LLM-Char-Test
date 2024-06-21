import os
from dotenv import load_dotenv
import openai 
from autogen import ConversableAgent, UserProxyAgent, GroupChat, GroupChatManager 
import random
from typing import Annotated
import json

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Load system messages from files
dm_system_message_path = r'Combat_Prompt\dm.txt'
orc_system_message_path = r'Combat_Prompt\orc.txt'
goblin_system_message_path = r'Combat_Prompt\goblin.txt'
player_system_message_path = r'Combat_Prompt\player.txt'
llm_config_path = r'llm_config.json'

with open(llm_config_path, 'r') as file:
    llm_config = json.load(file)
with open(dm_system_message_path, 'r') as file:
    dm_system_message = file.read()
with open(orc_system_message_path, 'r') as file:
    orc_system_message = file.read()
with open(goblin_system_message_path, 'r') as file:
    goblin_system_message= file.read()
with open(player_system_message_path, 'r') as file:
    player_system_message= file.read()


llm_config['config_list'][0]['api_key'] = OPENAI_API_KEY



# Define the roll_d20 function
def roll_d20(modifier: int, caller: str) -> str:
    """Roll a d20 and add a modifier"""
    roll = random.randint(1, 20)
    total = roll + modifier
    return f"{caller} rolled: {roll} + {modifier} = {total}"

# Define the function map
function_map = {
    "roll_d20": roll_d20
}

# Create agents
dm = ConversableAgent(
    name="dm",
    system_message=dm_system_message,
    llm_config=llm_config,
    function_map=function_map,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"]
)

orc = ConversableAgent(
    name="Orc",
    system_message=orc_system_message,
    llm_config=llm_config,
    function_map=function_map,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"]
)

goblin = ConversableAgent(
    name="Goblin",
    system_message=goblin_system_message,
    llm_config=llm_config,
    function_map=function_map,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"]
)

player_proxy = UserProxyAgent(
    name="Player",
    system_message=player_system_message,
    code_execution_config=False,
)

# Register the roll_d20 function for each agent
dm.register_for_llm(name="roll_d20", description="Roll a d20 and add a modifier")(roll_d20)
orc.register_for_llm(name="roll_d20", description="Roll a d20 and add a modifier")(roll_d20)
goblin.register_for_llm(name="roll_d20", description="Roll a d20 and add a modifier")(roll_d20)

player_proxy = UserProxyAgent(
    name="Player",
    system_message=player_system_message,
    code_execution_config=False,
)

# Register the roll_d20 function for each agent
dm.register_for_llm(name="roll_d20", description="Roll a d20 and add a modifier")(roll_d20)
orc.register_for_llm(name="roll_d20", description="Roll a d20 and add a modifier")(roll_d20)
goblin.register_for_llm(name="roll_d20", description="Roll a d20 and add a modifier")(roll_d20)

# Set up the group chat
max_combat_rounds = 20
groupchat = GroupChat(
    agents=[dm, orc, goblin, player_proxy],
    messages=[],
    max_round=max_combat_rounds
)

manager = GroupChatManager(groupchat=groupchat)

# Start the chat
player_proxy.initiate_chat(
    manager,
    message="Begin the combat simulation between the Orc and the Goblin."
)
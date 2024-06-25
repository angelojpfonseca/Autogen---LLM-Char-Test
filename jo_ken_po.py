import os
from dotenv import load_dotenv
import openai 
from autogen import ConversableAgent, GroupChat, GroupChatManager


# Define the path to the system message file for agent1
manager_system_message_path = r'Prompt\manager.txt'
agent1_system_message_path = r'Prompt\agent1.txt'
agent2_system_message_path = r'Prompt\agent2.txt'


# Open the file and read its contents into a string variable
with open(manager_system_message_path, 'r') as file:
    manager_system_message = file.read()

with open(agent1_system_message_path, 'r') as file:
    agent1_system_message = file.read()

with open(agent2_system_message_path, 'r') as file:
    agent2_system_message = file.read()


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

llm_config = {
    "model": "gpt-4",
    "temperature": 0,
    "max_tokens": 256,
    "cache_seed": 51,
    "api_key": OPENAI_API_KEY
    }

manager= ConversableAgent (
    name="manager",
    system_message=manager_system_message,
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "Goodbye" in msg["content"]
   )



agent1 = ConversableAgent(
    name="Agent 1",
    system_message= agent1_system_message,
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "Goodbye" in msg["content"]
    )

agent2= ConversableAgent(
    name="Agent 2",
    system_message=agent2_system_message,
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "Goodbye" in msg["content"]
    )


agent1.register_nested_chats(
    trigger=agent2,
    chat_queue=[
        {
            "sender": manager,
            "recipient": agent1,
            "summary_method": "last_msg",
        }
    ],
)

agent2.register_nested_chats(
    trigger=agent1,
    chat_queue=[
        {
            "sender": manager,
            "recipient": agent2,
            "summary_method": "last_msg",
        }
    ],
)



chat_result = agent1.initiate_chat(
    agent2,
    message="Let's play Jo Ken Po! Your move.",
    max_turns=2,
)

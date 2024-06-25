import os
from dotenv import load_dotenv
import openai
from autogen import ConversableAgent, UserProxyAgent, GroupChatManager, GroupChat

# Define the path to the system message file for agent1
dm_system_message_path = r'D:\Git Hub\Autogen---Combat\Prompt\manager.txt'
agent1_system_message_path = r'D:\Git Hub\Autogen---Combat\Prompt\agent1.txt'
agent2_system_message_path = r'D:\Git Hub\Autogen---Combat\Prompt\agent2.txt'
chat_manager_system_message_path = r'D:\Git Hub\Autogen---Combat\Prompt\Chat_Manager.txt'

# Open the file and read its contents into a string variable
with open(dm_system_message_path, 'r') as file:
    manager_system_message = file.read()

with open(agent1_system_message_path, 'r') as file:
    agent1_system_message = file.read()

with open(agent2_system_message_path, 'r') as file:
    agent2_system_message = file.read()

with open(chat_manager_system_message_path, 'r') as file:
    chat_manager_system_message = file.read()

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

llm_config = {
    "model": "gpt-4",
    "temperature": 0,
    "max_tokens": 256,
    "cache_seed": 50,
    "api_key": OPENAI_API_KEY
    }

manager= ConversableAgent(
    name="manager",
    system_message=manager_system_message,
    llm_config=llm_config,
    human_input_mode="NEVER",
   )



agent1 = ConversableAgent(
    name="Agent 1",
    system_message= agent1_system_message,
    llm_config=llm_config,
    human_input_mode="NEVER",
    )

agent2= ConversableAgent(
    name="Agent 2",
    system_message=agent2_system_message,
    llm_config=llm_config,
    human_input_mode="NEVER",
    )





group_chat = GroupChat(
    agents=[manager, agent1, agent2],
    messages=[],
    max_round= 10,
)

group_chat_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={"config_list": [{"model": "gpt-4", "api_key": OPENAI_API_KEY}]},
    human_input_mode="ALWAYS",
    system_message=chat_manager_system_message
)

chat_result = group_chat_manager.initiate_chat(
    manager,
    message="""now you guys play Jo Ken Po!""",
    summary_method="reflection_with_llm",
)


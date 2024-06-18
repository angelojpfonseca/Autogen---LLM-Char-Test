import os
from dotenv import load_dotenv
import openai
from autogen import ConversableAgent, UserProxyAgent, GroupChatManager, GroupChat




load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

llm_config = {
    "model": "gpt-4",
    "temperature": 0,
    "max_tokens": 256,
    "cache_seed": 42,
    "api_key": OPENAI_API_KEY
    }

dm_combat = ConversableAgent(
    name="Dungeon_Master",
    system_message='DM_Prompt.txt',
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
        is_termination_msg=lambda msg: "terminate" in msg.get("content").lower(),

)



agent1 = ConversableAgent(
    name="Agent 1",
    system_message= 'agent1.txt',
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "terminate" in msg.get("content").lower(),
)

agent2= ConversableAgent(
    name="Agent 2",
    system_message='agent2.txt',
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "terminate" in msg.get("content").lower()
)





group_chat = GroupChat(
    agents=[dm_combat, agent1, agent2],
    messages=[],
    max_round= 10,
)

group_chat_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={"config_list": [{"model": "gpt-4", "api_key": OPENAI_API_KEY}]},
    human_input_mode="ALWAYS",
    system_message='Chat_Manager.txt'
)

chat_result = group_chat_manager.initiate_chat(
    dm_combat,
    message="""Welcome to the game! Keep the game going as you do""",
    summary_method="reflection_with_llm",
)


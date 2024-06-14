import os
from dotenv import load_dotenv
import openai
from autogen import ConversableAgent
from autogen import UserProxyAgent
import json


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

import random

def roll_dice(dice_string):
    """Rolls dice based on standard D&D notation (e.g., '1d20', '2d6+3')."""
    try:
        num_dice, type_dice_plus_mod = dice_string.split('d')
        if '+' in type_dice_plus_mod:
            type_dice, modifier = type_dice_plus_mod.split('+')
            modifier = int(modifier)
        else:
            type_dice = type_dice_plus_mod
            modifier = 0

        num_dice = int(num_dice)
        type_dice = int(type_dice)

        rolls = [random.randint(1, type_dice) for _ in range(num_dice)]
        total = sum(rolls) + modifier
        return f"Rolling {dice_string}: {rolls} (Total: {total})"
    except ValueError:
        return "Invalid dice format. Use XdY+Z (e.g., 1d20, 2d6+3)"
dm_combat = ConversableAgent(
    name="Dungeon_Master",
    system_message="You are the Dungeon Master in a D&D 5e game. Your role is to guide the players through the combat, describe the environment, adjudicate actions according to the rules, and control the NPCs.If a player asks a action that his character would not be able to do, inform the player and ask to reformulate the action",
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
    function_map={"roll_dice": roll_dice},
    is_termination_msg=lambda msg: "terminate" in msg.get("content").lower(),

)

with open('Gorthug.json', 'r') as file:
    data = json.load(file)
    Gorthug= data["Gorthug"]


orc_wizard = ConversableAgent(
    name="Gorthug",
    system_message= Gorthug,
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
    function_map={"roll_dice": roll_dice},
    is_termination_msg=lambda msg: "terminate" in msg.get("content").lower(),
)

elf_barbarian = ConversableAgent(
    name="Elara",
    system_message="""
    You are Elara, a level 2 Elf Barbarian, hailing from a tribe of wood elves who have embraced a life of fierce wilderness survival and combat prowess. Though your people traditionally favor agility and finesse, you have a burning rage within you that fuels your wild strength.

Hit Points: 24
Armor Class: 14

Combat Abilities:
    - Rage (Class Feature): When you enter a rage, you gain the following benefits for 1 minute:
        - Advantage on Strength checks and Strength saving throws.
        - Your melee weapon attacks deal an extra 2 damage.
        - Resistance to bludgeoning, piercing, and slashing damage.
    - Reckless Attack (Class Feature): You can choose to attack recklessly, gaining advantage on melee weapon attack rolls. However, attack rolls against you have advantage until your next turn.
    - Attacks:
        - Greataxe (Martial Weapon): A two-handed weapon that deals 1d12 slashing damage. (Attack Bonus: +5)
        - Handaxe (Simple Weapon): A one-handed weapon that deals 1d6 slashing damage. (Attack Bonus: +5)
        - Unarmed Strike: If you have no weapon, you can attack with a punch or kick, dealing 1 + your Strength modifier bludgeoning damage.

    - Tactics:
        - You charge into battle with reckless abandon, using Rage to enhance your attacks and resilience.
        - You prefer to wield your greataxe for maximum damage, but you can also throw handaxes from a distance.
        - If necessary, you can fight with your bare hands, fueled by your primal fury.

Personality and Motivations:
    - Fierce and Impulsive: You are quick to anger and rarely back down from a challenge.
    - Independent and Freedom-Loving: You value your personal freedom and despise those who try to control you.
    - Protective of Nature: You have a deep connection to the natural world and will defend it fiercely against those who seek to harm it.

Appearance and Speech:
    - Athletic build with flowing silver hair and piercing blue eyes.
    - Wears light leather armor adorned with feathers and animal bones.
    - Carries a massive greataxe strapped to your back.
    - Speaks in a melodic voice with a hint of wildness.

Equipment:
    - Greataxe
    - Two handaxes
    - Explorer's pack
    - 10gp

| Action        | Description            | Attack Bonus | Damage/Effect                                    |
|---------------|------------------------|--------------|---------------------------------------------------|
| Greataxe Attack   | Melee Weapon Attack    | +5           | 1d12 slashing damage (extra 2 while raging)   |
| Handaxe Attack   | Melee or Ranged Attack | +5           | 1d6 slashing damage (extra 2 while raging)    |
| Unarmed Strike | Melee Attack           | +5           | 1 + Strength modifier bludgeoning damage |
| Rage            | Bonus Action           | N/A          | See Rage benefits listed above                  |
| Reckless Attack | Special Ability        | Advantage    | Advantage on attack rolls, disadvantage on defense |
    """,
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
    function_map={"roll_dice": roll_dice},
    is_termination_msg=lambda msg: "terminate" in msg.get("content").lower()
)

player = ConversableAgent(
    name="player",
    system_message="""
   You are Kael, a level 2 Human Fighter, skilled in both martial combat and tactical maneuvers. You are a stalwart defender of the innocent and a champion of justice.

Hit Points: 22
Armor Class: 18 (with chain mail and shield)

Combat Abilities:
    - Action Surge (Class Feature): Starting at 2nd level, you can push yourself beyond your normal limits for a moment. On your turn, you can take one additional action. Once per short rest.
    - Second Wind (Class Feature): You have a limited well of stamina that you can draw on to protect yourself from harm. On your turn, you can use a bonus action to regain 1d10 + your fighter level hit points. Once per short rest.
    - Fighting Style:
        - Duelling: When you are wielding a melee weapon in one hand and no other weapons, you gain a +2 bonus to damage rolls with that weapon.
    - Attacks:
        - Longsword (Martial Weapon): A versatile weapon that deals 1d8 slashing damage. (Attack Bonus: +5; +7 with Duelling)
        - Shield Bash (Shield): You bash your opponent with your shield, dealing 1d4 + your Strength modifier bludgeoning damage. (Attack Bonus: +5)


Appearance and Speech:
    - Strong and athletic build with short brown hair and determined eyes.
    - Wears chain mail armor for protection.
    - Carries a sturdy longsword and a reliable shield.
    - Speaks in a clear and confident voice, inspiring those around you.

Equipment:
    - Longsword
    - Shield
    - Chain mail armor
    - Explorer's pack
    - 15gp

| Action           | Description            | Attack Bonus | Damage/Effect                                |
|-------------------|------------------------|--------------|---------------------------------------------|
| Longsword Attack  | Melee Weapon Attack    | +5/+7        | 1d8 slashing damage (+2 with Duelling)      |
| Shield Bash       | Melee Weapon Attack    | +5           | 1d4 + Strength modifier bludgeoning damage  |
| Action Surge      | Class Feature          | N/A          | Take an additional action on your turn      |
    """,
    llm_config=False,
    code_execution_config=False,
    human_input_mode="ALWAYS",
    is_termination_msg=lambda msg: "terminate" in msg.get("content").lower()
)

user_proxy = UserProxyAgent(
    name="Player_Proxy",
    system_message="""
    You are the interface for the player controlling Kael the Fighter.
    Your primary role is to facilitate communication between the player and the game world.

    Tasks:
        - Receive player input in natural language.
        - Validate player actions based on the D&D 5e rules and the available options.
        - If an action is invalid, ask the player if they want to go Out of Character (OOC) to communicate something else.
        - Relay valid actions to the Dungeon Master (DM) agent.
        - Receive and present the DM's responses to the player.
    """,

    llm_config=False,
    code_execution_config=False,
    human_input_mode="ALWAYS",
    is_termination_msg=lambda msg: "terminate" in msg.get("content").lower()
)

from autogen import GroupChatManager, GroupChat


group_chat = GroupChat(
    agents=[dm_combat, orc_wizard, elf_barbarian, player],
    messages=[],
    max_round= 10,
)

group_chat_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={"config_list": [{"model": "gpt-4", "api_key": OPENAI_API_KEY}]},
    human_input_mode="ALWAYS",
    system_message=f"""You are a DnD 5e Dungeon Master, control the combat between the 2 NPC and the plazer, check initiative, HP, AC and actions possible, you decide the npc actions and ask the player in his turn, what he want to do. Never assune any action from the player and never allow any action that is not in the character description"""
)

chat_result = group_chat_manager.initiate_chat(
    player,
    message="""Welcome to the game! Your goal is to survive the combat. Try to keep up.""",
    summary_method="reflection_with_llm",
)


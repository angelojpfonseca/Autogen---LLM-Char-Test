# agents.py
import os
import anthropic
import json
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def call_api(prompt, max_tokens=300):
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=max_tokens,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content

class DM:
    def __init__(self):
        self.conversation_history = []

    def narrate(self, text):
        self.conversation_history.append(f"DM: {text}")
        print(f"DM: {text}")

    def request_action(self, action, **kwargs):
        prompt = f"You are the Dungeon Master in a D&D 5e combat. Please {action} with the following information:\n"
        prompt += json.dumps(kwargs, indent=2)

        response = call_api(prompt)
        return json.loads(response)

class NPC:
    def __init__(self, name, ac, hp, attack_bonus, damage_dice):
        self.name = name
        self.ac = ac
        self.hp = hp
        self.attack_bonus = attack_bonus
        self.damage_dice = damage_dice
        self.conversation_history = []

    def act(self, action, **kwargs):
        prompt = f"You are {self.name}, a character in a D&D 5e combat. Please {action} with the following information:\n"
        prompt += json.dumps(kwargs, indent=2)

        response = call_api(prompt)
        action_result = json.loads(response)
        self.conversation_history.append(f"{self.name}: {action_result['description']}")
        return action_result
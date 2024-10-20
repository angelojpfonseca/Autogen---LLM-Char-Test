import random
import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def simulate_attack_roll(attack_bonus, weapon_damage):
    d20_roll = random.randint(1, 20)
    total_attack = d20_roll + attack_bonus
    
    # Parse weapon damage (assuming format like "1d8")
    damage_dice, damage_sides = map(int, weapon_damage.split('d'))
    damage_roll = sum(random.randint(1, damage_sides) for _ in range(damage_dice))
    
    total_damage = damage_roll  # Damage doesn't include attack bonus
    
    return {
        "d20_roll": d20_roll,
        "total_attack": total_attack,
        "damage_roll": damage_roll,
        "total_damage": total_damage
    }

# Define the tool
tools = [
    {
        "name": "attack_roll_simulator",
        "description": "Simulates a D&D 5e attack roll, including damage.",
        "input_schema": {
            "type": "object",
            "properties": {
                "attack_bonus": {
                    "type": "integer",
                    "description": "The attack bonus to add to the d20 roll."
                },
                "weapon_damage": {
                    "type": "string",
                    "description": "The weapon damage dice (e.g., '1d8' for a longsword)."
                }
            },
            "required": ["attack_bonus", "weapon_damage"]
        }
    }
]

def process_tool_call(tool_name, tool_input):
    if tool_name == "attack_roll_simulator":
        params = json.loads(tool_input)
        return simulate_attack_roll(params["attack_bonus"], params["weapon_damage"])

def chat_with_claude(messages):
    if not ANTHROPIC_API_KEY:
        print("Error: ANTHROPIC_API_KEY not found in .env file")
        return None

    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    MODEL_NAME = "claude-3-opus-20240229"

    try:
        message = client.messages.create(
            model=MODEL_NAME,
            system="You have access to tools, but only use them when necessary. If a tool is not required, respond as normal",
            max_tokens=4096,
            messages=messages,
            tools=tools,
        )

        if message.stop_reason == "tool_calls":
            tool_call = message.content[-1].tool_calls[0]
            tool_name = tool_call.name
            tool_input = tool_call.arguments

            print(f"\nTool Used: {tool_name}")
            print(f"Tool Input: {tool_input}")
             
            try:
              tool_result = process_tool_call(tool_name, tool_input)
              print(f"Tool Result: {tool_result}")
            except Exception as e:
                print(f"An error occurred: {str(e)}")

            response = client.messages.create(
                model=MODEL_NAME,
                max_tokens=4096,
                messages=messages + [
                    {"role": "assistant", "content": str(message.content)},
                    {"role": "tool", "content": str(tool_result)},
                ],
            )
        else:
            response = message

        return response.content[0].text if response.content else "No response generated."

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def main():
    conversation = []
    print("Welcome to the D&D 5e Attack Roll Simulator Chatbot!")
    print("You can ask about simulating attack rolls or discuss D&D topics.")
    print("Type 'exit' to end the conversation.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Thank you for using the D&D 5e Attack Roll Simulator Chatbot. Goodbye!")
            break

        conversation.append({"role": "user", "content": user_input})
        response = chat_with_claude(conversation)

        if response:
            print(f"\nClaude: {response}")
            conversation.append({"role": "assistant", "content": response})
        else:
            print("\nClaude: I'm sorry, I encountered an error. Please try again.")

if __name__ == "__main__":
    main()
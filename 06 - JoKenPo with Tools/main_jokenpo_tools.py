import os
from dotenv import load_dotenv
import anthropic
from jokenpo_tools import tools, process_tool_call

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv('ANTHROPIC_API_KEY')

if not api_key:
    raise ValueError("No API key found. Please set the ANTHROPIC_API_KEY in your .env file.")

# Create the Anthropic client with the API key
client = anthropic.Anthropic(api_key=api_key)

def chatbot_interaction(user_message):
    print(f"\n{'='*50}\nUser Message: {user_message}\n{'='*50}")

    messages = [
        {"role": "user", "content": user_message}
    ]

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        tools=tools,
        messages=messages
    )

    print(f"\nInitial Response:")
    print(f"Stop Reason: {message.stop_reason}")
    print(f"Content: {message.content}")

    if message.stop_reason == "tool_calls":
        for tool_call in message.content[0].tool_calls:
            tool_name = tool_call.function.name
            tool_input = tool_call.function.arguments

            print(f"\nTool Used: {tool_name}")
            print(f"Tool Input: {tool_input}")

            tool_result = process_tool_call(tool_name, tool_input)

            print(f"Tool Result: {tool_result}")

            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": message.content},
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": str(tool_result),
                    },
                ],
                tools=tools,
            )
    else:
        response = message

    final_response = response.content[0].text if response.content else "No response generated."
    print(f"\nFinal Response: {final_response}")

    return final_response

def main():
    player1_score = 0
    player2_score = 0
    rounds_played = 0

    while max(player1_score, player2_score) < 2 and rounds_played < 3:
        rounds_played += 1
        print(f"\n--- Round {rounds_played} ---")
        
        user_message = f"""
        It's round {rounds_played} of our Jo Ken Po game. The current score is:
        Player 1: {player1_score}
        Player 2: {player2_score}
        
        Please make moves for both players, play the round, and update the game state.
        Don't forget to add some fun commentary!
        """
        
        response = chatbot_interaction(user_message)
        
        # Here you would parse the response to update scores
        # For simplicity, let's just increment a random player's score
        import random
        if random.choice([True, False]):
            player1_score += 1
        else:
            player2_score += 1

    winner = "Player 1" if player1_score > player2_score else "Player 2"
    print(f"\nGame over! {winner} wins!")

if __name__ == "__main__":
    main()
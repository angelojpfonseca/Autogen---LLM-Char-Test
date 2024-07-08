import logging
from anthropic import Anthropic
from anthropic.types import ToolUseBlock

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def chat_with_claude(messages, api_key, tools, process_tool_call, model_name):
    if not api_key:
        logger.error("ANTHROPIC_API_KEY not found in .env file")
        return None

    client = Anthropic(api_key=api_key)

    try:
        message = client.messages.create(
            model=model_name,
            system="You are a Dungeon Master simulating D&D 5e combat. You have access to tools for simulating melee and ranged attacks. Use these tools when a combat simulation is requested. Provide a narrative description of the combat along with the tool results. If a tool is not required, respond as normal.",
            max_tokens=4096,
            messages=messages,
            tools=tools,
        )

        logger.debug(f"Initial response: {message.content}")

        # Check if the message content indicates tool use
        tool_use_block = next((content for content in message.content if isinstance(content, ToolUseBlock)), None)

        if tool_use_block:
            tool_name = tool_use_block.name
            tool_input = tool_use_block.input

            logger.debug(f"Tool Used: {tool_name}")
            logger.debug(f"Tool Input: {tool_input}")

            # Call the tool
            tool_result = process_tool_call(tool_name, tool_input)
            logger.debug(f"Tool Result: {tool_result}")

            # Create a new message with the tool result incorporated into the assistant's response
            tool_result_message = f"Combat Simulation Results:\n\n{tool_result}\n\nBased on these results, here's what happened:"
            response = client.messages.create(
                model=model_name,
                max_tokens=4096,
                messages=messages + [
                    {"role": "assistant", "content": tool_result_message},
                ],
            )
            return response.content[0].text if response.content else "No response generated."
        else:
            return message.content[0].text if message.content else "No response generated."

    except Exception as e:
        logger.exception(f"An error occurred: {str(e)}")
        return None
import logging
from anthropic import Anthropic
from anthropic.types import ToolUseBlock

logger = logging.getLogger(__name__)

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',  # Blue
        'INFO': '\033[92m',   # Green
        'WARNING': '\033[93m',# Yellow
        'ERROR': '\033[91m',  # Red
        'CRITICAL': '\033[95m',# Magenta
        'RESET': '\033[0m'    # Reset color
    }

    def format(self, record):
        log_message = super().format(record)
        return f"{self.COLORS.get(record.levelname, self.COLORS['RESET'])}{log_message}{self.COLORS['RESET']}"

def chat_with_claude(conversation, api_key, tools, process_tool_call, model_name, system_prompt):
    client = Anthropic(api_key=api_key)

    try:
        message = client.messages.create(
            model=model_name,
            system=system_prompt,
            max_tokens=4096,
            messages=conversation,
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
            tool_result_message = f"Based on the combat simulation, here are the results: {tool_result}"
            response = client.messages.create(
                model=model_name,
                max_tokens=4096,
                system=system_prompt,
                messages=conversation + [
                    {"role": "assistant", "content": tool_result_message},
                ],
            )
            return response.content[0].text if response.content else "No response generated."
        else:
            return message.content[0].text if message.content else "No response generated."

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return None
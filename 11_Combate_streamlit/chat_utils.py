import logging
from anthropic import Anthropic
from anthropic.types import ToolUseBlock, TextBlock
import json
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Set up logging
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        log_message = super().format(record)
        return f"{self.COLORS.get(record.levelname, '')}{log_message}{Style.RESET_ALL}"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def content_to_dict(obj):
    if isinstance(obj, TextBlock):
        return {"type": "text", "text": obj.text}
    elif isinstance(obj, ToolUseBlock):
        return {
            "type": "tool_use",
            "name": obj.name,
            "input": obj.input
        }
    elif isinstance(obj, list):
        return [content_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: content_to_dict(v) for k, v in obj.items()}
    else:
        return str(obj)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        return content_to_dict(obj)

def pretty_print_json(data):
    return json.dumps(data, indent=2, cls=CustomJSONEncoder)

def chat_with_claude(messages, api_key, tools, process_tool_call, model_name, system_prompt):
    if not api_key:
        logger.error("ANTHROPIC_API_KEY not found in .env file")
        return None

    client = Anthropic(api_key=api_key)

    try:
        logger.debug(f"{Fore.MAGENTA}Sending request to model: {model_name}")
        logger.debug(f"{Fore.MAGENTA}System prompt: {system_prompt}")
        logger.debug(f"{Fore.MAGENTA}Messages:")
        for msg in messages:
            logger.debug(f"{Fore.BLUE}  Role: {msg['role']}")
            logger.debug(f"{Fore.GREEN}  Content: {msg['content'][:100]}...")  # Truncate long messages

        message = client.messages.create(
            model=model_name,
            system=system_prompt,
            max_tokens=4096,
            messages=messages,
            tools=tools,
        )

        logger.debug(f"{Fore.YELLOW}Received response from Claude:")
        logger.debug(f"{Fore.YELLOW}{pretty_print_json(message.content)}")

        # Check if the message content indicates tool use
        tool_use_block = next((content for content in message.content if isinstance(content, ToolUseBlock)), None)

        if tool_use_block:
            tool_name = tool_use_block.name
            tool_input = tool_use_block.input

            logger.debug(f"{Fore.CYAN}Tool Used: {tool_name}")
            logger.debug(f"{Fore.CYAN}Tool Input: {pretty_print_json(tool_input)}")

            # Call the tool
            tool_result = process_tool_call(tool_name, tool_input)
            logger.debug(f"{Fore.CYAN}Tool Result: {pretty_print_json(tool_result)}")

            # Create a new message with the tool result incorporated into the assistant's response
            tool_result_message = f"Combat Simulation Results:\n\n{tool_result}\n\nBased on these results, here's what happened:"
            logger.debug(f"{Fore.MAGENTA}Sending follow-up message with tool results")
            response = client.messages.create(
                model=model_name,
                system=system_prompt,
                max_tokens=4096,
                messages=messages + [
                    {"role": "assistant", "content": tool_result_message},
                ],
            )
            logger.debug(f"{Fore.YELLOW}Received follow-up response from Claude:")
            logger.debug(f"{Fore.YELLOW}{pretty_print_json(response.content)}")
            return response.content[0].text if response.content else "No response generated."
        else:
            return message.content[0].text if message.content else "No response generated."

    except Exception as e:
        logger.exception(f"{Fore.RED}An error occurred: {str(e)}")
        return None
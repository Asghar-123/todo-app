import os
from dotenv import load_dotenv
import yaml
from openai import OpenAI
from pydantic import BaseModel
from typing import Dict, Type
import logging # Import logging module

logger = logging.getLogger(__name__) # Create a logger instance

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_ENDPOINT_URL = os.getenv("GEMINI_API_ENDPOINT_URL")

if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY environment variable is not set.")
    raise ValueError("GEMINI_API_KEY environment variable is not set.")
if not GEMINI_API_ENDPOINT_URL:
    logger.error("GEMINI_API_ENDPOINT_URL environment variable is not set.")
    raise ValueError("GEMINI_API_ENDPOINT_URL environment variable is not set.")

# Initialize OpenAI client to point to Gemini API
client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url=GEMINI_API_ENDPOINT_URL,
)

# --- Tool Loading Logic ---
# This would typically be part of an MCP SDK or a custom tool manager
def load_tool_from_config(tool_config: Dict) -> Type[BaseModel]:
    """
    Loads a Pydantic tool model from a configuration dictionary.
    Assumes the schema path is in the format 'module.sub_module:ClassName'.
    """
    schema_path = tool_config["schema"]
    module_path, class_name = schema_path.split(":")
    
    # Dynamically import the module
    module = __import__(module_path, fromlist=[class_name])
    
    # Get the class from the module
    tool_class = getattr(module, class_name)
    
    if not issubclass(tool_class, BaseModel):
        raise TypeError(f"Tool schema '{class_name}' must be a Pydantic BaseModel.")
        
    return tool_class

def load_tools_from_yaml(config_path: str) -> Dict[str, Type[BaseModel]]:
    """Loads tool definitions from a YAML file."""
    logger.info(f"Loading tools from {config_path}")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    loaded_tools = {}
    if 'tools' in config:
        for tool_def in config['tools']:
            name = tool_def['name']
            description = tool_def.get('description', '')
            schema_model = load_tool_from_config(tool_def)
            
            # OpenAI requires a specific tool format
            loaded_tools[name] = {
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": schema_model.model_json_schema()
                },
                "pydantic_model": schema_model # Store model for execution
            }
            logger.info(f"Loaded tool: {name}")
    return loaded_tools

# Load tools from tools.yaml
TOOLS_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/tools.yaml")
available_tools = load_tools_from_yaml(TOOLS_CONFIG_PATH)

# Convert to OpenAI format for the agent
openai_tools = [tool_data for tool_name, tool_data in available_tools.items() if "function" in tool_data]
logger.info(f"Available tools for AI agent: {[tool['function']['name'] for tool in openai_tools]}")

async def process_message(user_message: str) -> str:
    """
    Processes a user message using the Gemini API (via OpenAI SDK) and available tools.
    """
    logger.info(f"Received user message: '{user_message}'")
    messages = [{"role": "user", "content": user_message}]

    # Step 1: Send user message to Gemini and get tool calls
    response = client.chat.completions.create(
        model="gemini-1.5-pro-latest", # Use a Gemini model name
        messages=messages,
        tools=openai_tools,
        tool_choice="auto", # Allow Gemini to decide if it needs a tool
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    logger.info(f"AI Model response received. Tool calls: {tool_calls}")

    # Step 2: Check if Gemini wanted to call a tool
    if tool_calls:
        logger.info(f"Tool calls detected: {len(tool_calls)}")
        tool_outputs = []
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args_str = tool_call.function.arguments
            logger.info(f"Executing tool: {function_name} with arguments: {function_args_str}")
            
            if function_name in available_tools:
                tool_model = available_tools[function_name]["pydantic_model"]
                try:
                    # Parse arguments using Pydantic model
                    parsed_args = tool_model.model_validate_json(function_args_str)
                    
                    # Use the run method defined in the tool's Pydantic model
                    tool_result = parsed_args.run()
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": tool_result
                    })
                    logger.info(f"Tool {function_name} executed successfully. Result: {tool_result}")
                    
                except Exception as e:
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": f"Error executing tool {function_name}: {e}"
                    })
                    logger.error(f"Error executing tool {function_name}: {e}")

        messages.append(response_message) # Extend conversation with assistant's reply
        for output in tool_outputs:
            messages.append(
                {
                    "tool_call_id": output["tool_call_id"],
                    "role": "tool",
                    "name": function_name,
                    "content": output["output"],
                }
            )
        
        # Step 3: Send back to Gemini with tool outputs to get a final response
        final_response = client.chat.completions.create(
            model="gemini-1.5-pro-latest",
            messages=messages,
        )
        logger.info(f"Final AI response after tool execution: {final_response.choices[0].message.content}")
        return final_response.choices[0].message.content
    else:
        logger.info(f"No tool calls. Returning direct AI response: {response_message.content}")
        return response_message.content

if __name__ == "__main__":
    import asyncio
    logging.basicConfig(level=logging.INFO) # Configure basic logging for standalone execution

    async def main():
        logger.info("Agent ready. Type your messages. Type 'exit' to quit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                break
            
            response = await process_message(user_input)
            logger.info(f"Bot: {response}")

    asyncio.run(main())

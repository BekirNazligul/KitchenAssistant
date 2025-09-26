import logging
from datetime import datetime

from bedrock_agentcore import BedrockAgentCoreApp
from bedrock_agentcore.memory import MemoryClient
from bedrock_agentcore.memory.constants import StrategyType
from botocore.exceptions import ClientError
from strands import Agent
from strands_tools.agent_core_memory import AgentCoreMemoryToolProvider

from prompt import KITCHEN_ASSISTANT_PROMPT

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("culinary-memory")

app = BedrockAgentCoreApp()
client = MemoryClient(region_name="us-west-2")
memory_name = "CulinaryAssistant"

actor_id = f"actor-1"
session_id = f"actor-session-1"
namespace = f"user/{actor_id}/preferences"

try:
    print("Creating Long-Term Memory...")

    # We use a more descriptive name for our long-term memory resource
    memory_name = memory_name

    # Create memory with user preference strategy
    memory = client.create_memory_and_wait(
        name=memory_name,
        description="Culinary Assistant Agent with long term memory",
        strategies=[{
                    StrategyType.USER_PREFERENCE.value: {
                        "name": "UserPreferences",
                        "description": "Captures user preferences",
                        "namespaces": ["user/{actorId}/preferences"]
                    }
                }],
        event_expiry_days=7,
        max_wait=300,
        poll_interval=10
    )

    memory_id = memory['id']

except ClientError as e:
    if e.response['Error']['Code'] == 'ValidationException' and "already exists" in str(e):
        # If memory already exists, retrieve its ID
        memories = client.list_memories()
        memory_id = next((m['id'] for m in memories if m['id'].startswith(memory_name)), None)
        logger.info(f"Memory already exists. Using existing memory ID: {memory_id}")
except Exception as e:
    # Handle any errors during memory creation
    logger.info(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    # Cleanup on error - delete the memory if it was partially created
    if memory_id:
        try:
            client.delete_memory_and_wait(memory_id=memory_id)
            logger.info(f"Cleaned up memory: {memory_id}")
        except Exception as cleanup_error:
            logger.info(f"Failed to clean up memory: {cleanup_error}")

strands_provider = AgentCoreMemoryToolProvider(
    memory_id=memory_id,
    actor_id=actor_id,
    session_id=session_id,
    namespace=namespace
)

agent = Agent(model="anthropic.claude-3-5-sonnet-20240620-v1:0", system_prompt=KITCHEN_ASSISTANT_PROMPT, tools=strands_provider.tools)

@app.entrypoint
def invoke(payload):
    """Your AI agent function"""
    user_message = payload.get("prompt", "Hello! How can I help you today?")
    result = agent(user_message)
    return {"result": result.message}

if __name__ == "__main__":
    app.run(3000)
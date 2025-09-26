from bedrock_agentcore import BedrockAgentCoreApp
from strands.models import BedrockModel
from strands import Agent, tool

from prompt import KITCHEN_ASSISTANT_PROMPT

app = BedrockAgentCoreApp()

model = BedrockModel(
    model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
)

@tool
def look_into_fridge() -> dict:
    """Returns the contents of the fridge."""
    return {
        "milk": "1 liter",
        "eggs": "12",
        "butter": "200 grams",
        "cheese": "500 grams",
        "vegetables": ["carrots", "broccoli", "spinach"]
    }


# Initialize the agent with the model, system prompt, and tool
agent = Agent(
    model=model,
    system_prompt=KITCHEN_ASSISTANT_PROMPT,
    tools=[look_into_fridge]
)

@app.entrypoint
def invoke(payload):
    """Your AI agent function"""
    user_message = payload.get("prompt")
    print("User message:", user_message)
    result = agent(user_message)
    return {"result": response.message['content'][0]['text']}

if __name__ == "__main__":
    app.run()
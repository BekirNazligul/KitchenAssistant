from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

from prompt import KITCHEN_ASSISTANT_PROMPT

app = BedrockAgentCoreApp()
agent = Agent(model="anthropic.claude-3-5-sonnet-20240620-v1:0", system_prompt=KITCHEN_ASSISTANT_PROMPT)

@app.entrypoint
def invoke(payload):
    """Your AI agent function"""
    user_message = payload.get("prompt", "Hello! How can I help you today?")
    result = agent(user_message)
    return {"result": result.message}

if __name__ == "__main__":
    app.run()
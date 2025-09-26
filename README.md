# Kitchen Assistant

Welcome to the Kitchen Assistant project, developed during the AWS Bedrock AgentCore and Strands SDK Hackathon by amazing engineers:

- Bekir Nazligul
- Jihan Xu
- Max Hopei
 
This project leverages the power of AWS Bedrock AgentCore and Strands SDK to create an intelligent culinary assistant capable of interacting with users to suggest recipes based on available ingredients and user preferences.

## Project Overview

The Kitchen Assistant is designed to act as a virtual chef, helping users find recipes based on what they have in their fridge and their culinary preferences. It uses AWS Bedrock AgentCore for memory management and Strands SDK for agent functionalities.

## Features

- **Interactive Recipe Suggestions**: The assistant interacts with users to determine their preferences and available ingredients, suggesting recipes accordingly.
- **Memory Management**: Utilizes AWS Bedrock AgentCore to remember user preferences for future interactions.
- **It looks into your fridge!**: It has access to the Fridge MCP, isn't this particularly amazing?

## Components

### Main Application

- **`main.py`**: The core of the application, initializing the BedrockAgentCoreApp and setting up the agent with necessary tools and models. It includes a function to look into the fridge and retrieve its contents.

### Configuration

- **`conf.py`**: Configures the runtime environment for the agent, including setting up the execution role and ECR.

### Prompt

- **`prompt.py`**: Contains the system prompt for the agent, guiding its interactions with users to assist in recipe selection.

## Setup

### Prerequisites

- Python 3.11.9
- [uv](https://docs.astral.sh/uv/) package manager
- AWS credentials configured for access to Bedrock services

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd KitchenAssistant
   ```

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

### Running the Application

To start the Kitchen Assistant, run the following command:

```bash
uv run python app/agent/main.py
```

The application will start on port 3000, ready to assist you with your culinary needs.

## Dependencies

- `bedrock-agentcore==0.1.5`
- `bedrock-agentcore-starter-toolkit==0.1.14`
- `strands-agents==1.9.1`
- `strands-agents-tools>=0.2.8`

## Contributing

We welcome contributions to enhance the Kitchen Assistant. Please fork the repository and submit a pull request with your improvements.

## License

This project is licensed under the MIT License.

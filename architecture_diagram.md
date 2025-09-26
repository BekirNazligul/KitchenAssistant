# Kitchen Assistant - Architecture Diagram

## System Architecture

```mermaid
graph TB
    subgraph "User Interface Layer"
        UI[Terminal Chat UI<br/>app/ui/chat.py]
        API[HTTP API<br/>localhost:3000/invocations]
    end
    
    subgraph "AWS Bedrock AgentCore"
        AC[BedrockAgentCoreApp<br/>main.py]
        MC[MemoryClient<br/>Long-term Memory]
        KB[Knowledge Base<br/>ID: ANR2F7LXJS]
    end
    
    subgraph "Strands SDK"
        AGENT[Agent<br/>Claude 3.5 Sonnet]
        TOOLS[Tools]
        FRIDGE[look_into_fridge]
        RETRIEVE[retrieve]
        MEMORY_TOOL[AgentCoreMemoryToolProvider]
    end
    
    subgraph "AWS Services"
        BEDROCK[AWS Bedrock<br/>Claude 3.5 Sonnet]
        MEMORY_STORE[Memory Store<br/>User Preferences]
    end
    
    subgraph "External Tools"
        MCP[MCP Tools<br/>Fridge Integration]
    end
    
    %% User Interactions
    UI -->|POST Request| API
    API -->|JSON Payload| AC
    
    %% AgentCore Processing
    AC -->|Initialize| AGENT
    AC -->|Memory Management| MC
    MC -->|Store/Retrieve| MEMORY_STORE
    
    %% Agent Processing
    AGENT -->|System Prompt| AC
    AGENT -->|Tool Calls| TOOLS
    TOOLS --> FRIDGE
    TOOLS --> RETRIEVE
    TOOLS --> MEMORY_TOOL
    
    %% External Integrations
    FRIDGE -->|Fridge Contents| MCP
    RETRIEVE -->|Knowledge Queries| KB
    MEMORY_TOOL -->|User Preferences| MC
    
    %% AI Model
    AGENT -->|AI Processing| BEDROCK
    
    %% Response Flow
    BEDROCK -->|AI Response| AGENT
    AGENT -->|Formatted Response| AC
    AC -->|JSON Response| API
    API -->|Chat Display| UI
    
    %% Styling
    classDef aws fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef strands fill:#4A90E2,stroke:#2E5BBA,stroke-width:2px,color:#fff
    classDef ui fill:#28A745,stroke:#1E7E34,stroke-width:2px,color:#fff
    classDef tools fill:#6F42C1,stroke:#5A2D91,stroke-width:2px,color:#fff
    
    class AC,MC,KB,BEDROCK,MEMORY_STORE aws
    class AGENT,TOOLS,FRIDGE,RETRIEVE,MEMORY_TOOL strands
    class UI,API ui
    class MCP tools
```

## Data Flow Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Chat UI
    participant API as Agent API
    participant AC as AgentCore
    participant AG as Agent
    participant B as Bedrock
    participant M as Memory
    participant K as Knowledge Base
    participant F as Fridge Tool
    
    U->>UI: "What can I cook with eggs?"
    UI->>API: POST /invocations
    Note over UI,API: {"prompt": "What can I cook with eggs?"}
    
    API->>AC: invoke(payload)
    AC->>AG: Process with tools
    
    AG->>F: look_into_fridge()
    F-->>AG: Fridge contents
    
    AG->>K: retrieve(recipe query)
    K-->>AG: Recipe suggestions
    
    AG->>M: Check user preferences
    M-->>AG: User preferences
    
    AG->>B: Generate response
    B-->>AG: AI response
    
    AG->>M: Save preferences
    M-->>AG: Confirmation
    
    AG-->>AC: Formatted response
    AC-->>API: {"result": "response"}
    API-->>UI: JSON response
    UI-->>U: "👨‍🍳 Chef: You can make..."
```

## Component Overview

```mermaid
graph LR
    subgraph "Frontend"
        A[Terminal Chat UI]
    end
    
    subgraph "Backend Services"
        B[Bedrock AgentCore]
        C[Strands Agent]
    end
    
    subgraph "AI & Memory"
        D[Claude 3.5 Sonnet]
        E[Long-term Memory]
        F[Knowledge Base]
    end
    
    subgraph "Tools & Integrations"
        G[Fridge MCP]
        H[Recipe Retrieval]
    end
    
    A --> B
    B --> C
    C --> D
    C --> E
    C --> F
    C --> G
    C --> H
    
    classDef frontend fill:#e1f5fe
    classDef backend fill:#f3e5f5
    classDef ai fill:#fff3e0
    classDef tools fill:#e8f5e8
    
    class A frontend
    class B,C backend
    class D,E,F ai
    class G,H tools
```

## Key Features Highlight

```mermaid
mindmap
  root((Kitchen Assistant))
    User Interface
      Terminal Chat
      HTTP API
      Real-time Interaction
    AI Capabilities
      Claude 3.5 Sonnet
      Recipe Suggestions
      Ingredient Analysis
      Step-by-step Instructions
    Memory System
      User Preferences
      Long-term Storage
      Context Awareness
    Tools & Integrations
      Fridge Contents
      Knowledge Base
      Recipe Database
    AWS Services
      Bedrock AgentCore
      Memory Store
      Knowledge Base
```

## Hackathon Highlights

- **AWS Bedrock AgentCore**: Core memory and agent management
- **Strands SDK**: Agent framework and tool integration
- **Real-time Chat**: Terminal-based user interface
- **Memory Persistence**: User preference learning
- **Tool Integration**: Fridge MCP and knowledge retrieval
- **Modern Architecture**: Microservices with clear separation of concerns

#!/usr/bin/env python3
"""
Terminal UI for Kitchen Assistant Agent
A simple chat interface that communicates with the Bedrock AgentCore agent.
"""

import requests
import json
import sys
from typing import Optional


class KitchenAssistantUI:
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.endpoint = f"{base_url}/invocations"
        
    def send_message(self, message: str) -> Optional[str]:
        """Send a message to the agent and return the response."""
        try:
            payload = {"prompt": message}
            response = requests.post(
                self.endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("result", "No response received")
            
        except requests.exceptions.ConnectionError:
            return "❌ Error: Could not connect to the agent. Make sure it's running on port 3000."
        except requests.exceptions.Timeout:
            return "❌ Error: Request timed out. The agent might be taking too long to respond."
        except requests.exceptions.HTTPError as e:
            return f"❌ Error: HTTP {e.response.status_code} - {e.response.text}"
        except json.JSONDecodeError:
            return "❌ Error: Invalid JSON response from agent."
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def print_welcome(self):
        """Print welcome message and instructions."""
        print("🍳" + "="*60 + "🍳")
        print("           Welcome to Kitchen Assistant Chat!")
        print("🍳" + "="*60 + "🍳")
        print()
        print("I'm your virtual chef! I can help you find recipes based on")
        print("what you have in your fridge and your preferences.")
        print()
        print("Commands:")
        print("  - Type your message and press Enter to chat")
        print("  - Type 'quit', 'exit', or 'bye' to end the conversation")
        print("  - Type 'help' to see this message again")
        print()
        print("Let's start cooking! 🥘")
        print("-" * 62)
        print()
    
    def print_help(self):
        """Print help message."""
        print("\n" + "="*60)
        print("KITCHEN ASSISTANT HELP")
        print("="*60)
        print("I can help you with:")
        print("• Finding recipes based on your available ingredients")
        print("• Suggesting dishes based on your preferences")
        print("• Providing step-by-step cooking instructions")
        print("• Remembering your food preferences for future chats")
        print()
        print("Try asking me things like:")
        print("• 'What can I cook with eggs and cheese?'")
        print("• 'I have chicken and vegetables, any suggestions?'")
        print("• 'I'm in the mood for something Italian'")
        print("• 'What's in my fridge?'")
        print("="*60)
        print()
    
    def format_response(self, response: str) -> str:
        """Format the agent's response for better readability."""
        # Add some basic formatting
        if response.startswith("❌"):
            return response
        
        # Add some visual separation
        formatted = f"👨‍🍳 Chef: {response}"
        return formatted
    
    def run(self):
        """Main chat loop."""
        self.print_welcome()
        
        while True:
            try:
                # Get user input
                user_input = input("👤 You: ").strip()
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👨‍🍳 Chef: Thanks for cooking with me! Have a great meal! 👋")
                    print("🍳" + "="*60 + "🍳")
                    break
                elif user_input.lower() == 'help':
                    self.print_help()
                    continue
                elif not user_input:
                    print("👨‍🍳 Chef: Please enter a message or type 'help' for assistance.")
                    continue
                
                # Send message to agent
                print("👨‍🍳 Chef: Thinking...")
                response = self.send_message(user_input)
                
                # Display response
                formatted_response = self.format_response(response)
                print(f"\n{formatted_response}\n")
                print("-" * 62)
                
            except KeyboardInterrupt:
                print("\n\n👨‍🍳 Chef: Thanks for cooking with me! Have a great meal! 👋")
                print("🍳" + "="*60 + "🍳")
                break
            except EOFError:
                print("\n\n👨‍🍳 Chef: Thanks for cooking with me! Have a great meal! 👋")
                print("🍳" + "="*60 + "🍳")
                break


def main():
    """Main entry point."""
    # Check if requests is available
    try:
        import requests
    except ImportError:
        print("❌ Error: 'requests' library is required but not installed.")
        print("Please install it with: uv add requests")
        sys.exit(1)
    
    # Create and run the UI
    ui = KitchenAssistantUI()
    ui.run()


if __name__ == "__main__":
    main()

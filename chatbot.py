import google.generativeai as genai
import os
import json
from datetime import datetime
import time

class GeminiChatbot:
    def __init__(self, api_key, temperature=0.7):
        """Initialize chatbot with API key and optional temperature setting"""
        self.api_key = api_key
        self.temperature = temperature
        self.setup_model()
        self.chat = None
        self.conversation_history = []
        
    def setup_model(self):
        """Configure and set up the Gemini model"""
        genai.configure(api_key=self.api_key)
        model_config = {
            "temperature": self.temperature,
            "top_p": 1,
            "top_k": 1,
        }
        self.model = genai.GenerativeModel('gemini-pro', generation_config=model_config)
        
    def start_new_chat(self):
        """Start a new chat session"""
        self.chat = self.model.start_chat(history=[])
        self.conversation_history = []
        
    def save_conversation(self, filename=None):
        """Save conversation history to a JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chat_history_{timestamp}.json"
            
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, indent=2)
        return filename
        
    def get_response(self, user_input, max_retries=3):
        """Get response from the model with retry mechanism"""
        if not self.chat:
            self.start_new_chat()
            
        for attempt in range(max_retries):
            try:
                response = self.chat.send_message(user_input)
                # Save to conversation history
                self.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "user": user_input,
                    "bot": response.text
                })
                return response.text
                
            except Exception as e:
                if attempt == max_retries - 1:  # Last attempt
                    return f"Error after {max_retries} attempts: {str(e)}"
                time.sleep(1)  # Wait before retrying
                
    def run_chat_loop(self):
        """Run the main chat loop"""
        print("Chatbot initialized! Available commands:")
        print("- 'quit': Exit the chat")
        print("- 'new': Start a new chat session")
        print("- 'save': Save conversation history")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                # Handle special commands
                if user_input.lower() == 'quit':
                    print("Saving conversation and exiting...")
                    self.save_conversation()
                    print("Goodbye!")
                    break
                    
                elif user_input.lower() == 'new':
                    self.start_new_chat()
                    print("Started a new chat session!")
                    continue
                    
                elif user_input.lower() == 'save':
                    filename = self.save_conversation()
                    print(f"Conversation saved to {filename}")
                    continue
                    
                if user_input:
                    response = self.get_response(user_input)
                    print("\nBot:", response)
                    
            except KeyboardInterrupt:
                print("\nExiting gracefully...")
                self.save_conversation()
                break
                
            except Exception as e:
                print(f"An error occurred: {str(e)}")

def main():
    # Replace with your actual API key
    API_KEY = "AIzaSyDJwQsaRRqMjGWSLzCfl4U8fFAdo0wy3I0"
    
    # Create and run chatbot
    try:
        chatbot = GeminiChatbot(API_KEY)
        chatbot.run_chat_loop()
    except Exception as e:
        print(f"Fatal error: {str(e)}")

if __name__ == "__main__":
    main()
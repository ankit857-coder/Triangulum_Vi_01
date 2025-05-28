import os
import time
import textwrap
from typing import Any, Dict
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI as genAi
from langchain.agents import AgentType, initialize_agent
from langchain.agents.agent import AgentExecutor
from langchain.callbacks.base import BaseCallbackHandler
from triangulum.tools_and_plugins import tools

load_dotenv()

API_KEY = os.getenv("Gemini_API")
if not API_KEY:
    raise ValueError("Gemini API key not found. Please set the Gemini_API environment variable.")

# Custom callback handler for rate limiting
class RateLimitHandler(BaseCallbackHandler):
    def __init__(self):
        self.last_call = 0
        self.min_delay = 1  # Minimum delay between calls in seconds

    def on_llm_start(self, *args, **kwargs):
        current_time = time.time()
        time_since_last = current_time - self.last_call
        if time_since_last < self.min_delay:
            time.sleep(self.min_delay - time_since_last)
        self.last_call = time.time()

def format_text(text: str, width: int = 80) -> str:
    """Format text with proper wrapping and indentation"""
    return textwrap.fill(text, width=width, replace_whitespace=False)

# Initialize the language model with Gemini
llm = genAi(
    model="gemini-1.5-flash",
    google_api_key=API_KEY,
    temperature=0,
    callbacks=[RateLimitHandler()],
    max_retries=3
)

def create_agent() -> AgentExecutor:
    """Create and configure the agent with improved settings"""
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=8,  # Increased but still limited
        early_stopping_method="generate",
    )

def handle_response(response: Dict[str, Any]) -> str:
    """Format and structure the agent's response"""
    if not response or "output" not in response:
        return "I apologize, but I couldn't generate a proper response. Please try rephrasing your question."
    
    output = response["output"].strip()
    if len(output) < 10:
        return "I apologize, but I couldn't generate a complete response. Please try asking again."
    
    # Format the response with proper sections if possible
    try:
        if ":" in output:
            # Try to split into sections
            sections = output.split("\n\n")
            formatted = []
            for section in sections:
                if ":" in section:
                    title, content = section.split(":", 1)
                    formatted.append(f"{title.strip()}:\n{textwrap.indent(content.strip(), '  ')}")
                else:
                    formatted.append(section)
            output = "\n\n".join(formatted)
    except:
        # If formatting fails, just use the original output
        pass
    
    return format_text(output)

def main():
    agent_chain = create_agent()

    print("\nWelcome to Triangulum_Vi_01 - Your AI Research Assistant!")
    print("Ask me anything about research papers, current events, or general knowledge.")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            user_query = input("\nEnter your query for process (or 'quit' to exit): ").strip()
            if not user_query:
                continue
            if user_query.lower() == 'quit':
                print("\nGoodbye! Thanks for using Triangulum_Vi_01.")
                break
            
            # Add retry logic for rate limit errors
            max_retries = 3
            retry_delay = 2
            last_error = None
            
            for attempt in range(max_retries):
                try:
                    response = agent_chain.invoke({"input": user_query})
                    print("\nResponse:", handle_response(response))
                    break
                except Exception as e:
                    last_error = e
                    if "429" in str(e) and attempt < max_retries - 1:
                        print(f"\nRate limit reached. Waiting {retry_delay} seconds before retrying...")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                    if attempt == max_retries - 1:
                        print("\nAn error occurred:", str(last_error))
                        print("Please try rephrasing your question or try a different query.")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try rephrasing your question or try a different query.")

if __name__ == "__main__":
    main()
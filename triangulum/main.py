import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI as genAi
from langchain.agents import AgentType, initialize_agent
from triangulum.tools_and_plugins import tools

load_dotenv()

API_KEY = os.getenv("Gemini_API")

# Initialize the language model with Gemini
llm = genAi(
    model="gemini-1.5-flash",
    google_api_key=API_KEY,
    temperature=0
)

# Initialize the agent with ZERO_SHOT_REACT_DESCRIPTION
agent_chain = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def main():
    # Initialize the agent with ZERO_SHOT_REACT_DESCRIPTION
    agent_chain = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    # Interactive query loop
    print("\nWelcome to Triangulum_Vi_01 - Your AI Research Assistant!")
    print("Ask me anything about research papers, current events, or general knowledge.")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            user_query = input("\nEnter your query for process (or 'quit' to exit): ")
            if user_query.lower() == 'quit':
                print("\nGoodbye! Thanks for using Triangulum_Vi_01.")
                break
                
            response = agent_chain.invoke({"input": user_query})
            print("\nResponse:", response["output"])
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()
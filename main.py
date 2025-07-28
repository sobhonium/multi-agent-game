#!/usr/bin/env python3
"""
Main entry point for the Werewolf game.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from game.graph import create_game_graph


def setup_llm():
    """
    Set up the language model for the game.
    
    Returns:
        Configured LLM instance
    """
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in your .env file.")
    
    # Create LLM instance
    llm = ChatGroq(model="llama3-8b-8192")
    
    return llm


def create_initial_state():
    """
    Create the initial game state.
    
    Returns:
        Initial game state dictionary
    """
    return {
        "turn": 0,
        "current_iter": 0,
        "max_iter": 3,
        "history": [],
        "roles": [],
        "rules": "",
        "alive_players": [i for i in range(1, 7)],
        "voted_to_leave": [],
        "dead_players": [],
    }


def main():
    """
    Main function to run the Werewolf game.
    """
    print("🐺 Welcome to the Werewolf Game! 🐺")
    print("=" * 50)
    
    try:
        # Setup LLM
        print("Setting up language model...")
        llm = setup_llm()
        
        # Create game graph
        print("Creating game graph...")
        app = create_game_graph(llm)
        
        # Create initial state
        print("Initializing game state...")
        initial_state = create_initial_state()
        
        print("\n🎮 Starting the game...")
        print("=" * 50)
        
        # Run the game
        result = app.invoke(initial_state, config={"recursion_limit": 2000})
        
        print("\n" + "=" * 50)
        print("🏁 Game finished!")
        print("=" * 50)
        
        # Print final game history
        print("\n📜 Final Game History:")
        print("-" * 30)
        for entry in result["history"]:
            print(entry)
        
    except Exception as e:
        print(f"❌ Error running the game: {e}")
        print("\n💡 Make sure you have:")
        print("  1. Set up your .env file with GROQ_API_KEY")
        print("  2. Installed all dependencies with: pip install -r requirements.txt")


if __name__ == "__main__":
    main() 
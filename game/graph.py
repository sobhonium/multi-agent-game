"""
LangGraph configuration for the Werewolf game.
"""

from langgraph.graph import StateGraph, START, END
from .state import GraphState
from .players import create_player_functions
from .game_logic import god, next_node


def create_game_graph(llm):
    """
    Create the LangGraph for the Werewolf game.
    
    Args:
        llm: Language model instance
    
    Returns:
        Compiled LangGraph application
    """
    # Create the graph
    graph = StateGraph(GraphState)
    
    # Create player functions
    player_functions = create_player_functions(llm)
    
    # Add player nodes
    for name, fn in player_functions.items():
        graph.add_node(name, fn)
    
    # Add god node
    graph.add_node("god", god)
    
    # Add edges
    graph.add_edge(START, "god")
    
    graph.add_conditional_edges(
        "god", 
        next_node,
        {    
            "to_1": "player_1",
            "to_2": "player_2", 
            "to_3": "player_3",
            "to_4": "player_4",
            "to_5": "player_5",
            "to_6": "player_6",
            "to_end": END,
        }
    )
    
    # Add edges from players back to god
    graph.add_edge("player_1", "god")
    graph.add_edge("player_2", "god")
    graph.add_edge("player_3", "god")
    graph.add_edge("player_4", "god")
    graph.add_edge("player_5", "god")
    graph.add_edge("player_6", "god")
    
    # Compile the graph
    return graph.compile() 
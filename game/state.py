"""
Game state definitions for the Werewolf game.
"""

from typing import Dict, TypedDict, Optional, List
from pydantic import BaseModel, Field


class GraphState(TypedDict):
    """State structure for the LangGraph game."""
    history: Optional[List] = None 
    turn: Optional[int] = None
    max_iter: Optional[int] = 3
    topic: Optional[str] = None
    current_iter: Optional[int] = 0
    alive_players: Optional[List] = None
    dead_players: Optional[List] = []
    voted_to_leave: Optional[List] = []


class GuessWhoIsWolf(BaseModel):
    """Pydantic model for player wolf guessing."""
    guessed_wolf: int = Field(..., description="""
        One integer of:  1, 2, 3,
                4, 5, 6
                       which each represents a player""")
    percentage_assureness: int = Field(..., description="what is the percentage of the player you are sure to be wolf")
    question: str = Field(..., description="Which of the players do you think is a wolf")
    description: str = Field(..., description="Shortly, describe what is in you mind that you picked this player as is a wolf")


# Game roles configuration
ROLES = {
    1: "wolf",
    2: "wolf", 
    3: "villeger doctor",    
    4: "villeger hunter",
    6: "villeger armor",
    5: "villeger detective",
}

# Game rules
RULES = {
    'wolf': """wolves know other wolves in the games. 
                they should collectively shoot one of the villegers 
                after each round.""",
    'villeger doctor': """can save one player in each round. wolves do not know him. he does 
                it secrectly, and if he saves on player and wolves shut him, the shot is no
                effective.
                """,
    'villeger hunter': """
        hungers one player that he thinks is a wolf after each round. 
        He can also spare that 
        if he thinks in the round cannot decisively say which on is a wolf. 
                    """,
    'villeger armour': """is the one when sent out by the villegers does not die and
    that's becuase he is wearing armor. 
                        """,
     
    'game rules': """
                    after each round all villegers decide which player should die. if
                    they decisively say one of the player is so sneaky and with a high
                    chance is wolf, that player should die.
    """,
    
    'winning rules': """
            if the number of wolves and villegers are equal the game ends and wolves are winning.
            if are wolves are recognized and death, the villegers win.
    """
} 
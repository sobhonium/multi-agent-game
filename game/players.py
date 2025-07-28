"""
Player logic and role-based behavior for the Werewolf game.
"""

from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from .state import ROLES, RULES, GuessWhoIsWolf


def run_player_turn(state, player_number, llm):
    """
    Execute a player's turn in the game.
    
    Args:
        state: Current game state
        player_number: Player number (1-6)
        llm: Language model instance
    
    Returns:
        Updated game state
    """
    player_role = ROLES[player_number]
    history_str = "\n".join(state["history"])
    
    state['turn'] = player_number
    
    # First prompt for player response
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are playing werewolf. Rules: {rules}. "
         "You are player {player_number} and your role is {role}."),
        ("human", 
         """Conversation so far:\n\n{history}\n\n. 
         Please respond as your role and if you are a wolf never 
         realve yourslef and pretend and act like a villeger. if
         you are a villeger don't say I'm a doctor or sth. Just say I'm 
         a villeger. your target should be from players {alive_players} who is most likely to be shown as a wolf to decieve villegers.
     players {dead_players} are already dead and not in the game and should not pick these.
         you should challenge others and convince the villegers. you should know that {your_teammates_if_wolf}.
         leave clear statements and shortly.  please diverge the blames and attention from
         your teammates (other wolves if you are a wolf) and defend yourself or teammates.
         
         """)
    ])

    chain = prompt | llm
    
    # Determine teammate information for wolves
    if player_number == 1:
        other_wolves_teammates = "player 2 is a wolf too and is your teammate and you should protect him and diverge the attention from him"
    elif player_number == 2:
        other_wolves_teammates = "player 1 is a wolf too and is your teammate and you should protect him and diverge the attention from him"
    else:
        other_wolves_teammates = "you don't know for sure who is a wolf and should find out by guessing from hisoty of conversation and putting pressure on a suspect you think would be a wolf candidate"   

    response = chain.invoke({
        "player_number": player_number,
        "role": player_role,
        "rules": RULES,
        "history": history_str,
        "alive_players": state["alive_players"],
        "dead_players": state["dead_players"],
        "your_teammates_if_wolf": other_wolves_teammates
    })
    
    print(f'player {player_number}): {response.content}')
    state['history'].append(f"player {player_number}: {response.content}")
    
    # Add to debug log if it exists
    if 'debug_log' not in state:
        state['debug_log'] = []
    state['debug_log'].append(f'player {player_number}): {response.content}')
    
    # Second prompt for wolf guessing
    parser = PydanticOutputParser(pydantic_object=GuessWhoIsWolf)

    prompt = ChatPromptTemplate.from_messages([
        ("system", 
     "You are a professional werewolf player who strictly follows the rules: {rules}. "
     "You MUST respond with valid JSON ONLY — no additional text, no markdown. "
     "{format_instructions}"),

        ("human", 
         """you are player {player_number}, based on the flow of conversations:{history} and the fact
         that you should avoid blames on yourself (who is player {player_number}), which one of other players do you think can be a wolf?
            Your role is: {role}. you should know that {your_teammates_if_wolf}.
     If your role is wolf  pick a villeger from players {alive_players} who is most likely to be shown as a wolf to decieve villegers.
     players {dead_players} are already dead and not in the game and should not pick these.
    """)
    ])

    prompt = prompt.partial(format_instructions=parser.get_format_instructions())
    chain = prompt | llm | parser

    response_2 = chain.invoke({
        "player_number": player_number,
        "role": ROLES[player_number],
        "rules": RULES,
        "history": history_str,
        "alive_players": state["alive_players"],
        "dead_players": state["dead_players"],
        "your_teammates_if_wolf": other_wolves_teammates
    })
    
    print(f'--> self thoughts and strategies in the brain of this player (not added in game): I think, player {response_2.guessed_wolf} with conf={response_2.percentage_assureness}% is a wolf. The reason: {response_2.description}')
    
    # Add to debug log if it exists
    if 'debug_log' not in state:
        state['debug_log'] = []
    state['debug_log'].append(f'--> self thoughts and strategies in the brain of this player (not added in game): I think, player {response_2.guessed_wolf} with conf={response_2.percentage_assureness}% is a wolf. The reason: {response_2.description}')
    
    if response_2.percentage_assureness > 50:
        state["voted_to_leave"].append(response_2.guessed_wolf)

    return state


def create_player_functions(llm):
    """
    Create player function closures with the LLM instance.
    
    Args:
        llm: Language model instance
    
    Returns:
        Dictionary of player functions
    """
    def player_1(state):
        return run_player_turn(state, player_number=1, llm=llm)

    def player_2(state):
        return run_player_turn(state, player_number=2, llm=llm)

    def player_3(state):
        return run_player_turn(state, player_number=3, llm=llm)

    def player_4(state):
        return run_player_turn(state, player_number=4, llm=llm)

    def player_5(state):
        return run_player_turn(state, player_number=5, llm=llm)

    def player_6(state):
        return run_player_turn(state, player_number=6, llm=llm)

    return {
        "player_1": player_1,
        "player_2": player_2,
        "player_3": player_3,
        "player_4": player_4,
        "player_5": player_5,
        "player_6": player_6,
    } 
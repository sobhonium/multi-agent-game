"""
Core game mechanics and logic for the Werewolf game.
"""

from collections import Counter
from .state import ROLES


def god(state):
    """
    God function that manages game state, voting, and round transitions.
    
    Args:
        state: Current game state
    
    Returns:
        Updated game state
    """
    if state['turn'] in state['dead_players']:
        return state
    
    print('='*5)
    
    # Add to debug log if it exists
    if 'debug_log' not in state:
        state['debug_log'] = []
    state['debug_log'].append('='*5)
    
    # Handle voting when turn reaches 6 (end of round)
    if state['turn'] % 6 == 0:
        if state["voted_to_leave"] != []:
            voted_to_leave = state["voted_to_leave"]

            # Count frequencies
            counter = Counter(voted_to_leave)
            print(f'These are who looked suspecious for so far: {voted_to_leave}. Lets see who should leave')
            if 'debug_log' not in state:
                state['debug_log'] = []
            state['debug_log'].append(f'These are who looked suspecious for so far: {voted_to_leave}. Lets see who should leave')
            
            print('-------------voting Started-------------')
            state['debug_log'].append('-------------voting Started-------------')
            
            # Most common value and its count
            most_common_value, count = counter.most_common(1)[0]

            # If more than half of alive_players vote for the suspect, they should leave the game
            if count >= len(state['alive_players']) / 2:
                print(f'player {most_common_value} is leaving the game. Collectively players say this.')
                state['debug_log'].append(f'player {most_common_value} is leaving the game. Collectively players say this.')
                
                state['dead_players'].append(int(most_common_value))
                value_to_remove = int(most_common_value)
                print('most common value:', most_common_value)
                state['debug_log'].append(f'most common value: {most_common_value}')
                print('dead players:', state['dead_players'])
                state['debug_log'].append(f'dead players: {state["dead_players"]}')
                if value_to_remove in state['alive_players']:
                    print('alive players before:', state['alive_players'])
                    state['debug_log'].append(f'alive players before: {state["alive_players"]}')
                    state['alive_players'].remove(value_to_remove)
                    print('alive players after:', state['alive_players'])
                    state['debug_log'].append(f'alive players after: {state["alive_players"]}')
                    state['history'].append(f"player {value_to_remove} leaves the game based on voted collected.")
                    
            else:
                print('no one leaves the game in this round.')
                state['debug_log'].append('no one leaves the game in this round.')
            print('-------------voting Ended-------------')
            state['debug_log'].append('-------------voting Ended-------------')
            state["voted_to_leave"] = []
            state['turn'] = state['turn'] + 1
        
        print('='*20)
        state['debug_log'].append('='*20)
        print('---------round started--------')
        state['debug_log'].append('---------round started--------')
        
        # Count wolves and villagers
        wolf_num = 0
        vilg_num = 0
        for i in state['alive_players']:
            if 'wolf' in ROLES[i]:
                wolf_num += 1
            else:
                vilg_num += 1
                
        state['history'].append(f"God: Dear players, there are {wolf_num} wolves and {vilg_num} villagers are alive and playing in the game.")
        print('*'*15)
        state['debug_log'].append('*'*15)
        print(f"     God: Dear players, so far {wolf_num} wolf palyers and {vilg_num} villagers are still playing.")
        state['debug_log'].append(f"     God: Dear players, so far {wolf_num} wolf palyers and {vilg_num} villagers are still playing.")
        print('*'*15)
        state['debug_log'].append('*'*15)
    
    return state


def next_node(state):
    """
    Determine the next node in the game graph based on current state.
    
    Args:
        state: Current game state
    
    Returns:
        String indicating next node or "to_end" if game should end
    """
    wolf_num = 0
    vilg_num = 0
    
    for i in state['alive_players']:
        if 'wolf' in ROLES[i]:
            wolf_num += 1
        else:
            vilg_num += 1
    
    # Check winning conditions
    if wolf_num == 0:
        print('===> final result: Villegers won and game ended')
        return "to_end"
    elif wolf_num >= vilg_num:
        print('===> final result: Wolves won and game ended')
        return "to_end"  
    
    # Find next alive player
    flag = True
    next_player = (state['turn'] + 1) % 7
    
    while flag:
        if next_player not in state['dead_players']:
            flag = False
            if next_player == 0:
                return "to_1"
            return f"to_{next_player}"
        elif next_player in state['dead_players']:
            next_player = (next_player + 1) % 6 
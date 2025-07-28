"""
Streamlit-compatible version of the Werewolf game with real-time updates.
"""

import streamlit as st
import time
from collections import Counter
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from .state import ROLES, RULES, GuessWhoIsWolf
from .players import run_player_turn
from .game_logic import god, next_node


class StreamlitGameRunner:
    """Game runner that provides real-time updates for Streamlit."""
    
    def __init__(self, llm):
        self.llm = llm
        self.state = None
        self.callback = None
    
    def set_callback(self, callback):
        """Set callback function for state updates."""
        self.callback = callback
    
    def update_state(self, new_state):
        """Update state and notify callback."""
        self.state = new_state
        if self.callback:
            self.callback(new_state)
    
    def run_player_turn_with_updates(self, player_number):
        """Run player turn with real-time updates."""
        if self.state is None:
            return
        
        # Update turn
        self.state['turn'] = player_number
        self.update_state(self.state.copy())
        time.sleep(0.5)  # Small delay for visual effect
        
        # Run the actual turn with live updates
        new_state = self._run_player_turn_live(player_number)
        self.update_state(new_state)
        
        return new_state
    
    def _run_player_turn_live(self, player_number):
        """Run player turn with live streaming updates."""
        if self.state is None:
            return self.state
        
        player_role = ROLES[player_number]
        history_str = "\n".join(self.state["history"])
        
        self.state['turn'] = player_number
        
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

        chain = prompt | self.llm
        
        # Determine teammate information for wolves
        if player_number == 1:
            other_wolves_teammates = "player 2 is a wolf too and is your teammate and you should protect him and diverge the attention from him"
        elif player_number == 2:
            other_wolves_teammates = "player 1 is a wolf too and is your teammate and you should protect him and diverge the attention from him"
        else:
            other_wolves_teammates = "you don't know for sure who is a wolf and should find out by guessing from hisoty of conversation and putting pressure on a suspect you think would be a wolf candidate"   

        # Show thinking indicator with typing animation
        self.state['current_action'] = f"🤔 Player {player_number} is thinking..."
        self.update_state(self.state.copy())
        time.sleep(0.5)
        
        # Simulate typing
        for i in range(3):
            self.state['current_action'] = f"🤔 Player {player_number} is thinking{'...'[:i+1]}"
            self.update_state(self.state.copy())
            time.sleep(0.3)

        response = chain.invoke({
            "player_number": player_number,
            "role": player_role,
            "rules": RULES,
            "history": history_str,
            "alive_players": self.state["alive_players"],
            "dead_players": self.state["dead_players"],
            "your_teammates_if_wolf": other_wolves_teammates
        })
        
        # Show player speaking
        self.state['current_action'] = f"🗣️ Player {player_number} is speaking..."
        self.update_state(self.state.copy())
        time.sleep(0.5)
        
        # Capture the print output and add to state
        player_message = f'player {player_number}): {response.content}'
        print(player_message)  # Keep original print for terminal
        self.state['history'].append(f"player {player_number}: {response.content}")
        
        # Add the print output to a special debug log
        if 'debug_log' not in self.state:
            self.state['debug_log'] = []
        self.state['debug_log'].append(player_message)
        
        self.update_state(self.state.copy())
        time.sleep(1)
        
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
        chain = prompt | self.llm | parser

        # Show thinking about voting
        self.state['current_action'] = f"🤔 Player {player_number} is deciding who to vote for..."
        self.update_state(self.state.copy())
        time.sleep(0.5)
        
        # Simulate decision making
        for i in range(2):
            self.state['current_action'] = f"🤔 Player {player_number} is deciding who to vote for{'...'[:i+1]}"
            self.update_state(self.state.copy())
            time.sleep(0.4)

        response_2 = chain.invoke({
            "player_number": player_number,
            "role": ROLES[player_number],
            "rules": RULES,
            "history": history_str,
            "alive_players": self.state["alive_players"],
            "dead_players": self.state["dead_players"],
            "your_teammates_if_wolf": other_wolves_teammates
        })
        
        # Show internal thoughts
        internal_thought = f"🧠 Player {player_number}'s internal thoughts: I think player {response_2.guessed_wolf} is a wolf ({response_2.percentage_assureness}% sure). Reason: {response_2.description}"
        self.state['current_action'] = internal_thought
        self.update_state(self.state.copy())
        time.sleep(2)
        
        # Capture the internal thoughts print output
        internal_message = f'--> self thoughts and strategies in the brain of this player (not added in game): I think, player {response_2.guessed_wolf} with conf={response_2.percentage_assureness}% is a wolf. The reason: {response_2.description}'
        print(internal_message)  # Keep original print for terminal
        
        # Add to debug log
        self.state['debug_log'].append(internal_message)
        
        if response_2.percentage_assureness > 50:
            self.state["voted_to_leave"].append(response_2.guessed_wolf)
            vote_message = f"🗳️ Player {player_number} voted to eliminate Player {response_2.guessed_wolf}"
            self.state['current_action'] = vote_message
        else:
            no_vote_message = f"🤷 Player {player_number} is not confident enough to vote"
            self.state['current_action'] = no_vote_message
        
        self.update_state(self.state.copy())
        time.sleep(1)
        
        # Clear current action
        self.state['current_action'] = None
        return self.state
    
    def run_god_turn_with_updates(self):
        """Run god turn with real-time updates."""
        if self.state is None:
            return
        
        # Show god processing
        self.state['current_action'] = "🕊️ God is processing the round..."
        self.update_state(self.state.copy())
        time.sleep(1)
        
        # Capture print output from god function
        import io
        import sys
        
        # Redirect stdout to capture print statements
        old_stdout = sys.stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            # Run god logic
            new_state = god(self.state)
            
            # Get captured output
            god_output = captured_output.getvalue()
            
            # Add captured output to debug log
            if 'debug_log' not in new_state:
                new_state['debug_log'] = []
            
            for line in god_output.strip().split('\n'):
                if line.strip():
                    new_state['debug_log'].append(line.strip())
                    print(line.strip())  # Also print to terminal
            
        finally:
            # Restore stdout
            sys.stdout = old_stdout
        
        # Show god's announcement
        if new_state.get('history') and new_state['history'] != self.state.get('history', []):
            latest_announcement = new_state['history'][-1]
            if "God:" in latest_announcement:
                self.state['current_action'] = f"🕊️ {latest_announcement}"
                self.update_state(self.state.copy())
                time.sleep(2)
        
        self.update_state(new_state)
        
        # Clear current action
        self.state['current_action'] = None
        return new_state
    
    def run_full_game(self, initial_state, callback=None):
        """Run the full game with real-time updates."""
        self.state = initial_state
        self.callback = callback
        
        # Initialize
        self.update_state(self.state)
        
        # Game loop
        while True:
            # Check winning conditions
            wolf_num = 0
            vilg_num = 0
            
            for i in self.state['alive_players']:
                if 'wolf' in ROLES[i]:
                    wolf_num += 1
                else:
                    vilg_num += 1
            
            if wolf_num == 0:
                st.success("🏆 Villagers won!")
                break
            elif wolf_num >= vilg_num:
                st.success("🏆 Wolves won!")
                break
            
            # Run god turn
            self.run_god_turn_with_updates()
            time.sleep(1)
            
            # Determine next player
            next_action = next_node(self.state)
            
            if next_action == "to_end":
                break
            
            # Run player turn
            if next_action.startswith("to_"):
                player_num = int(next_action.split("_")[1])
                if player_num in self.state['alive_players']:
                    self.run_player_turn_with_updates(player_num)
                    time.sleep(1)
        
        return self.state


def create_streamlit_game_runner(llm):
    """Create a Streamlit game runner instance."""
    return StreamlitGameRunner(llm)


def display_game_metrics(state):
    """Display game metrics in Streamlit."""
    if not state:
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Alive Players", len(state.get("alive_players", [])))
    
    with col2:
        wolf_count = sum(1 for p in state.get("alive_players", []) if "wolf" in ROLES.get(p, ""))
        st.metric("🐺 Wolves", wolf_count)
    
    with col3:
        villager_count = len(state.get("alive_players", [])) - wolf_count
        st.metric("👥 Villagers", villager_count)
    
    with col4:
        current_turn = state.get("turn", 0)
        if current_turn > 0:
            st.metric("🎯 Current Turn", f"Player {current_turn}")
        else:
            st.metric("🎯 Current Turn", "God")
    
    # Display current action
    current_action = state.get("current_action")
    if current_action:
        st.info(f"🔄 **Live Action:** {current_action}")


def display_players_status(state):
    """Display players status in a grid."""
    if not state:
        return
    
    st.subheader("🎮 Players Status")
    
    cols = st.columns(3)
    for i, player_num in enumerate(range(1, 7)):
        col_idx = i % 3
        with cols[col_idx]:
            role = ROLES.get(player_num, "unknown")
            
            if player_num in state.get("alive_players", []):
                if "wolf" in role:
                    st.success(f"🐺 Player {player_num} - {role}")
                else:
                    st.info(f"👤 Player {player_num} - {role}")
                
                # Highlight current speaker
                if state.get("turn") == player_num:
                    st.markdown("**🎯 Currently Speaking**")
            else:
                st.error(f"💀 Player {player_num} - Dead")


def display_voting_status(state):
    """Display current voting status."""
    if not state:
        return
    
    voted_to_leave = state.get("voted_to_leave", [])
    if not voted_to_leave:
        return
    
    st.subheader("🗳️ Current Votes")
    
    vote_counts = Counter(voted_to_leave)
    alive_count = len(state.get("alive_players", []))
    
    for player, count in vote_counts.items():
        st.write(f"Player {player}: {count} vote(s)")
    
    most_voted, max_votes = vote_counts.most_common(1)[0]
    
    if max_votes >= alive_count / 2:
        st.warning(f"⚠️ Player {most_voted} will be eliminated!")
    else:
        st.info(f"📊 Player {most_voted} has the most votes ({max_votes}/{alive_count//2 + 1} needed)")


def display_game_history(state):
    """Display game history with styling."""
    if not state:
        return
    
    st.subheader("📜 Live Game Chat")
    
    history = state.get("history", [])
    debug_log = state.get("debug_log", [])
    
    # Create a chat-like container
    chat_container = st.container()
    
    with chat_container:
        # Show messages in a chat-like format
        for i, entry in enumerate(history):
            if "God:" in entry:
                # God messages in a special box
                st.markdown(f"""
                <div style="background-color: #f0f8ff; padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 4px solid #0066cc;">
                    <strong>🕊️ {entry}</strong>
                </div>
                """, unsafe_allow_html=True)
            elif "player" in entry and ":" in entry:
                try:
                    player_num = entry.split("player ")[1].split(":")[0]
                    role = ROLES.get(int(player_num), "unknown")
                    message = entry.split(': ', 1)[1] if ': ' in entry else entry
                    
                    if "wolf" in role:
                        # Wolf messages in red-tinted box
                        st.markdown(f"""
                        <div style="background-color: #fff0f0; padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 4px solid #cc0000;">
                            <strong>🐺 Player {player_num}</strong><br>
                            {message}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Villager messages in green-tinted box
                        st.markdown(f"""
                        <div style="background-color: #f0fff0; padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 4px solid #00cc00;">
                            <strong>👤 Player {player_num}</strong><br>
                            {message}
                        </div>
                        """, unsafe_allow_html=True)
                except:
                    st.markdown(f"""
                    <div style="background-color: #f8f8f8; padding: 10px; border-radius: 10px; margin: 5px 0;">
                        💬 {entry}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: #f8f8f8; padding: 10px; border-radius: 10px; margin: 5px 0;">
                    💬 {entry}
                </div>
                """, unsafe_allow_html=True)
    
    # Show debug log (print statements) in a separate section
    if debug_log:
        st.subheader("🔍 Debug Log (Print Statements)")
        for log_entry in debug_log:
            if "player" in log_entry and "):" in log_entry:
                # Player speaking
                st.markdown(f"""
                <div style="background-color: #e8f4fd; padding: 8px; border-radius: 8px; margin: 3px 0; font-family: monospace; font-size: 0.9em;">
                    🗣️ {log_entry}
                </div>
                """, unsafe_allow_html=True)
            elif "--> self thoughts" in log_entry:
                # Internal thoughts
                st.markdown(f"""
                <div style="background-color: #fff2e6; padding: 8px; border-radius: 8px; margin: 3px 0; font-family: monospace; font-size: 0.9em;">
                    🧠 {log_entry}
                </div>
                """, unsafe_allow_html=True)
            elif "voting Started" in log_entry or "voting Ended" in log_entry:
                # Voting events
                st.markdown(f"""
                <div style="background-color: #f0f8ff; padding: 8px; border-radius: 8px; margin: 3px 0; font-family: monospace; font-size: 0.9em;">
                    🗳️ {log_entry}
                </div>
                """, unsafe_allow_html=True)
            elif "round started" in log_entry or "God:" in log_entry:
                # Round events
                st.markdown(f"""
                <div style="background-color: #f0fff0; padding: 8px; border-radius: 8px; margin: 3px 0; font-family: monospace; font-size: 0.9em;">
                    🕊️ {log_entry}
                </div>
                """, unsafe_allow_html=True)
            else:
                # Other debug messages
                st.markdown(f"""
                <div style="background-color: #f8f8f8; padding: 8px; border-radius: 8px; margin: 3px 0; font-family: monospace; font-size: 0.9em;">
                    🔍 {log_entry}
                </div>
                """, unsafe_allow_html=True)
    
    # Show current action if any
    current_action = state.get("current_action")
    if current_action:
        st.markdown(f"""
        <div style="background-color: #fff3cd; padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 4px solid #ffc107;">
            <strong>🔄 {current_action}</strong>
        </div>
        """, unsafe_allow_html=True)


def create_initial_state():
    """Create initial game state."""
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
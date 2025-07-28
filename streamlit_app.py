#!/usr/bin/env python3
"""
Streamlit app for the Werewolf game with real-time updates.
"""

import streamlit as st
import time
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from game.graph import create_game_graph
from game.state import ROLES
from game.streamlit_game import (
    create_streamlit_game_runner,
    display_game_metrics,
    display_players_status,
    display_voting_status,
    display_game_history,
    create_initial_state
)


def setup_llm():
    """Set up the language model for the game."""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY not found in environment variables. Please set it in your .env file.")
        st.stop()
    
    return ChatGroq(model="llama3-8b-8192")


def get_player_role(player_num):
    """Get player role with emoji."""
    role = ROLES.get(player_num, "unknown")
    if "wolf" in role:
        return f"🐺 {role}"
    elif "doctor" in role:
        return f"👨‍⚕️ {role}"
    elif "hunter" in role:
        return f"🏹 {role}"
    elif "armor" in role:
        return f"🛡️ {role}"
    elif "detective" in role:
        return f"🔍 {role}"
    else:
        return f"👤 {role}"


def main():
    st.set_page_config(
        page_title="Werewolf Game - Live Stream",
        page_icon="🐺",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🐺 Werewolf Game - Live Stream")
    st.markdown("Watch AI players battle it out in real-time!")
    
    # Sidebar for controls and info
    with st.sidebar:
        st.header("🎮 Game Controls")
        
        if st.button("🚀 Start New Game", type="primary"):
            st.session_state.game_started = True
            st.session_state.game_finished = False
            st.session_state.current_state = None
            st.rerun()
        
        st.header("📊 Game Info")
        st.info("""
        **Game Rules:**
        - Wolves try to eliminate villagers
        - Villagers try to identify and eliminate wolves
        - Players vote to eliminate suspicious players
        - Special roles have unique abilities
        """)
        
        st.header("🎭 Player Roles")
        for player_num, role in ROLES.items():
            st.write(f"Player {player_num}: {get_player_role(player_num)}")
    
    # Main game area
    if not st.session_state.get("game_started", False):
        st.info("👆 Click 'Start New Game' in the sidebar to begin!")
        return
    
    # Initialize game if not already done
    if st.session_state.get("current_state") is None:
        with st.spinner("Setting up the game..."):
            llm = setup_llm()
            game_runner = create_streamlit_game_runner(llm)
            initial_state = create_initial_state()
            
            # Store in session state
            st.session_state.game_runner = game_runner
            st.session_state.current_state = initial_state
            st.session_state.game_started = True
    
    # Display game state
    current_state = st.session_state.get("current_state")
    
    if current_state:
        # Game metrics
        display_game_metrics(current_state)
        
        # Players status
        display_players_status(current_state)
        
        # Voting status
        display_voting_status(current_state)
        
        # Game history
        display_game_history(current_state)
        
        # Game controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⏭️ Next Turn"):
                if st.session_state.get("game_runner"):
                    # Run next turn
                    game_runner = st.session_state.game_runner
                    current_state = st.session_state.current_state
                    
                    # Determine next action
                    from game.game_logic import next_node
                    next_action = next_node(current_state)
                    
                    if next_action == "to_end":
                        st.success("🏆 Game finished!")
                        st.session_state.game_finished = True
                    elif next_action.startswith("to_"):
                        player_num = int(next_action.split("_")[1])
                        if player_num in current_state['alive_players']:
                            with st.spinner(f"Player {player_num} is thinking..."):
                                new_state = game_runner.run_player_turn_with_updates(player_num)
                                st.session_state.current_state = new_state
                                st.rerun()
        
        with col2:
            if st.button("🕊️ God Turn"):
                if st.session_state.get("game_runner"):
                    with st.spinner("God is processing..."):
                        game_runner = st.session_state.game_runner
                        new_state = game_runner.run_god_turn_with_updates()
                        st.session_state.current_state = new_state
                        st.rerun()
        
        with col3:
            if st.button("🏁 Run Full Game"):
                if st.session_state.get("game_runner"):
                    st.info("Running full game with live updates...")
                    
                    # Create placeholders for live updates
                    metrics_placeholder = st.empty()
                    players_placeholder = st.empty()
                    voting_placeholder = st.empty()
                    history_placeholder = st.empty()
                    
                    def update_callback(state):
                        with metrics_placeholder.container():
                            display_game_metrics(state)
                        with players_placeholder.container():
                            display_players_status(state)
                        with voting_placeholder.container():
                            display_voting_status(state)
                        with history_placeholder.container():
                            display_game_history(state)
                    
                    game_runner = st.session_state.game_runner
                    game_runner.set_callback(update_callback)
                    
                    with st.spinner("Running the full game with live updates..."):
                        final_state = game_runner.run_full_game(current_state)
                        st.session_state.current_state = final_state
                        st.success("🏆 Game completed!")
                        st.rerun()
        
        # Auto-advance option
        col4, col5 = st.columns(2)
        with col4:
            auto_advance = st.checkbox("🔄 Auto-advance turns", value=False)
        
        with col5:
            if auto_advance and st.session_state.get("game_runner"):
                import time
                time.sleep(2)  # Wait 2 seconds between auto-advances
                
                # Auto-advance logic
                game_runner = st.session_state.game_runner
                current_state = st.session_state.current_state
                
                from game.game_logic import next_node
                next_action = next_node(current_state)
                
                if next_action == "to_end":
                    st.success("🏆 Game finished!")
                    st.session_state.game_finished = True
                elif next_action.startswith("to_"):
                    player_num = int(next_action.split("_")[1])
                    if player_num in current_state['alive_players']:
                        new_state = game_runner.run_player_turn_with_updates(player_num)
                        st.session_state.current_state = new_state
                        st.rerun()


if __name__ == "__main__":
    main() 
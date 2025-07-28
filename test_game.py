#!/usr/bin/env python3
"""
Basic tests for the Werewolf game components.
"""

import pytest
from game.state import GraphState, GuessWhoIsWolf, ROLES, RULES
from game.game_logic import next_node


def test_graph_state():
    """Test GraphState structure."""
    state = GraphState(
        history=[],
        turn=0,
        max_iter=3,
        alive_players=[1, 2, 3, 4, 5, 6],
        dead_players=[],
        voted_to_leave=[]
    )
    assert state["turn"] == 0
    assert len(state["alive_players"]) == 6


def test_roles_configuration():
    """Test that roles are properly configured."""
    assert 1 in ROLES
    assert 2 in ROLES
    assert "wolf" in ROLES[1]
    assert "wolf" in ROLES[2]


def test_rules_configuration():
    """Test that rules are properly configured."""
    assert "wolf" in RULES
    assert "game rules" in RULES
    assert "winning rules" in RULES


def test_next_node_function():
    """Test next_node function with basic state."""
    state = {
        "turn": 0,
        "alive_players": [1, 2, 3, 4, 5, 6],
        "dead_players": [],
        "voted_to_leave": []
    }
    
    # Test that it returns a valid next action
    result = next_node(state)
    assert result in ["to_1", "to_2", "to_3", "to_4", "to_5", "to_6", "to_end"]


def test_guess_who_is_wolf_model():
    """Test the Pydantic model for wolf guessing."""
    guess = GuessWhoIsWolf(
        guessed_wolf=3,
        percentage_assureness=75,
        question="Which player do you think is a wolf?",
        description="Player 3 seems suspicious"
    )
    assert guess.guessed_wolf == 3
    assert guess.percentage_assureness == 75
    assert "suspicious" in guess.description


if __name__ == "__main__":
    pytest.main([__file__]) 
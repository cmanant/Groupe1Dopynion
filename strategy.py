"""
Main strategy logic for Rhum & Ruin bot.
Contains the core decision-making functions.
"""

from dopynion.data_model import Game
from game_state import GameState
from strategy_helpers import (
    count_copper_in_hand,
    is_estate_available_in_stock,
    get_player_hand_as_list,
)


def should_buy_estate(game: Game, game_state: GameState) -> bool:
    """Determine if we should buy an Estate card based on our strategy."""
    print("\n" + "="*50)
    print("🤔 EVALUATING ESTATE PURCHASE STRATEGY")
    print("="*50)
    
    # Check if we have any purchases remaining this turn
    if not game_state.can_purchase():
        print(f"❌ Cannot buy Estate: No purchases remaining this turn ({game_state.purchases_remaining_this_turn})")
        print("="*50 + "\n")
        return False
    
    # Get our hand as a list
    our_hand = get_player_hand_as_list(game)
    if not our_hand:  # Empty hand means something went wrong
        print("❌ Cannot buy Estate: No hand found")
        print("="*50 + "\n")
        return False
    
    # Check if we have at least 2 Copper cards
    copper_count = count_copper_in_hand(our_hand)
    if copper_count < 2:
        print(f"❌ Cannot buy Estate: Need 2+ Copper, but only have {copper_count}")
        print("="*50 + "\n")
        return False
    
    # Check if Estate is available in stock
    if not is_estate_available_in_stock(game.stock):
        print("❌ Cannot buy Estate: No Estate available in stock")
        print("="*50 + "\n")
        return False
    
    print(f"✅ ALL CONDITIONS MET! Will buy Estate (purchases remaining: {game_state.purchases_remaining_this_turn})")
    print("="*50 + "\n")
    return True
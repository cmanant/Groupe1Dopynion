"""
Helper functions for Rhum & Ruin strategy.
Contains utility functions for game analysis and card counting.
"""

from dopynion.data_model import CardName, Cards, Game


def count_copper_in_hand(hand: list[CardName]) -> int:
    """Count the number of Copper cards in the given hand."""
    copper_count = hand.count(CardName.COPPER)
    print(f"🪙 Copper count in hand: {copper_count} (total cards: {len(hand)})")
    return copper_count


def is_estate_available_in_stock(stock: Cards) -> bool:
    """Check if Estate cards are available in the stock."""
    estate_quantity = stock.quantities.get(CardName.ESTATE, 0)
    available = estate_quantity > 0
    print(f"🏘️ Estate availability in stock: {estate_quantity} cards available -> {available}")
    return available


def get_player_hand_as_list(game: Game) -> list[CardName]:
    """Get our player's hand as a list of CardName.
    Since we receive the /play request, it's our turn and our hand should be the active one."""
    print(f"🎮 Looking for player 'Rhum & Ruin' among {len(game.players)} players")
    
    for player in game.players:
        print(f"   - Player: {player.name}, hand: {player.hand}")
        if "Rhum & Ruin" in player.name and player.hand is not None:
            # Convert Cards (quantities) to list of CardName
            hand_list = []
            for card_name, quantity in player.hand.quantities.items():
                hand_list.extend([card_name] * quantity)
            print(f"✅ Found our player! Hand: {hand_list}")
            return hand_list
    
    print("❌ Our player 'Rhum & Ruin' not found or has no hand!")
    return []
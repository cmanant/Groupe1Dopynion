"""
Game state management for Rhum & Ruin bot.
Handles per-game state tracking for multiple simultaneous games.
"""

class GameState:
    """Class to track the state of a specific game."""
    
    def __init__(self, game_id: str):
        self.game_id = game_id
        self.purchases_remaining_this_turn = 1
        # Future: Add other game-specific state variables here
        # self.actions_remaining_this_turn = 1
        # self.money_available = 0
        # self.cards_bought_this_game = []
    
    def reset_turn(self):
        """Reset turn-specific counters."""
        self.purchases_remaining_this_turn = 1
        print(f"🔄 Turn reset for game {self.game_id}: purchases = {self.purchases_remaining_this_turn}")
    
    def use_purchase(self):
        """Consume one purchase and return if successful."""
        if self.purchases_remaining_this_turn > 0:
            self.purchases_remaining_this_turn -= 1
            print(f"🛒 Purchase used for game {self.game_id}: {self.purchases_remaining_this_turn} remaining")
            return True
        return False
    
    def can_purchase(self) -> bool:
        """Check if we can make a purchase."""
        return self.purchases_remaining_this_turn > 0


# Dictionary to store game states by game_id
game_states: dict[str, GameState] = {}


def get_game_state(game_id: str) -> GameState:
    """Get or create game state for a specific game."""
    if game_id not in game_states:
        game_states[game_id] = GameState(game_id)
        print(f"🆕 Created new game state for game {game_id}")
    return game_states[game_id]
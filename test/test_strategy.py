from dopynion.data_model import CardName, Game, Player, Hand, Cards
from game_state import GameState
from strategy_helpers import (
    count_copper_in_hand,
    is_estate_available_in_stock,
    get_player_hand_as_list,
)
from strategy import should_buy_estate


class TestCountCopperInHand:
    """Tests for count_copper_in_hand function."""
    
    def test_no_copper_cards(self):
        """Test counting when there are no copper cards."""
        hand = [CardName.ESTATE, CardName.SILVER, CardName.GOLD]
        assert count_copper_in_hand(hand) == 0
    
    def test_one_copper_card(self):
        """Test counting when there is one copper card."""
        hand = [CardName.COPPER, CardName.ESTATE, CardName.SILVER]
        assert count_copper_in_hand(hand) == 1
    
    def test_multiple_copper_cards(self):
        """Test counting when there are multiple copper cards."""
        hand = [CardName.COPPER, CardName.COPPER, CardName.ESTATE, CardName.COPPER]
        assert count_copper_in_hand(hand) == 3
    
    def test_all_copper_cards(self):
        """Test counting when all cards are copper."""
        hand = [CardName.COPPER, CardName.COPPER, CardName.COPPER]
        assert count_copper_in_hand(hand) == 3
    
    def test_empty_hand(self):
        """Test counting with an empty hand."""
        hand = []
        assert count_copper_in_hand(hand) == 0


class TestIsEstateAvailableInStock:
    """Tests for is_estate_available_in_stock function."""
    
    def test_estate_available(self):
        """Test when Estate cards are available in stock."""
        stock = Cards(quantities={CardName.ESTATE: 5, CardName.COPPER: 10})
        assert is_estate_available_in_stock(stock) == True
    
    def test_estate_not_available(self):
        """Test when Estate cards are not available in stock."""
        stock = Cards(quantities={CardName.ESTATE: 0, CardName.COPPER: 10})
        assert is_estate_available_in_stock(stock) == False
    
    def test_estate_not_in_stock(self):
        """Test when Estate is not even in the stock dictionary."""
        stock = Cards(quantities={CardName.COPPER: 10, CardName.SILVER: 5})
        assert is_estate_available_in_stock(stock) == False
    
    def test_empty_stock(self):
        """Test with empty stock."""
        stock = Cards(quantities={})
        assert is_estate_available_in_stock(stock) == False


class TestGetPlayerHandAsList:
    """Tests for get_player_hand_as_list function."""
    
    def test_get_player_hand_with_cards(self):
        """Test getting our player's hand when they have cards."""
        players = [
            Player(name="Other Player", hand=Cards(quantities={}), score=0),
            Player(name="Rhum & Ruin", hand=Cards(quantities={CardName.COPPER: 2, CardName.ESTATE: 1}), score=0),
            Player(name="Another Player", hand=Cards(quantities={}), score=0),
        ]
        game = Game(finished=False, players=players, stock=Cards())
        
        result = get_player_hand_as_list(game)
        assert len(result) == 3
        assert result.count(CardName.COPPER) == 2
        assert result.count(CardName.ESTATE) == 1
    
    def test_get_player_hand_empty_hand(self):
        """Test when our player exists but has no cards."""
        players = [
            Player(name="Other Player", hand=Cards(quantities={CardName.COPPER: 1}), score=0),
            Player(name="Rhum & Ruin", hand=Cards(quantities={}), score=0),
        ]
        game = Game(finished=False, players=players, stock=Cards())
        
        result = get_player_hand_as_list(game)
        assert result == []
    
    def test_our_player_not_found(self):
        """Test when our player is not in the game."""
        players = [
            Player(name="Other Player", hand=Cards(quantities={CardName.COPPER: 1}), score=0),
            Player(name="Another Player", hand=Cards(quantities={}), score=0),
        ]
        game = Game(finished=False, players=players, stock=Cards())
        
        result = get_player_hand_as_list(game)
        assert result == []
    
    def test_empty_players_list(self):
        """Test with empty players list."""
        game = Game(finished=False, players=[], stock=Cards())
        
        result = get_player_hand_as_list(game)
        assert result == []


class TestShouldBuyEstate:
    """Tests for should_buy_estate function."""
    
    def test_should_buy_estate_all_conditions_met(self):
        """Test when all conditions are met: our turn, 2+ copper, estate available."""
        players = [
            Player(name="Rhum & Ruin", hand=Cards(quantities={CardName.COPPER: 2, CardName.ESTATE: 1}), score=0),
        ]
        stock = Cards(quantities={CardName.ESTATE: 5, CardName.COPPER: 10})
        game = Game(finished=False, players=players, stock=stock)
        game_state = GameState("test_game")
        
        assert should_buy_estate(game, game_state) == True
    
    def test_should_not_buy_estate_no_purchases_remaining(self):
        """Test when no purchases remaining this turn."""
        players = [
            Player(name="Rhum & Ruin", hand=Cards(quantities={CardName.COPPER: 3}), score=0),
        ]
        stock = Cards(quantities={CardName.ESTATE: 5, CardName.COPPER: 10})
        game = Game(finished=False, players=players, stock=stock)
        game_state = GameState("test_game")
        game_state.purchases_remaining_this_turn = 0  # No purchases left
        
        assert should_buy_estate(game, game_state) == False
    
    def test_should_not_buy_estate_not_our_turn(self):
        """Test when it's not our turn (empty hand)."""
        players = [
            Player(name="Rhum & Ruin", hand=Cards(quantities={}), score=0),
        ]
        stock = Cards(quantities={CardName.ESTATE: 5, CardName.COPPER: 10})
        game = Game(finished=False, players=players, stock=stock)
        game_state = GameState("test_game")
        
        assert should_buy_estate(game, game_state) == False
    
    def test_should_not_buy_estate_insufficient_copper(self):
        """Test when we have less than 2 copper cards."""
        players = [
            Player(name="Rhum & Ruin", hand=Cards(quantities={CardName.COPPER: 1, CardName.ESTATE: 1}), score=0),
        ]
        stock = Cards(quantities={CardName.ESTATE: 5, CardName.COPPER: 10})
        game = Game(finished=False, players=players, stock=stock)
        game_state = GameState("test_game")
        
        assert should_buy_estate(game, game_state) == False
    
    def test_should_not_buy_estate_no_copper(self):
        """Test when we have no copper cards."""
        players = [
            Player(name="Rhum & Ruin", hand=Cards(quantities={CardName.ESTATE: 1, CardName.SILVER: 1}), score=0),
        ]
        stock = Cards(quantities={CardName.ESTATE: 5, CardName.COPPER: 10})
        game = Game(finished=False, players=players, stock=stock)
        game_state = GameState("test_game")
        
        assert should_buy_estate(game, game_state) == False
    
    def test_should_not_buy_estate_no_estate_in_stock(self):
        """Test when estate is not available in stock."""
        players = [
            Player(name="Rhum & Ruin", hand=Cards(quantities={CardName.COPPER: 2, CardName.ESTATE: 1}), score=0),
        ]
        stock = Cards(quantities={CardName.ESTATE: 0, CardName.COPPER: 10})
        game = Game(finished=False, players=players, stock=stock)
        game_state = GameState("test_game")
        
        assert should_buy_estate(game, game_state) == False
    
    def test_should_not_buy_estate_player_not_found(self):
        """Test when our player is not found in the game."""
        players = [
            Player(name="Other Player", hand=Cards(quantities={CardName.COPPER: 2}), score=0),
        ]
        stock = Cards(quantities={CardName.ESTATE: 5, CardName.COPPER: 10})
        game = Game(finished=False, players=players, stock=stock)
        game_state = GameState("test_game")
        
        assert should_buy_estate(game, game_state) == False
    
    def test_should_buy_estate_exactly_two_copper(self):
        """Test edge case with exactly 2 copper cards."""
        players = [
            Player(name="Rhum & Ruin", hand=Cards(quantities={CardName.COPPER: 2}), score=0),
        ]
        stock = Cards(quantities={CardName.ESTATE: 1, CardName.COPPER: 10})
        game = Game(finished=False, players=players, stock=stock)
        game_state = GameState("test_game")
        
        assert should_buy_estate(game, game_state) == True
    
    def test_should_buy_estate_many_copper(self):
        """Test with many copper cards."""
        players = [
            Player(name="Rhum & Ruin", hand=Cards(quantities={CardName.COPPER: 7}), score=0),
        ]
        stock = Cards(quantities={CardName.ESTATE: 1, CardName.COPPER: 10})
        game = Game(finished=False, players=players, stock=stock)
        game_state = GameState("test_game")
        
        assert should_buy_estate(game, game_state) == True


class TestGameState:
    """Tests for GameState class."""
    
    def test_game_state_initialization(self):
        """Test GameState initialization."""
        game_state = GameState("test_game_123")
        assert game_state.game_id == "test_game_123"
        assert game_state.purchases_remaining_this_turn == 1
    
    def test_can_purchase(self):
        """Test can_purchase method."""
        game_state = GameState("test_game")
        assert game_state.can_purchase() == True
        
        game_state.purchases_remaining_this_turn = 0
        assert game_state.can_purchase() == False
    
    def test_use_purchase(self):
        """Test use_purchase method."""
        game_state = GameState("test_game")
        
        # Should successfully use purchase
        assert game_state.use_purchase() == True
        assert game_state.purchases_remaining_this_turn == 0
        
        # Should fail to use purchase when none left
        assert game_state.use_purchase() == False
        assert game_state.purchases_remaining_this_turn == 0
    
    def test_reset_turn(self):
        """Test reset_turn method."""
        game_state = GameState("test_game")
        game_state.purchases_remaining_this_turn = 0
        
        game_state.reset_turn()
        assert game_state.purchases_remaining_this_turn == 1
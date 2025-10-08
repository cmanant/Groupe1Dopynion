from dopynion.data_model import CardName, Game, Player, Hand, Cards
from BOOT import (
    count_copper_in_hand,
    is_estate_available_in_stock,
    find_our_player,
    should_buy_estate,
)


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


class TestFindOurPlayer:
    """Tests for find_our_player function."""
    
    def test_find_our_player_with_cards(self):
        """Test finding our player when they have cards (their turn)."""
        players = [
            Player(name="Other Player", hand=Cards(quantities={}), score=0),
            Player(name="Rhum & Ruin", hand=Cards(quantities={CardName.COPPER: 2, CardName.ESTATE: 1}), score=0),
            Player(name="Another Player", hand=Cards(quantities={}), score=0),
        ]
        game = Game(finished=False, players=players, stock=Cards())
        
        result = find_our_player(game)
        assert result is not None
        # Should return hand with 2 Copper + 1 Estate = 3 cards total
        assert len(result.hand) == 3
        assert result.hand.count(CardName.COPPER) == 2
        assert result.hand.count(CardName.ESTATE) == 1
    
    def test_find_our_player_empty_hand(self):
        """Test when our player exists but has no cards (not their turn)."""
        players = [
            Player(name="Other Player", hand=Cards(quantities={CardName.COPPER: 1}), score=0),
            Player(name="Rhum & Ruin", hand=Cards(quantities={}), score=0),
        ]
        game = Game(finished=False, players=players, stock=Cards())
        
        result = find_our_player(game)
        assert result is None
    
    def test_our_player_not_found(self):
        """Test when our player is not in the game."""
        players = [
            Player(name="Other Player", hand=Cards(quantities={CardName.COPPER: 1}), score=0),
            Player(name="Another Player", hand=Cards(quantities={}), score=0),
        ]
        game = Game(finished=False, players=players, stock=Cards())
        
        result = find_our_player(game)
        assert result is None
    
    def test_empty_players_list(self):
        """Test with empty players list."""
        game = Game(finished=False, players=[], stock=Cards())
        
        result = find_our_player(game)
        assert result is None


class TestShouldBuyEstate:
    """Tests for should_buy_estate function."""
    
    def test_should_buy_estate_all_conditions_met(self):
        """Test when all conditions are met: our turn, 2+ copper, estate available."""
        players = [
            Player(name="Rhum & Ruin", hand=Cards(quantities={CardName.COPPER: 2, CardName.ESTATE: 1}), score=0),
        ]
        stock = Cards(quantities={CardName.ESTATE: 5, CardName.COPPER: 10})
        game = Game(finished=False, players=players, stock=stock)
        
        assert should_buy_estate(game) == True
    
    def test_should_not_buy_estate_not_our_turn(self):
        """Test when it's not our turn (empty hand)."""
        players = [
            Player(name="Rhum & Ruin", hand=Cards(quantities={}), score=0),
        ]
        stock = Cards(quantities={CardName.ESTATE: 5, CardName.COPPER: 10})
        game = Game(finished=False, players=players, stock=stock)
        
        assert should_buy_estate(game) == False
    
    def test_should_not_buy_estate_insufficient_copper(self):
        """Test when we have less than 2 copper cards."""
        players = [
            Player(name="Rhum & Ruin", hand=Cards(quantities={CardName.COPPER: 1, CardName.ESTATE: 1}), score=0),
        ]
        stock = Cards(quantities={CardName.ESTATE: 5, CardName.COPPER: 10})
        game = Game(finished=False, players=players, stock=stock)
        
        assert should_buy_estate(game) == False
    
    def test_should_not_buy_estate_no_copper(self):
        """Test when we have no copper cards."""
        players = [
            Player(name="Rhum & Ruin", hand=Cards(quantities={CardName.ESTATE: 1, CardName.SILVER: 1}), score=0),
        ]
        stock = Cards(quantities={CardName.ESTATE: 5, CardName.COPPER: 10})
        game = Game(finished=False, players=players, stock=stock)
        
        assert should_buy_estate(game) == False
    
    def test_should_not_buy_estate_no_estate_in_stock(self):
        """Test when estate is not available in stock."""
        players = [
            Player(name="Rhum & Ruin", hand=Cards(quantities={CardName.COPPER: 2, CardName.ESTATE: 1}), score=0),
        ]
        stock = Cards(quantities={CardName.ESTATE: 0, CardName.COPPER: 10})
        game = Game(finished=False, players=players, stock=stock)
        
        assert should_buy_estate(game) == False
    
    def test_should_not_buy_estate_player_not_found(self):
        """Test when our player is not found in the game."""
        players = [
            Player(name="Other Player", hand=Cards(quantities={CardName.COPPER: 2}), score=0),
        ]
        stock = Cards(quantities={CardName.ESTATE: 5, CardName.COPPER: 10})
        game = Game(finished=False, players=players, stock=stock)
        
        assert should_buy_estate(game) == False
    
    def test_should_buy_estate_exactly_two_copper(self):
        """Test edge case with exactly 2 copper cards."""
        players = [
            Player(name="Rhum & Ruin", hand=Cards(quantities={CardName.COPPER: 2}), score=0),
        ]
        stock = Cards(quantities={CardName.ESTATE: 1, CardName.COPPER: 10})
        game = Game(finished=False, players=players, stock=stock)
        
        assert should_buy_estate(game) == True
    
    def test_should_buy_estate_many_copper(self):
        """Test with many copper cards."""
        players = [
            Player(name="Rhum & Ruin", hand=Cards(quantities={CardName.COPPER: 7}), score=0),
        ]
        stock = Cards(quantities={CardName.ESTATE: 1, CardName.COPPER: 10})
        game = Game(finished=False, players=players, stock=stock)
        
        assert should_buy_estate(game) == True
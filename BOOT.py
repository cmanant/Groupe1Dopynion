import html
from pathlib import Path
from typing import Annotated

from dopynion.data_model import (
    CardName,
    CardNameAndHand,
    Cards,
    Game,
    Hand,
    MoneyCardsInHand,
    PossibleCards,
)
from fastapi import Depends, FastAPI, Header, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI()

#####################################################
# Data model for responses
#####################################################


class DopynionResponseBool(BaseModel):
    game_id: str
    decision: bool


class DopynionResponseCardName(BaseModel):
    game_id: str
    decision: CardName


class DopynionResponseStr(BaseModel):
    game_id: str
    decision: str


#####################################################
# Getter for the game identifier
#####################################################


def get_game_id(x_game_id: str = Header(description="ID of the game")) -> str:
    return x_game_id


GameIdDependency = Annotated[str, Depends(get_game_id)]


#####################################################
# Error management
#####################################################


@app.exception_handler(Exception)
def unknown_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    print(exc.__class__.__name__, str(exc))
    return JSONResponse(
        status_code=500,
        content={
            "message": "Oops!",
            "detail": str(exc),
            "name": exc.__class__.__name__,
        },
    )


#####################################################
# Template extra bonus
#####################################################


# The root of the website shows the code of the website
@app.get("/", response_class=HTMLResponse)
def root() -> str:
    header = (
        "<html><head><title>Dopynion template</title></head><body>"
        "<h1>Dopynion documentation</h1>"
        "<h2>API documentation</h2>"
        '<p><a href="/docs">Read the documentation.</a></p>'
        "<h2>Code template</h2>"
        "<p>The code of this website is:</p>"
        "<pre>"
    )
    footer = "</pre></body></html>"
    return header + html.escape(Path(__file__).read_text(encoding="utf-8")) + footer


#####################################################
# The code of the strategy
#####################################################


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


def should_buy_estate(game: Game) -> bool:
    """Determine if we should buy an Estate card based on our strategy."""
    print("\n" + "="*50)
    print("🤔 EVALUATING ESTATE PURCHASE STRATEGY")
    print("="*50)
    
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
    
    print("✅ ALL CONDITIONS MET! Will buy Estate")
    print("="*50 + "\n")
    return True


@app.get("/name")
def name() -> str:
    return "Rhum & Ruin"


@app.get("/start_game")
def start_game(game_id: GameIdDependency) -> DopynionResponseStr:
    print(f"🚀 GAME STARTED - Game ID: {game_id}")
    return DopynionResponseStr(game_id=game_id, decision="OK")


@app.get("/start_turn")
def start_turn(game_id: GameIdDependency) -> DopynionResponseStr:
    print(f"▶️ TURN STARTED - Game ID: {game_id}")
    return DopynionResponseStr(game_id=game_id, decision="OK")


@app.post("/play")
def play(game: Game, game_id: GameIdDependency) -> DopynionResponseStr:
    print(f"\n🎯 RECEIVED PLAY REQUEST - Game ID: {game_id}")
    print(f"📊 Game state: {len(game.players)} players, finished: {game.finished}")
    
    if should_buy_estate(game):
        print("🛒 DECISION: BUY ESTATE")
        return DopynionResponseStr(game_id=game_id, decision="BUY ESTATE")
    
    print("⏭️ DECISION: END_TURN")
    return DopynionResponseStr(game_id=game_id, decision="END_TURN")


@app.get("/end_game")
def end_game(game_id: GameIdDependency) -> DopynionResponseStr:
    print(f"🏁 GAME ENDED - Game ID: {game_id}")
    return DopynionResponseStr(game_id=game_id, decision="OK")


@app.post("/confirm_discard_card_from_hand")
async def confirm_discard_card_from_hand(
    game_id: GameIdDependency,
    decision_input: CardNameAndHand,
) -> DopynionResponseBool:
    print(f"🗑️ CONFIRM DISCARD - Card: {decision_input.card_name}, Game ID: {game_id}")
    return DopynionResponseBool(game_id=game_id, decision=True)


@app.post("/discard_card_from_hand")
async def discard_card_from_hand(
    game_id: GameIdDependency,
    decision_input: Hand,
) -> DopynionResponseCardName:
    card_to_discard = decision_input.hand[0]
    print(f"🗑️ DISCARD CARD - Discarding: {card_to_discard}, Game ID: {game_id}")
    return DopynionResponseCardName(game_id=game_id, decision=card_to_discard)


@app.post("/confirm_trash_card_from_hand")
async def confirm_trash_card_from_hand(
    game_id: GameIdDependency,
    _decision_input: CardNameAndHand,
) -> DopynionResponseBool:
    return DopynionResponseBool(game_id=game_id, decision=True)


@app.post("/trash_card_from_hand")
async def trash_card_from_hand(
    game_id: GameIdDependency,
    decision_input: Hand,
) -> DopynionResponseCardName:
    return DopynionResponseCardName(game_id=game_id, decision=decision_input.hand[0])


@app.post("/confirm_discard_deck")
async def confirm_discard_deck(
    game_id: GameIdDependency,
) -> DopynionResponseBool:
    return DopynionResponseBool(game_id=game_id, decision=True)


@app.post("/choose_card_to_receive_in_discard")
async def choose_card_to_receive_in_discard(
    game_id: GameIdDependency,
    decision_input: PossibleCards,
) -> DopynionResponseCardName:
    return DopynionResponseCardName(
        game_id=game_id,
        decision=decision_input.possible_cards[0],
    )


@app.post("/choose_card_to_receive_in_deck")
async def choose_card_to_receive_in_deck(
    game_id: GameIdDependency,
    decision_input: PossibleCards,
) -> DopynionResponseCardName:
    return DopynionResponseCardName(
        game_id=game_id,
        decision=decision_input.possible_cards[0],
    )


@app.post("/skip_card_reception_in_hand")
async def skip_card_reception_in_hand(
    game_id: GameIdDependency,
    _decision_input: CardNameAndHand,
) -> DopynionResponseBool:
    return DopynionResponseBool(game_id=game_id, decision=True)


@app.post("/trash_money_card_for_better_money_card")
async def trash_money_card_for_better_money_card(
    game_id: GameIdDependency,
    decision_input: MoneyCardsInHand,
) -> DopynionResponseCardName:
    return DopynionResponseCardName(
        game_id=game_id,
        decision=decision_input.money_in_hand[0],
    )
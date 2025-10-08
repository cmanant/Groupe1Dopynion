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

# Import our strategy modules
from game_state import GameState, get_game_state
from strategy import should_buy_estate

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
# API Routes - Game lifecycle
#####################################################


@app.get("/name")
def name() -> str:
    return "Rhum & Ruin"


@app.get("/start_game")
def start_game(game_id: GameIdDependency) -> DopynionResponseStr:
    print(f"🚀 GAME STARTED - Game ID: {game_id}")
    return DopynionResponseStr(game_id=game_id, decision="OK")


@app.get("/start_turn")
def start_turn(game_id: GameIdDependency) -> DopynionResponseStr:
    game_state = get_game_state(game_id)
    game_state.reset_turn()
    print(f"▶️ TURN STARTED - Game ID: {game_id}")
    return DopynionResponseStr(game_id=game_id, decision="OK")


@app.post("/play")
def play(game: Game, game_id: GameIdDependency) -> DopynionResponseStr:
    game_state = get_game_state(game_id)
    
    print(f"\n🎯 RECEIVED PLAY REQUEST - Game ID: {game_id}")
    print(f"📊 Game state: {len(game.players)} players, finished: {game.finished}")
    print(f"🏪 Purchase status: {game_state.purchases_remaining_this_turn} purchases remaining this turn")
    
    if should_buy_estate(game, game_state):
        game_state.use_purchase()  # Consume one purchase
        print(f"🛒 DECISION: BUY ESTATE")
        return DopynionResponseStr(game_id=game_id, decision="BUY ESTATE")
    
    print("⏭️ DECISION: END_TURN")
    return DopynionResponseStr(game_id=game_id, decision="END_TURN")


@app.get("/end_game")
def end_game(game_id: GameIdDependency) -> DopynionResponseStr:
    print(f"🏁 GAME ENDED - Game ID: {game_id}")
    return DopynionResponseStr(game_id=game_id, decision="OK")


#####################################################
# API Routes - Card interactions
#####################################################


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
import random
from dataclasses import dataclass, field

CARDS = ["J", "Q", "K"]
CARD_RANK = {"J": 0, "Q": 1, "K": 2}
BET_SIZE = 1
ANTE = 1

# Every possible game state maps to (legal actions, who acts next).
# Terminal nodes have no legal actions and no active player.
GAME_TREE = {
    ():              (["k", "b"], "OOP"),
    ("k",):          (["k", "b"], "IP"),
    ("b",):          (["f", "c"], "IP"),
    ("k", "b"):      (["f", "c"], "OOP"),
    # terminal nodes
    ("k", "k"):      ([], None),
    ("k", "b", "f"): ([], None),
    ("k", "b", "c"): ([], None),
    ("b", "f"):      ([], None),
    ("b", "c"):      ([], None),
}


@dataclass
class GameState:
    oop_card: str
    ip_card: str
    history: list[str] = field(default_factory=list)

    @property
    def legal_actions(self) -> list[str]:
        return GAME_TREE[tuple(self.history)][0]

    @property
    def active_player(self) -> str | None:
        return GAME_TREE[tuple(self.history)][1]

    @property
    def is_over(self) -> bool:
        return len(self.legal_actions) == 0

    @property
    def pot(self) -> float:
        return 2 * ANTE + sum(BET_SIZE for a in self.history if a in ("b", "c"))

    @property
    def winnings(self) -> float | None:
        """Net chips from OOP's perspective. None if hand is not over."""
        if not self.is_over:
            return None
        h = tuple(self.history)
        oop_wins = CARD_RANK[self.oop_card] > CARD_RANK[self.ip_card]
        if h == ("k", "k"):
            return ANTE if oop_wins else -ANTE
        if h == ("k", "b", "f"):
            return -ANTE   # OOP folded
        if h == ("b", "f"):
            return ANTE    # IP folded
        # ("k", "b", "c") or ("b", "c") -- bet-call showdown
        prize = ANTE + BET_SIZE
        return prize if oop_wins else -prize


def new_hand() -> GameState:
    """Deal two random cards and return the opening game state."""
    cards = random.sample(CARDS, 2)
    return GameState(oop_card=cards[0], ip_card=cards[1])


def act(state: GameState, action: str) -> GameState:
    """Apply an action and return a new GameState. The original is unchanged."""
    if state.is_over:
        raise ValueError("Hand is already over.")
    if action not in state.legal_actions:
        raise ValueError(f"Illegal action '{action}'. Legal: {state.legal_actions}")
    return GameState(
        oop_card=state.oop_card,
        ip_card=state.ip_card,
        history=state.history + [action],
    )

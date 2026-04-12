# Kuhn Poker CFR

## What is Kuhn Poker?

Kuhn Poker is the simplest non-trivial poker game, designed by Harold Kuhn in 1950. It strips poker down to its bare essentials, making it ideal for studying game theory and algorithms like Counterfactual Regret Minimization (CFR).

### The Deck

The game uses only three cards: **Jack (J)**, **Queen (Q)**, and **King (K)**. The ranking from lowest to highest is J < Q < K.

### Setup

- Two players, each antes **1 chip** into the pot. The pot starts at 2.
- Each player is dealt **one card** face down. The third card is set aside unseen.

### Positions: OOP and IP

**OOP (Out of Position)** acts first on every street. Acting first is a disadvantage because you have to commit to an action before knowing what your opponent will do.

**IP (In Position)** acts second. Acting last is an advantage because you get to see what OOP does before making your decision.

In Kuhn Poker, position never changes. OOP always goes first, IP always goes second.

### Betting Rules

There is one betting round. The only bet size is **1 chip**.

The legal actions are:

| Code | Action | Description |
|------|--------|-------------|
| `k`  | Check  | Pass without betting (only available if no bet has been made yet) |
| `b`  | Bet    | Put 1 chip into the pot |
| `c`  | Call   | Match the opponent's bet of 1 chip |
| `f`  | Fold   | Surrender the hand and forfeit your ante |

### How a Hand Plays Out

OOP acts first and can either **check** or **bet**.

```
OOP checks:
    IP checks  -> Showdown (pot = 2)
    IP bets:
        OOP folds  -> IP wins (pot = 2)
        OOP calls  -> Showdown (pot = 4)

OOP bets:
    IP folds   -> OOP wins (pot = 2)
    IP calls   -> Showdown (pot = 4)
```

There are exactly **5 terminal nodes** (ways a hand can end).

### Showdown

At showdown, the player with the higher card wins the pot. Winnings are tracked from OOP's perspective:

| History     | Result                                  | OOP net |
|-------------|-----------------------------------------|---------|
| `k, k`      | Showdown, pot = 2                       | +1 / -1 |
| `k, b, f`   | OOP folded                              | -1      |
| `k, b, c`   | Showdown, pot = 4                       | +2 / -2 |
| `b, f`      | IP folded                               | +1      |
| `b, c`      | Showdown, pot = 4                       | +2 / -2 |

### Why Kuhn Poker is Useful for CFR

- The full game tree has only **12 non-terminal nodes** (one for each player-card combination at each decision point).
- There are exactly **12 information sets** (6 per player).
- The Nash equilibrium strategy is known analytically, so CFR results can be verified.
- Despite its simplicity, the game captures the core challenge of poker: making decisions under incomplete information.

## Project Structure

```
src/
  models.py   -- Pydantic models: Player, GameState, GameResponse, ActRequest
  game.py     -- KuhnPokerGame engine (new_hand, act)
researcher-api-client/  -- submodule, GTOWizard Researcher API client
```

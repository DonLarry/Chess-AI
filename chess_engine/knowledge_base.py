from random import choice
from typing import List, Optional

from pyswip import Prolog
from chess import Move


class Kb:
  """Knoledge base of the agent."""
  
  def __init__(self):
    """Initialization of the knoledge base."""
    
    # Prolog object
    prolog = Prolog()

    # First move
    prolog.assertz('play([], e2e4)')
    prolog.assertz('play([], d2d4)')

    # -> e4 openings:

    # 1. Sicilian Defense
    prolog.assertz('play([e2e4], c7c5)')

    # 2. French Defense
    prolog.assertz('play([e2e4], e7e6)')

    # 3. Ruy López
    prolog.assertz('play([e2e4], e7e5)')
    prolog.assertz('play([e2e4, e7e5], g1f3)')
    prolog.assertz('play([e2e4, e7e5, g1f3], b8c6)')
    prolog.assertz('play([e2e4, e7e5, g1f3, b8c6], f1b5)')

    # 4. Caro-Kann Defense
    prolog.assertz('play([e2e4], c7c6)')

    # 5. Italian Game
    # Same first 4 moves as in Ruy López
    prolog.assertz('play([e2e4, e7e5, g1f3, b8c6], f1c4)')

    # 6. Sicilian Defense: Closed
    prolog.assertz('play([e2e4, c7c5], b1c3)')

    # -> d4 openings:

    # 1. Queen's Gambit
    prolog.assertz('play([d2d4], d7d5)')
    prolog.assertz('play([d2d4, d7d5], c2c4)')

    # 2. Slav Defense
    # Same first 3 moves as in Queen's Gambit
    prolog.assertz('play([d2d4, d7d5, c2c4], c7c6)')

    # 3. King's Indian Defense
    prolog.assertz('play([d2d4], g8f6)')
    prolog.assertz('play([d2d4, g8f6], c2c4)')
    prolog.assertz('play([d2d4, g8f6, c2c4], g7g6)')
    
    # 4. Nimzo-Indian Defense
    # Same first 3 moves as in King's Indian Defense
    prolog.assertz('play([d2d4, g8f6, c2c4], e7e6)')
    prolog.assertz('play([d2d4, g8f6, c2c4, e7e6], b1c3)')
    prolog.assertz('play([d2d4, g8f6, c2c4, e7e6, b1c3], f8b4)')

    # 5. Queen's Indian Defense
    # Same first 4 moves as in Nimzo-Indian Defense
    prolog.assertz('play([d2d4, g8f6, c2c4, e7e6], g1f3)')
    prolog.assertz('play([d2d4, g8f6, c2c4, e7e6, g1f3], b7b6)')

    # 6. Bogo-Indian Defense
    # Same first 5 moves as in Queen's Indian Defense
    prolog.assertz('play([d2d4, g8f6, c2c4, e7e6, g1f3], f8b4)')

    self.prolog = prolog

  def find_move(self, moves: List[Move]) -> Optional[Move]:
    query = f"play([{', '.join(move.xboard() for move in moves)}], Move)"
    options = [result['Move'] for result in self.prolog.query(query)]
    return Move.from_uci(choice(options)) if options else None

from random import choice
from typing import Tuple, Optional

from pyswip import Prolog
from chess import Move


class Kb:
  """Knoledge base of the agent."""
  
  def __init__(self):
    """Initialization of the knoledge base."""
    
    # Prolog object
    prolog = Prolog()

    # First move
    prolog.assertz("play('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', e2e4)")
    prolog.assertz("play('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', d2d4)")

    # -> e4 openings:

    # 1. Sicilian Defense
    prolog.assertz("play('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1', c7c5)")

    # 2. French Defense
    prolog.assertz("play('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1', e7e6)")

    # 3. Ruy López
    prolog.assertz("play('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1', e7e5)")
    prolog.assertz("play('rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2', g1f3)")
    prolog.assertz("play('rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2', b8c6)")
    prolog.assertz("play('r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3', f1b5)")

    # 4. Caro-Kann Defense
    prolog.assertz("play('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1', c7c6)")

    # 5. Italian Game
    # Same first 4 moves as in Ruy López
    prolog.assertz("play('r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3', f1c4)")

    # 6. Sicilian Defense: Closed
    prolog.assertz("play('rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2', b1c3)")

    # -> d4 openings:

    # 1. Queen's Gambit
    prolog.assertz("play('rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1', d7d5)")
    prolog.assertz("play('rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2', c2c4)")

    # 2. Slav Defense
    # Same first 3 moves as in Queen's Gambit
    prolog.assertz("play('rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq - 0 2', c7c6)")

    # 3. King's Indian Defense
    prolog.assertz("play('rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1', g8f6)")
    prolog.assertz("play('rnbqkb1r/pppppppp/5n2/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 1 2', c2c4)")
    prolog.assertz("play('rnbqkb1r/pppppppp/5n2/8/2PP4/8/PP2PPPP/RNBQKBNR b KQkq - 0 2', g7g6)")
    
    # 4. Nimzo-Indian Defense
    # Same first 3 moves as in King's Indian Defense
    prolog.assertz("play('rnbqkb1r/pppppppp/5n2/8/2PP4/8/PP2PPPP/RNBQKBNR b KQkq - 0 2', e7e6)")
    prolog.assertz("play('rnbqkb1r/pppp1ppp/4pn2/8/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 0 3', b1c3)")
    prolog.assertz("play('rnbqkb1r/pppp1ppp/4pn2/8/2PP4/2N5/PP2PPPP/R1BQKBNR b KQkq - 1 3', f8b4)")

    # 5. Queen's Indian Defense
    # Same first 4 moves as in Nimzo-Indian Defense
    prolog.assertz("play('rnbqkb1r/pppp1ppp/4pn2/8/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 0 3', g1f3)")
    prolog.assertz("play('rnbqkb1r/pppp1ppp/4pn2/8/2PP4/5N2/PP2PPPP/RNBQKB1R b KQkq - 1 3', b7b6)")

    # 6. Bogo-Indian Defense
    # Same first 5 moves as in Queen's Indian Defense
    prolog.assertz("play('rnbqkb1r/pppp1ppp/4pn2/8/2PP4/5N2/PP2PPPP/RNBQKB1R b KQkq - 1 3', f8b4)")

    self.prolog = prolog

  def find_moves(self, position: str) -> Tuple[Move]:
    query = f"play('{position}', Move)"
    return tuple(Move.from_uci(result['Move']) for result in self.prolog.query(query))

  def find_move(self, position: str) -> Optional[Move]:
    options = self.find_moves(position)
    return choice(options) if options else None

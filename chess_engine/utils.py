import random
import time
from typing import List, Tuple, Optional

import chess
import chess.svg
from chess import Move

from .minimax import minimax
from .knowledge_base import Kb


try:
  import IPython
  def display_board(board, *args, size=390, **kwargs):
    """Displays a board drawn as an SVG."""
    svg = chess.svg.board(board, *args, size=size, **kwargs)
    display(IPython.display.HTML(svg))
except ModuleNotFoundError:
  def display_board(board, *args, **kwargs):
    """Displays a board drawn as an ascii representation."""
    del args, kwargs
    print(board)


def find_move(board, depth, white, kb: Optional[Kb]=None, moves: Optional[List[Move]]=None) -> Tuple[bool, int, Move]:
  """Finds the best possible move using a Knowledge Base if possible, or the minimax algorithm otherwise."""

  if moves is not None and kb:
    move = kb.find_move(moves)
    if move:
      return True, 0, move

  evaluation, moves = minimax(board, depth, white=not white)
  move = random.choice(moves)
  return False, evaluation, move


def play(white=bool(random.getrandbits(1)), depth=3):
  """Creates a game simulation with the engine."""

  board = chess.Board()
  kb = Kb()
  moves = []
  turn = 0 if white else 1
  using_kb = True
  display_board(board, flipped=not white)
  
  while True:

    # Checks whether the game has ended and, if it has, shows the cause.
    outcome = board.outcome()
    if outcome:
      print(f'Game over: {outcome.result()} ({outcome.termination.name})')
      break

    # On even turns, the person plays, on odd turns, the agent plays.
    if not turn & 1:
      time.sleep(0.1)
      instruction = input("Enter move: ")
      if instruction in {'quit', 'resign', 'exit'}:
        break
      move = Move.from_uci(instruction)
      if move not in board.legal_moves:
        print("Invalid move.")
        continue
    else:
      print("Computer's Turn")
      in_kb, evaluation, move = find_move(board, depth, white, kb, moves)
      if using_kb and not in_kb:
        using_kb = False
        kb = None
      print(f'Move: {move} (evaluation {evaluation})')

    board.push(move)
    moves.append(move)

    # After any move, the board is displayed.
    display_board(board, flipped=not white)
    turn += 1

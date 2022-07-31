import os
import random
from random import choice
import time
from typing import List, Tuple, Optional

import chess
import chess.svg
from chess import Move

from .minimax import minimax
from .knowledge_base import Kb


try:
  import IPython
  from IPython.display import clear_output
  def display_board(board, *args, size=390, **kwargs):
    """Displays a board drawn as an SVG."""
    svg = chess.svg.board(board, *args, size=size, **kwargs)
    display(IPython.display.HTML(svg))
except ModuleNotFoundError:
  def display_board(board, *args, flipped, **kwargs):
    """Displays a board drawn as an ascii representation."""
    del args, kwargs
    if flipped:
      board = board.transform(chess.flip_vertical)
      board = board.transform(chess.flip_horizontal)
    print(board.unicode(empty_square='.'))
  
  def clear_output():
    os.system('cls||clear')


def find_moves(board, depth, white, kb: Optional[Kb]=None) -> Tuple[bool, Tuple[int, ...], Tuple[Move, ...]]:
  """Finds the best possible moves using a Knowledge Base if possible, or the minimax algorithm otherwise."""

  if kb:
    moves = kb.find_moves(board.fen())
    if moves:
      evaluations = (0,) * len(moves)
      return True, evaluations, moves

  evaluations, moves = zip(*minimax(board, depth, white=not white))
  return False, evaluations, moves


def find_move(board, depth, white, kb: Optional[Kb]=None) -> Tuple[bool, int, Move]:
  """Finds the best possible move using a Knowledge Base if possible, or the minimax algorithm otherwise."""

  using_kb, evaluations, moves = find_moves(board, depth, white, kb)
  
  best_evaluation = evaluations[0]
  size = evaluations.count(best_evaluation)

  return using_kb, best_evaluation, choice(moves[:size])


def play(white=None, depth=3):
  """Creates a game simulation with the engine."""

  if white is None:
    white = bool(random.getrandbits(1))

  board = chess.Board()
  kb = Kb()
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
      clear_output()
    else:
      print("Computer's Turn")
      in_kb, evaluation, move = find_move(board, depth, white, kb)
      if using_kb and not in_kb:
        using_kb = False
        kb = None
      clear_output()
      print(f"Computer's move: {move} (evaluation {evaluation})")

    board.push(move)

    # After any move, the board is displayed.
    display_board(board, flipped=not white)
    turn += 1

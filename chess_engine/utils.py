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


def find_move(board, depth, white, kb: Optional[Kb]=None, estimate_chances = False) -> Tuple[bool, int, Move]:
  """Finds the best possible move using a Knowledge Base if possible, or the minimax algorithm otherwise."""

  using_kb, evaluations, moves = find_moves(board, depth, white, kb)

  # Rival play chances are estimated
  if estimate_chances:
    chances = estimate_play_chances(moves, evaluations, not white)
    if chances:
      print("Possible rival moves:")
      for move, chance in chances:
        print("{}: {} ".format(move, chance))
  
  best_evaluation = evaluations[0]
  size = evaluations.count(best_evaluation)

  return using_kb, best_evaluation, choice(moves[:size])

def estimate_play_chances(moves: Tuple[Move, ...], evaluations: Tuple[int, ...], white: bool = True):
  """ Returns a list of pairs each one consisting of a move and a percent indicating how likely is that
  move to occur based in the current knowledge"""

  # Builds a list of pairs with every possible move and its utility
  possibilities = list(zip(tuple(map(lambda x: x.uci() , moves)), evaluations))

  # Returned list
  results = [] 

  # Accumulated utilities
  total_utility = 0
  
  # Floor value for plays, used to pad values when calculating percents
  plays_floor = evaluations_floor(evaluations, white)

  # for every move higher/smaller than 0, sum all moves, then divide each one by the total sum
  for move, evaluation in possibilities:
    play_selected = lambda x: x >= 0 if white else lambda x: x <= 0
    
    # Harmful plays are not considered
    if not play_selected(evaluation):
      continue
  
    # Padded total utilities are added up
    total_utility += evaluation - plays_floor
    results.append((move, evaluation - plays_floor))

  # When there are no good moves based on current knowledge, an empty list is returned
  if total_utility == 0:
    return []

  print("Total utility: {}".format(total_utility))
  print("Floor: {}".format(plays_floor))
  return [(move, utility) for move, utility in results if utility > 0]


def evaluations_floor(evaluations: Tuple[int, ...], white: bool = True):
  """ Returns the evaluation closest or equal to 0, depending on color """
  return min([x for x in evaluations if x >= 0]) if white else max([x for x in evaluations if x <= 0])
  

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
      try:
        instruction = input("Enter move: ")
        if instruction in {'quit', 'resign', 'exit'}:
          break
        move = Move.from_uci(instruction)
        if move not in board.legal_moves:
          print("Invalid move.")
          continue
        clear_output()
        board.push(move)
      except KeyboardInterrupt:
        break
    else:
      print("Computer's Turn")
      in_kb, evaluation, move = find_move(board, depth, white, kb)
      if using_kb and not in_kb:
        using_kb = False
        kb = None
      # clear_output()
      print(f"Computer's move: {move} (evaluation {evaluation})")
      board.push(move)
      in_kb, evaluation, move = find_move(board, depth, not white, kb, True)
    
    # After any move, the board is displayed.
    display_board(board, flipped=not white)
    turn += 1
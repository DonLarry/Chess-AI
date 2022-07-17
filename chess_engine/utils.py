import chess
import chess.svg
import random
import time
from .minimax import minimax


try:
  from IPython import display
  def display_board(board, *args, size=390, **kwargs):
    """Displays a board drawn as an SVG."""
    svg = chess.svg.board(board, *args, size=size, **kwargs)
    display(IPython.display.HTML(svg))
except ModuleNotFoundError:
  def display_board(board, *args, **kwargs):
    """Displays a board drawn as an ascii representation."""
    print(board)


def play():
  """Creates a game simulation with the engine."""
  
  board = chess.Board()
  turn = 0
  display_board(board)
  
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
      if instruction in {'quit', 'resign'}:
        break
      move = chess.Move.from_uci(instruction)
      if move not in board.legal_moves:
        print("Invalid move.")
        continue
      board.push(move)
    else:
      print("Computers Turn")
      evaluation, moves = minimax(board, 3, white=False)
      move = random.choice(moves)
      print(f'Move: {move} (evaluation {evaluation})')
      board.push(move)

    # After any move, the board is displayed.
    display_board(board)
    turn += 1

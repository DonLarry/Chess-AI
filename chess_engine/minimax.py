from typing import Tuple, List

from chess import Move


# Values are assigned for each piece, either positive or negative depending on the color.
piece_value = {
  None: 0,
  'p': -10,
  'P': 10,
  'n': -30,
  'N': 30,
  'b': -30,
  'B': 30,
  'r': -50,
  'R': 50,
  'q': -90,
  'Q': 90,
  'k': -900,
  'K': 900,
}


def evaluation(board):
  """Board evaluation function."""

  eval = 0

  # For all pieces present on the board, their values are added up, depending on the piece and color.
  # This produces a number that represents the current evaluation of the board used in the minimax.

  for piece in board.piece_map().values():
    eval += piece_value[str(piece)]

  return eval


def _minimax(board, depth=2, alpha=-10000, beta=10000, white=True) -> int:
  """This is a pure minimax recursive algorithm that gives an evaluation for
  a node in the minimax tree."""

  # The possible moves for the current board are obtained.
  legal_moves = [move for move in board.legal_moves]

  # When the target depth is reached, the evaluation function is applied.
  if depth==0 or not legal_moves:
    return evaluation(board)

  # The comparison criterion is chosen according to the color of the pieces.
  if white:
    compare = lambda a, b: a > b
    best_eval = -9999
  else:
    compare = lambda a, b: a < b
    best_eval = 9999

  # The algorithm is run with all the possible movements.

  for move in board.legal_moves:
    # A move is simulated on the board to calculate what benefit it brings.
    board.push(move)
    current_eval = _minimax(board, depth-1, alpha, beta, not white)

    # The board is returned to the previous state, since it was only a simulation.
    board.pop()

    # The benefit of the movement is compared with the best one found so far, in the hope of updating the latter.
    if compare(current_eval, best_eval):
      best_eval = current_eval

    # Alpha-beta pruning.
    alpha = max(alpha, current_eval)
    if beta <= alpha:
      break

  # The evaluation for the current node is the best one found.
  return best_eval


def minimax(board, depth=3, alpha=-10000, beta=10000, white=True) -> List[Tuple[int, Move]]:
  """Custom minimax algorithm. Returns a list of all the possible moves represented
  as pairs (evaluation, move)."""

  # The possible moves for the current board are obtained.
  legal_moves = [move for move in board.legal_moves]

  # If there's no legal moves, either the position is checkmate, or stalemate
  if not legal_moves:
    return [(evaluation(board), None)]

  evaluations = []

  # The algorithm is run with all the possible movements.

  for move in board.legal_moves:
    # A move is simulated on the board to calculate what benefit it brings.
    board.push(move)
    current_eval = _minimax(board, depth-1, alpha, beta, not white)
    evaluations.append(current_eval)

    # The board is returned to the previous state, since it was only a simulation.
    board.pop()

    # Alpha-beta pruning.
    alpha = max(alpha, current_eval)
    if beta <= alpha:
      break

  evaluations_and_moves = zip(evaluations, legal_moves)
  return sorted(evaluations_and_moves, reverse=white, key=lambda t: t[0])

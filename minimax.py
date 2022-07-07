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
  eval = 0
  for piece in board.piece_map().values():
    eval += piece_value[str(piece)]
  return eval


def minimax(board, depth=3, alpha=-10000, beta=10000, white=True):
  legal_moves = [move for move in board.legal_moves]

  if depth==0 or not legal_moves:
    return evaluation(board), []

  best_moves = []

  if white:
    compare = lambda a, b: a > b
    best_eval = -9999
  else:
    compare = lambda a, b: a < b
    best_eval = 9999

  for move in board.legal_moves:
    board.push(move)
    current_eval, _ = minimax(board, depth-1, alpha, beta, not white)
    board.pop()

    if compare(current_eval, best_eval):
      best_eval = current_eval
      best_moves = [move]
    elif current_eval == best_eval:
      best_moves.append(move)

    alpha = max(alpha, current_eval)
    if beta <= alpha:
      break
  return best_eval, best_moves

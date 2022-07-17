# Se asignan valores para cada pieza, ya sea positivo o negativo según el color
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
  """ Función de evaluación del tablero """
  eval = 0
  # Para todas las piezas presentes en el tablero se suman sus valores, dependiendo de la pieza y el color
  # esto produce un número que representa la evaluación actual del tablero usada en el minimax.
  for piece in board.piece_map().values():
    eval += piece_value[str(piece)]
  return eval


def minimax(board, depth=3, alpha=-10000, beta=10000, white=True):
  """ Implementación recursiva del algoritmo minimax """
  # Se obtienen los movimientos posibles para el tablero actual
  legal_moves = [move for move in board.legal_moves]

  # Al llegar a la profundidad deseada, se aplica la función de evaluación
  if depth==0 or not legal_moves:
    return evaluation(board), []

  best_moves = []

  # Se elige el criterio de comparación según el color de las piezas
  if white:
    compare = lambda a, b: a > b
    best_eval = -9999
  else:
    compare = lambda a, b: a < b
    best_eval = 9999

  # Se corre el algoritmo con todos los movimientos posibles

  for move in board.legal_moves:
    # Se simula un movimiento en el tablero para calcular que beneficio aporta
    board.push(move)
    current_eval, _ = minimax(board, depth-1, alpha, beta, not white)
    # Se regresa el tablero al estado anterior, puesto que solo era una simulación
    board.pop()

    # Se compara el beneficio del movimiento con el mejor hallado hasta el momento, con la esperanza de actualizar este último
    if compare(current_eval, best_eval):
      best_eval = current_eval
      best_moves = [move]
    elif current_eval == best_eval:
      best_moves.append(move)

    # Aplicación de la poda alfa beta
    alpha = max(alpha, current_eval)
    if beta <= alpha:
      break
  return best_eval, best_moves

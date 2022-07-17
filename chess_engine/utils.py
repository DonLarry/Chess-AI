import chess
import chess.svg
import random
import IPython
from .minimax import minimax

# Funcion de utilidad para mostrar un tablero dibujado como un SVG
def display_board(board, *args, size=390, **kwargs):
  svg = chess.svg.board(board, *args, size=size, **kwargs)
  display(IPython.display.HTML(svg))


# Loop de juego principal
def play():
  board = chess.Board()
  turn = 0
  display_board(board)
  while True:
    # Se verifica si la partida ha terminado y en caso afirmativo muestra la causa
    outcome = board.outcome()
    if outcome:
      print(f'Game over: {outcome.result()} ({outcome.termination.name})')
      break
    # En los turnos pares, juega la persona, en los impares, juega el agente
    if not turn & 1:
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
    display_board(board)
    turn += 1

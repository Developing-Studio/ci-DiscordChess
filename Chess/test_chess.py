from Chess.chess import *
from time import time

letters = "pbnrqkPBNRQK-"
symbols = "♟♝♞♜♛♚♙♗♘♖♕♔ "


def print_fen(fen):
    for line in fen.split(" ")[0].split("/"):
        for item in numbers_to_dashes(line):
            print(symbols[letters.index(item)] + " ", end="")
        print()


g = ChessGame()
print(g.get_figure_possible_moves_rows_in_line("Pe2", "3"))

while True:
    print(g.get_all_possible_moves())
    print_fen(g.game)
    g.move(input("Move >> "))

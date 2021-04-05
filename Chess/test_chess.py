from Chess.chess import *
from time import time

letters = "pbnrqkPBNRQK-"
symbols = "♟♝♞♜♛♚♙♗♘♖♕♔ "


def print_fen(fen):
    for fenline in fen.split(" ")[0].split("/"):
        for item in numbers_to_dashes(fenline):
            print(symbols[letters.index(item)] + " ", end="")
        print()


g = ChessGame()
g.game = "8/1k4P1/8/8/8/8/8/1K6 w - - 0 1"
while True:
    print_fen(g.game)
    print(g.log)
    print(g.get_game_is_over_messsage())
    letter = input(g.get_remaining_movable_letters())
    row = input(g.get_rows_containing_movable_letter(letter))
    line = input(g.get_lines_containing_movable_letter_in_row(letter, row))
    figure = letter + row + line
    move_row = input(g.get_figure_possible_moves_rows(figure))
    move_line = input(g.get_figure_possible_moves_lines_in_row(figure, move_row))
    option = ""
    if len(g.get_figure_transormation_options(figure)) > 0:
        option = input(g.get_figure_transormation_options(figure))
    g.move(figure + move_row + move_line + option)

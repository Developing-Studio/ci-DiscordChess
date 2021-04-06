from Chess.chess import *
from time import time


def performence_test(function, *args):
    return
    t = time()
    function(*args)
    print(str(function.__name__) + ": " + str("{:f}".format(round(time() - t, 5))) + " Sekunden")


performence_test(letter_to_name, "A")
performence_test(numbers_to_dashes, "8")
performence_test(dashes_to_numbers, "-"*8)
performence_test(castle_bools_to_letters, True, True, True, True)
performence_test(increase_position, "a1")
performence_test(relative_position, "a1", 1, 1)
p = ChessGame()
performence_test(p.get_position, "a1")
performence_test(p.set_position, "a1", "-")
performence_test(p.get_turn)
performence_test(p.get_turn_name)
performence_test(p.set_turn, "w")
performence_test(p.get_white_can_castle_kingside)
performence_test(p.set_white_can_castle_kingside, True)
performence_test(p.get_white_can_castle_queenside)
performence_test(p.set_white_can_castle_queenside, True)
performence_test(p.get_black_can_castle_kingside)
performence_test(p.set_black_can_castle_kingside, True)
performence_test(p.get_black_can_castle_queenside)
performence_test(p.set_black_can_castle_queenside, True)
performence_test(p.get_current_can_castle_kingside)
performence_test(p.set_current_can_castle_kingside, True)
performence_test(p.get_current_can_castle_queenside)
performence_test(p.set_current_can_castle_queenside, True)
performence_test(p.get_en_passant)
performence_test(p.set_en_passant, "-")
performence_test(p.get_fifty_moves)
performence_test(p.set_fifty_moves, 0)
performence_test(p.increase_fifty_moves)
performence_test(p.get_move_number)
performence_test(p.set_move_number, 0)
performence_test(p.increase_move_number)
performence_test(p.get_is_in_check, "w")
performence_test(p.get_white_is_in_check)
performence_test(p.get_black_is_in_check)
performence_test(p.get_current_is_in_check)
performence_test(p.get_current_would_be_in_check, "Pe2e4")
performence_test(p.get_remaining_figures, white_pieces + black_pieces)
performence_test(p.get_remaining_movable_figures)
performence_test(p.get_remaining_letters)
performence_test(p.get_remaining_movable_letters)
performence_test(p.get_rows_containing_letter, "K")
performence_test(p.get_rows_containing_movable_letter, "K")
performence_test(p.get_lines_containing_letter, "K")
performence_test(p.get_lines_containing_movable_letter, "K")
performence_test(p.get_rows_containing_letter_in_line, "K", "1")
performence_test(p.get_rows_containing_movable_letter_in_line, "K", "1")
performence_test(p.get_lines_containing_letter_in_row, "K", "a")
performence_test(p.get_lines_containing_movable_letter_in_row, "K", "a")
performence_test(p.get_figure_possible_moves, "Pe2")
performence_test(p.get_figure_possible_moves_rows, "Pe2")
performence_test(p.get_figure_possible_moves_lines, "Pe2")
performence_test(p.get_figure_possible_moves_rows_in_line, "Pe2", "1")
performence_test(p.get_figure_possible_moves_lines_in_row, "Pe2", "a")
performence_test(p.get_all_possible_moves)
performence_test(p.get_figure_transormation_options, "Pe2")
performence_test(p.move, "Pe2e4")
performence_test(p.get_game_is_over)
performence_test(p.get_game_is_over_messsage)
print()


letters = "pbnrqkPBNRQK-"
symbols = "♟♝♞♜♛♚♙♗♘♖♕♔ "


def print_fen(fen):
    for fenline in fen.split(" ")[0].split("/"):
        for fenline_item in numbers_to_dashes(fenline):
            print(symbols[letters.index(fenline_item)] + " ", end="")
        print()


g = ChessGame()
g.game = "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1"
# g.game = "k7/pp6/3Q4/8/8/8/8/3K4 w - - 0 1"
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
    print(figure + move_row + move_line + option)

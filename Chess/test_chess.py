from Chess.chess import *

letters = "pbnrqkPBNRQK-"
symbols = "♟♝♞♜♛♚♙♗♘♖♕♔ "


def print_fen(fen):
    for line in fen.split(" ")[0].split("/"):
        for item in numbers_to_dashes(line):
            print(symbols[letters.index(item)] + " ", end="")
        print()


g = ChessGame()
print(g.get_position("e1"))
print_fen(g.game)
print_fen("r1bqkb1r/pp2pppp/2p2n2/2nP4/2P1B3/8/PP1P1PPP/RNBQK1NR w KQkq - 5 6")

print()
print(numbers_to_dashes("2p2n2"))
print(dashes_to_numbers("----p-Q-"))

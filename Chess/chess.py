
class ChessGame:
    white_pieces = "PBNRQK"
    black_pieces = "pbnrqk"
    line_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7}

    game = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def field(self, position: str):
        return self.game.split(" ")[0].split("/")[self.line_index[position[1]]][self.line_index[position[0]]]

    def turn(self):
        return self.game.split(" ")[1]

    def white_can_castle_kingside(self):
        if self.game.split(" ")[2].count("K") > 0:
            return True
        else:
            return False

    def white_can_castle_queenside(self):
        if self.game.split(" ")[2].count("Q") > 0:
            return True
        else:
            return False

    def black_can_castle_kingside(self):
        if self.game.split(" ")[2].count("k") > 0:
            return True
        else:
            return False

    def black_can_castle_queenside(self):
        if self.game.split(" ")[2].count("q") > 0:
            return True
        else:
            return False

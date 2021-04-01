
class ChessGame:
    white_pieces = "PBNRQK"
    black_pieces = "pbnrqk"
    line_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}

    game = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def get_position(self, position: str):
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

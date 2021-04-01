
class ChessGame:
    game = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

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

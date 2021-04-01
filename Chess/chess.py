class ChessGame:
    white_pieces = ["P", "B", "N", "R", "Q", "K"]
    black_pieces = ["p", "b", "n", "r", "q", "k"]
    numbers = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8}
    line_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}

    game = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def numbers_to_dashes(self, fen_line: str):
        output = ""
        for item in list(fen_line):
            if item in self.numbers.keys():
                output += "-" * self.numbers[item]
            else:
                output += item
        return output

    def get_position(self, position: str):
        return self.numbers_to_dashes(self.game.split(" ")[0].split("/")[self.line_index[position[1]]])[self.line_index[position[0]]]

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

    def en_passant(self):
        return self.game.split(" ")[3]

    def moves_since_pawn_move(self):
        return self.game.split(" ")[4]

    def move_number(self):
        return self.game.split(" ")[5]

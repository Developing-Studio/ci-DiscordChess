white_pieces = "PBNRQK"
black_pieces = "pbnrqk"
numbers = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8}
line_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}


def numbers_to_dashes(fen_line: str) -> str:
    output = ""
    for item in list(fen_line):
        if item in numbers.keys():
            output += "-" * numbers[item]
        else:
            output += item
    return output


class ChessGame:
    game = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def get_position(self, position: str) -> str:
        return numbers_to_dashes(self.game.split(" ")[0].split("/")[line_index[position[1]]])[line_index[position[0]]]

    def get_turn(self) -> str:
        return self.game.split(" ")[1]

    def set_turn(self, turn: str):
        if turn != self.get_turn():
            self.game.replace(" " + self.get_turn() + " ", " " + turn + " ", 1)

    def white_can_castle_kingside(self) -> bool:
        if self.game.split(" ")[2].count("K") > 0:
            return True
        else:
            return False

    def white_can_castle_queenside(self) -> bool:
        if self.game.split(" ")[2].count("Q") > 0:
            return True
        else:
            return False

    def black_can_castle_kingside(self) -> bool:
        if self.game.split(" ")[2].count("k") > 0:
            return True
        else:
            return False

    def black_can_castle_queenside(self) -> bool:
        if self.game.split(" ")[2].count("q") > 0:
            return True
        else:
            return False

    def en_passant(self) -> str:
        return self.game.split(" ")[3]

    def moves_since_pawn_move(self) -> int:
        return int(self.game.split(" ")[4])

    def move_number(self) -> int:
        return int(self.game.split(" ")[5])

    def possible_moves(self) -> list:
        pass

    def move(self, move: str):
        if move in self.possible_moves():
            #

            if self.get_turn() == "w":
                self.set_turn("b")
            else:
                self.set_turn("w")

white_pieces = "PBNRQK"
black_pieces = "pbnrqk"
numbers = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8}
line_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}


def numbers_to_dashes(fen_line: str) -> str:
    output = ""
    for item in fen_line:
        if item in numbers.keys():
            output += "-" * numbers[item]
        else:
            output += item
    return output


def dashes_to_numbers(fen_line: str) -> str:
    output = ""
    number = 0
    for item in fen_line:
        if item == "-":
            number += 1
        else:
            if number == 0:
                output += item
            else:
                output += str(number)
                output += item
                number = 0
    if number != 0:
        output += str(number)
    return output


def castle_bools_to_letters(wk: bool, wq: bool, bk: bool, bq: bool) -> str:
    output = ""
    if wk:
        output += "K"
    if wq:
        output += "Q"
    if bk:
        output += "k"
    if bq:
        output += "q"
    if output == "":
        output = "-"
    return output


class ChessGame:
    game = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def get_position(self, position: str) -> str:
        return numbers_to_dashes(self.game.split(" ")[0].split("/")[line_index[position[1]]])[line_index[position[0]]]

    def set_position(self, position: str, to: str):
        new = self.game.split(" ")
        board = new[0].split("/")
        line = list(board[line_index[position[1]]])
        line[line_index[position[0]]] = to
        board[line_index[position[1]]] = "".join(line)
        new[0] = " ".join(board)
        self.game = " ".join(new)

    def get_turn(self) -> str:
        return self.game.split(" ")[1]

    def set_turn(self, to: str):
        new = self.game.split(" ")
        new[1] = to
        self.game = " ".join(new)

    def get_white_can_castle_kingside(self) -> bool:
        if self.game.split(" ")[2].count("K") > 0:
            return True
        else:
            return False

    def set_white_can_castle_kingside(self, to: bool):
        new = self.game.split(" ")
        new[2] = castle_bools_to_letters(to, self.get_white_can_castle_queenside(), self.get_black_can_castle_kingside(), self.get_black_can_castle_queenside())
        self.game = " ".join(new)

    def get_white_can_castle_queenside(self) -> bool:
        if self.game.split(" ")[2].count("Q") > 0:
            return True
        else:
            return False

    def set_white_can_castle_queenside(self, to: bool):
        new = self.game.split(" ")
        new[2] = castle_bools_to_letters(self.get_white_can_castle_kingside(), to, self.get_black_can_castle_kingside(), self.get_black_can_castle_queenside())
        self.game = " ".join(new)

    def get_black_can_castle_kingside(self) -> bool:
        if self.game.split(" ")[2].count("k") > 0:
            return True
        else:
            return False

    def set_black_can_castle_kingside(self, to: bool):
        new = self.game.split(" ")
        new[2] = castle_bools_to_letters(self.get_white_can_castle_kingside(), self.get_white_can_castle_queenside(), to, self.get_black_can_castle_queenside())
        self.game = " ".join(new)

    def get_black_can_castle_queenside(self) -> bool:
        if self.game.split(" ")[2].count("q") > 0:
            return True
        else:
            return False

    def set_black_can_castle_queenside(self, to: bool):
        new = self.game.split(" ")
        new[2] = castle_bools_to_letters(self.get_white_can_castle_kingside(), self.get_white_can_castle_queenside(), self.get_black_can_castle_kingside(), to)
        self.game = " ".join(new)

    def get_en_passant(self) -> str:
        return self.game.split(" ")[3]

    def set_en_passant(self, to: str):
        new = self.game.split(" ")
        new[3] = to
        self.game = " ".join(new)

    def get_moves_since_pawn_move(self) -> int:
        return int(self.game.split(" ")[4])

    def set_moves_since_pawn_move(self, to: int):
        new = self.game.split(" ")
        new[4] = str(to)
        self.game = " ".join(new)

    def increase_moves_since_pawn_move(self, by: int = 1):
        self.set_moves_since_pawn_move(self.get_moves_since_pawn_move() + by)

    def get_move_number(self) -> int:
        return int(self.game.split(" ")[5])

    def set_move_number(self, to: int):
        new = self.game.split(" ")
        new[5] = str(to)
        self.game = " ".join(new)

    def increase_move_number(self, by: int = 1):
        self.set_move_number(self.get_move_number() + by)

    def get_possible_moves(self) -> list:
        pass

    def move(self, move: str):
        if move in self.get_possible_moves():
            #

            if self.get_turn() == "w":
                self.set_turn("b")
            else:
                self.set_turn("w")

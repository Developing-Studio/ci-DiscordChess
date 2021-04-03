white_pieces = "PBNRQK"
black_pieces = "pbnrqk"
numbers = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8}
line_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
next_line = {"a": "b", "b": "c", "c": "d", "d": "e", "e": "f", "f": "g", "g": "h", "h": "a"}
previous_line = {"a": "h", "b": "a", "c": "b", "d": "c", "e": "d", "f": "e", "g": "f", "h": "g"}


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


def increase_position(position: str, by: int = 1) -> str:
    for _ in range(by):
        if position[1] == "8":
            position = next_line[position[0]] + "1"
        else:
            position = position[0] + str(int(position[1]) + 1)
    return position


def relative_position(position: str, relative_x: int, relative_y: int) -> str:
    if (0 <= (line_index[position[0]] + relative_x) <= 7) and (0 <= (7 - line_index[position[1]] + relative_y) <= 7):
        for _ in range(abs(relative_x)):
            if relative_x > 0:
                position = next_line[position[0]] + position[1]
            else:
                position = previous_line[position[0]] + position[1]
        position = position[0] + str(int(position[1]) + relative_y)
        return position
    else:
        return "-"


class ChessGame:
    game = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def get_position(self, position: str) -> str:
        return numbers_to_dashes(self.game.split(" ")[0].split("/")[line_index[position[1]]])[line_index[position[0]]]

    def set_position(self, position: str, to: str):
        new = self.game.split(" ")
        board = new[0].split("/")
        line = list(numbers_to_dashes(board[line_index[position[1]]]))
        line[line_index[position[0]]] = to
        board[line_index[position[1]]] = "".join(line)
        new[0] = "/".join(board)
        self.game = " ".join(new)

    def get_turn(self) -> str:
        return self.game.split(" ")[1]

    def get_turn_name(self) -> str:
        return "White" if self.get_turn() == "w" else "Black"

    def set_turn(self, to: str):
        new = self.game.split(" ")
        new[1] = to
        self.game = " ".join(new)

    def get_white_can_castle_kingside(self) -> bool:
        return True if self.game.split(" ")[2].count("K") > 0 else False

    def set_white_can_castle_kingside(self, to: bool):
        new = self.game.split(" ")
        new[2] = castle_bools_to_letters(to, self.get_white_can_castle_queenside(), self.get_black_can_castle_kingside(), self.get_black_can_castle_queenside())
        self.game = " ".join(new)

    def get_white_can_castle_queenside(self) -> bool:
        return True if self.game.split(" ")[2].count("Q") > 0 else False

    def set_white_can_castle_queenside(self, to: bool):
        new = self.game.split(" ")
        new[2] = castle_bools_to_letters(self.get_white_can_castle_kingside(), to, self.get_black_can_castle_kingside(), self.get_black_can_castle_queenside())
        self.game = " ".join(new)

    def get_black_can_castle_kingside(self) -> bool:
        return True if self.game.split(" ")[2].count("k") > 0 else False

    def set_black_can_castle_kingside(self, to: bool):
        new = self.game.split(" ")
        new[2] = castle_bools_to_letters(self.get_white_can_castle_kingside(), self.get_white_can_castle_queenside(), to, self.get_black_can_castle_queenside())
        self.game = " ".join(new)

    def get_black_can_castle_queenside(self) -> bool:
        return True if self.game.split(" ")[2].count("q") > 0 else False

    def set_black_can_castle_queenside(self, to: bool):
        new = self.game.split(" ")
        new[2] = castle_bools_to_letters(self.get_white_can_castle_kingside(), self.get_white_can_castle_queenside(), self.get_black_can_castle_kingside(), to)
        self.game = " ".join(new)

    def get_current_can_castle_kingside(self) -> bool:
        return self.get_white_can_castle_kingside() if self.get_turn() == "w" else self.get_black_can_castle_kingside()

    def set_current_can_castle_kingside(self, to: bool):
        self.set_white_can_castle_kingside(to) if self.get_turn() == "w" else self.set_black_can_castle_kingside(to)

    def get_current_can_castle_queenside(self) -> bool:
        return self.get_white_can_castle_queenside() if self.get_turn() == "w" else self.get_black_can_castle_queenside()

    def set_current_can_castle_queenside(self, to: bool):
        self.set_white_can_castle_queenside(to) if self.get_turn() == "w" else self.set_black_can_castle_queenside(to)

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

    def get_remaining_figures(self) -> list:
        pieces = white_pieces if self.get_turn() == "w" else black_pieces
        remaining_figures = []
        position = "a1"
        for _ in range(64):
            if self.get_position(position) in pieces:
                remaining_figures.append(self.get_position(position) + position)
            position = increase_position(position)
        return remaining_figures

    def get_remaining_movable_figures(self) -> list:
        return list(dict.fromkeys(map(lambda x: x[:3], self.get_all_possible_moves())))

    def get_remaining_letters(self) -> list:
        return list(dict.fromkeys(map(lambda x: x[0], self.get_remaining_figures())))

    def get_remaining_movable_letters(self) -> list:
        return list(dict.fromkeys(map(lambda x: x[0], self.get_remaining_movable_figures())))

    def get_rows_containing_figure(self, figure: str) -> list:
        rows = []
        position = "a1"
        for _ in range(64):
            if self.get_position(position)[0] == figure:
                rows.append(position[0])
            position = increase_position(position)
        return list(dict.fromkeys(rows))

    def get_lines_containing_figure(self, figure: str) -> list:
        lines = []
        position = "a1"
        for _ in range(64):
            if self.get_position(position)[0] == figure:
                lines.append(position[1])
            position = increase_position(position)
        return list(dict.fromkeys(lines))

    def get_rows_containing_figure_in_line(self, figure: str, line: str) -> list:
        rows = []
        position = "a" + line
        for _ in range(8):
            if self.get_position(position)[0] == figure:
                rows.append(position[0])
            position = increase_position(position, by=8)
        return list(dict.fromkeys(rows))

    def get_lines_containing_figure_in_row(self, figure: str, row: str) -> list:
        lines = []
        position = row + "1"
        for _ in range(8):
            if self.get_position(position)[0] == figure:
                lines.append(position[1])
            position = increase_position(position, by=1)
        return list(dict.fromkeys(lines))

    def get_figure_possible_moves(self, figure: str):
        possible_moves = []
        opponent_pieces = black_pieces if self.get_turn() == "w" else white_pieces

        def check(rx: int, ry: int, allowed: str):
            rposition = relative_position(figure[1:], rx, ry)
            if (rposition != "-") and (self.get_position(rposition) in allowed):
                possible_moves.append(figure[0] + figure[1:] + rposition)
                return True
            else:
                return False

        if figure[0] == "P":
            check(0, 1, "-")
            check(1, 1, opponent_pieces)
            check(-1, 1, opponent_pieces)
        elif figure[0] == "p":
            check(0, -1, "-")
            check(1, -1, opponent_pieces)
            check(-1, -1, opponent_pieces)
        elif figure[0].lower() == "b":
            for item in range(1, 9):
                if not check(item, item, "-" + opponent_pieces):
                    break
            for item in range(1, 9):
                if not check(-item, item, "-" + opponent_pieces):
                    break
            for item in range(1, 9):
                if not check(item, -item, "-" + opponent_pieces):
                    break
            for item in range(1, 9):
                if not check(-item, -item, "-" + opponent_pieces):
                    break
        elif figure[0].lower() == "n":
            check(2, 1, "-" + opponent_pieces)
            check(2, -1, "-" + opponent_pieces)
            check(-2, 1, "-" + opponent_pieces)
            check(-2, -1, "-" + opponent_pieces)
            check(1, 2, "-" + opponent_pieces)
            check(-1, 2, "-" + opponent_pieces)
            check(1, -2, "-" + opponent_pieces)
            check(-1, -2, "-" + opponent_pieces)
        elif figure[0].lower() == "r":
            for item in range(1, 9):
                if not check(item, 0, "-" + opponent_pieces):
                    break
            for item in range(1, 9):
                if not check(-item, 0, "-" + opponent_pieces):
                    break
            for item in range(1, 9):
                if not check(0, item, "-" + opponent_pieces):
                    break
            for item in range(1, 9):
                if not check(0, -item, "-" + opponent_pieces):
                    break
        elif figure[0].lower() == "q":
            for item in range(1, 9):
                if not check(item, item, "-" + opponent_pieces):
                    break
            for item in range(1, 9):
                if not check(-item, item, "-" + opponent_pieces):
                    break
            for item in range(1, 9):
                if not check(item, -item, "-" + opponent_pieces):
                    break
            for item in range(1, 9):
                if not check(-item, -item, "-" + opponent_pieces):
                    break
            for item in range(1, 9):
                if not check(item, 0, "-" + opponent_pieces):
                    break
            for item in range(1, 9):
                if not check(-item, 0, "-" + opponent_pieces):
                    break
            for item in range(1, 9):
                if not check(0, item, "-" + opponent_pieces):
                    break
            for item in range(1, 9):
                if not check(0, -item, "-" + opponent_pieces):
                    break
        elif figure[0].lower() == "k":
            check(1, 1, "-" + opponent_pieces)
            check(0, 1, "-" + opponent_pieces)
            check(-1, 1, "-" + opponent_pieces)
            check(1, 0, "-" + opponent_pieces)
            check(-1, 0, "-" + opponent_pieces)
            check(1, -1, "-" + opponent_pieces)
            check(0, -1, "-" + opponent_pieces)
            check(-1, -1, "-" + opponent_pieces)
        return possible_moves

    def get_figure_possible_moves_rows(self, figure: str) -> list:
        return list(dict.fromkeys(map(lambda x: x[3], self.get_figure_possible_moves(figure))))

    def get_figure_possible_moves_lines(self, figure: str) -> list:
        return list(dict.fromkeys(map(lambda x: x[4], self.get_figure_possible_moves(figure))))

    def get_figure_possible_moves_rows_in_line(self, figure: str, line: str) -> list:
        return list(dict.fromkeys(map(lambda x: x[3], filter(lambda x: x[4] == line, self.get_figure_possible_moves(figure)))))

    def get_figure_possible_moves_lines_in_row(self, figure: str, row: str) -> list:
        return list(dict.fromkeys(map(lambda x: x[4], filter(lambda x: x[3] == row, self.get_figure_possible_moves(figure)))))

    def get_all_possible_moves(self) -> list:
        all_possible_moves = []
        for item in self.get_remaining_figures():
            all_possible_moves += self.get_figure_possible_moves(item)
        return all_possible_moves

    def move(self, move: str):
        if move in self.get_all_possible_moves():
            self.set_position(move[1:3], "-")
            self.set_position(move[3:], move[0])
            if move[0].lower() == "p":
                self.set_moves_since_pawn_move(0)
            else:
                self.increase_moves_since_pawn_move()

            if self.get_turn() == "w":
                self.set_turn("b")
            else:
                self.set_turn("w")
                self.increase_move_number()

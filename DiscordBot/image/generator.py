from PIL import Image

from Chess.chess import letter_to_name, numbers_to_dashes


class ChessBoard:
    def __init__(self, fen: str, width: int = 75 * 8):
        self.width = self.height = width
        self.fen = fen
        self.image = Image.open("./board/board.png")
        self.draw_fen(fen)

    def draw_letter(self, letter: str, x: int, y: int):
        path = "./board/figures/" + "_".join(letter_to_name(letter).lower().split()[::-1]) + ".png"
        x *= self.width // 8
        y *= self.height // 8
        img: Image.Image = Image.open(path)
        self.image.paste(img, box=(x, y), mask=img.split()[1])
        return self

    def draw_fen(self, fen_str: str):
        x: int = 0
        y: int = 0
        for row in fen_str.split()[0].split("/"):
            row = numbers_to_dashes(row)
            for letter in row:
                if letter != "-":
                    self.draw_letter(letter, x, y)
                x += 1
            x = 0
            y += 1
        return self


def create_embed_image(fen: str, gameid):
    chessboard: Image.Image = ChessBoard(fen).image
    chessboard.save("./dist/" + str(gameid) + ".png")

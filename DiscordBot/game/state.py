from enum import Enum

from discord import Reaction

from Chess.chess import letter_to_name
from DiscordBot.game.game import Game
from DiscordBot.utils import figure_to_emoji, letter_to_emoji


class GameState(Enum):
    SELECT_FIGURE_TYPE = 0
    SELECT_FIGURE_POS_ROW = 1
    SELECT_FIGURE_POS_COL = 2

    SELECT_MOVE_POS_ROW = 3
    SELECT_MOVE_POS_COL = 4

    SELECT_PAWN_TRANSFORM = 5
    EXEC_MOVE = 1000


class Field:
    def __init__(self, name: str, value: str, inline: bool = False):
        self.name = name
        self.value = value
        self.inline = inline


class State:
    def __init__(self, name: GameState, game: Game):
        self.name = name
        self.game = game

        state_cls = self
        game.state = state_cls

    def next(self, *args, **kwargs) -> "State":
        pass

    def get_embed_field(self) -> Field:
        pass

    def possible_emotes(self) -> list:
        pass

    def on_react(self, reaction: Reaction):
        pass


class SelectFigureState(State):
    def __init__(self, game: Game):
        super().__init__(GameState.SELECT_FIGURE_TYPE, game)

    def next(self, selected_letter: str) -> State:
        return SelectFigureRow(self.game, selected_letter)

    def get_embed_field(self) -> Field:
        return Field(
            name="** **",
            value="Please select a figure to move"
        )

    def possible_emotes(self) -> list:
        movable_letters = self.game.chess.get_remaining_movable_letters()
        return [figure_to_emoji(i, 3) for i in movable_letters]

    def on_react(self, reaction: Reaction):
        self.next(reaction.emoji.name[0])


class SelectFigureRow(State):
    def __init__(self, game: Game, selected_letter: str):
        super().__init__(GameState.SELECT_FIGURE_POS_ROW, game)
        self.selected_letter = selected_letter
        self.rows = self.game.chess.get_rows_containing_movable_letter(selected_letter)

        if len(self.rows) == 1:
            self.next(self.rows[0])

    def next(self, selected_row: str) -> "State":
        return SelectFigureColumn(self.game, self.selected_letter, selected_row)

    def get_embed_field(self) -> Field:
        return Field(
            name="** **",
            value="Please select the column, where your **" + letter_to_name(self.selected_letter) + "** is located"
        )

    def possible_emotes(self) -> list:
        return [letter_to_emoji(i) for i in self.rows]

    def on_react(self, reaction: Reaction):
        em = reaction.emoji
        self.next(
            "a" if em == "🇦" else "b" if em == "🇧" else "c" if em == "🇨" else "d" if em == "🇩" else "e" if em == "🇪" else "f" if em == "🇫" else "g" if em == "🇬" else "h")


class SelectFigureColumn(State):
    def __init__(self, game: Game, selected_letter: str, selected_row: str):
        super().__init__(GameState.SELECT_FIGURE_POS_COL, game)
        self.selected_letter = selected_letter
        self.selected_row = selected_row

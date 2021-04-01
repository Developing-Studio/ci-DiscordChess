from typing import List

from discord import Member

from Chess.chess import ChessGame


class Game:
    def __init__(self, member: Member, name: str):
        self.member = member
        self.name = name
        self.chess = ChessGame()
        self.url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    @staticmethod
    def create(member: Member, name: str) -> "Game":
        game: Game = Game(member, name)
        if member.id not in games.keys():
            games[member.id] = []

        games[member.id].append(game)
        return game


games: dict = {}


def get_games(member: Member) -> List[Game]:
    return games[member.id] if member.id in games.keys() else []


def get_game(member: Member, name: str) -> Game:
    gms: List[Game] = get_games(member)
    l = [i for i in gms if i.name == name]
    return l[0] if l else None

from discord.ext.commands import AutoShardedBot


def figure_to_emoji(figure: str):
    return {
        "R": "<:rook_white:827233035971461230>",
        "r": "<:rook_black:827233035815747595>",
        "Q": "<:queen_white:827233036004360283>",
        "q": "<:queen_black:827233035920998441>",
        "P": "<:pawn_white:827233034251272262>",
        "p": "<:pawn_black:827233033874702357>",
        "N": "<:knight_white:827233034251010098>",
        "n": "<:knight_black:827233027117154425>",
        "K": "<:king_white:827233027020161044>",
        "k": "<:king_black:827233027058827345>",
        "B": "<:bishop_white:827233025145831474>",
        "b": "<:bishop_black:827233024730726421>"
    }[figure]


def add_cogs(bot: AutoShardedBot, cogs):
    for cog_c in cogs:
        bot.add_cog(cog_c(bot))

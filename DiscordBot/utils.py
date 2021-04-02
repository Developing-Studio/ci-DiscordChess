from discord.ext.commands import AutoShardedBot


def figure_to_emoji(figure: str, field_number: int):
    emojis: dict = {
        "Ql": "<:lqueenw:827569943955505153>",
        "kl": "<:lkingb:827569943972544523>",
        "qd": "<:dqueenb:827569943985127436>",
        "nl": "<:lknightb:827569944057217085>",
        "Pl": "<:lpawnw:827569944169676901>",
        "ql": "<:lqueenb:827569944178589716>",
        "Kl": "<:lkingw:827569944203624498>",
        "Qd": "<:dqueenw:827569944228135003>",
        "kd": "<:dkingb:827569944245829633>",
        "Rl": "<:lrookw:827569944270602271>",
        "rl": "<:lrookb:827569944278597632>",
        "Kd": "<:dkingw:827569944279121951>",
        "bd": "<:dbishopb:827569944304156682>",
        "Pd": "<:dpawnw:827569944312152075>",
        "bl": "<:lbishopb:827569944328667156>",
        "rd": "<:drookb:827569944333254696>",
        "pl": "<:lpawnb:827569944358944788>",
        "nd": "<:dknightb:827569944401149972>",
        "Bd": "<:dbishopw:827569944404819978>",
        "Nl": "<:lknightw:827569944438505482>",
        "Bl": "<:lbishopw:827569944442830919>",
        "pd": "<:dpawnb:827569944472453150>",
        "-l": "<:tile_light:827569944501288970>",
        "Rd": "<:drookw:827569944517541919>",
        "Nd": "<:dknightw:827569944681775144>",
        "-d": "<:tile_dark:827569944991367228>",
    }
    light_dark = "d" if not field_number else "l"
    return emojis[figure + light_dark]


def add_cogs(bot: AutoShardedBot, cogs):
    for cog_c in cogs:
        bot.add_cog(cog_c(bot))

from discord.ext.commands import AutoShardedBot

emojis: dict = {
    "Ql": "<:Ql:827569943955505153>",
    "kl": "<:kl:827569943972544523>",
    "qd": "<:qd:827569943985127436>",
    "nl": "<:nl:827569944057217085>",
    "Pl": "<:Pl:827569944169676901>",
    "ql": "<:ql:827569944178589716>",
    "Kl": "<:Kl:827569944203624498>",
    "Qd": "<:Qd:827569944228135003>",
    "kd": "<:kd:827569944245829633>",
    "Rl": "<:Rl:827569944270602271>",
    "rl": "<:rl:827569944278597632>",
    "Kd": "<:Kd:827569944279121951>",
    "bd": "<:bd:827569944304156682>",
    "Pd": "<:Pd:827569944312152075>",
    "bl": "<:bl:827569944328667156>",
    "rd": "<:rd:827569944333254696>",
    "pl": "<:pl:827569944358944788>",
    "nd": "<:nd:827569944401149972>",
    "Bd": "<:Bd:827569944404819978>",
    "Nl": "<:Nl:827569944438505482>",
    "Bl": "<:Bl:827569944442830919>",
    "pd": "<:pd:827569944472453150>",
    "-l": "<:_l:827569944501288970>",
    "Rd": "<:Rd:827569944517541919>",
    "Nd": "<:Nd:827569944681775144>",
    "-d": "<:_d:827569944991367228>",
    "r_": "<:r_:827847488449937428>",
    "R_": "<:R_:827847488500269066>",
    "Q_": "<:Q_:827847488517308437>",
    "p_": "<:p_:827847488558858291>",
    "N_": "<:N_:827847488563052564>",
    "n_": "<:n_:827847488576028702>",
    "k_": "<:k_:827847488579960863>",
    "P_": "<:P_:827847488622952478>",
    "B_": "<:B_:827847488630292500>",
    "b_": "<:b_:827847488651657216>",
    "K_": "<:K_:827847488677347338>",
    "q_": "<:q_:827847488752189461>",
}


def figure_to_emoji(figure: str, field_number: int):
    light_dark = "d" if not field_number else "l"
    light_dark = "_" if field_number == 3 else light_dark
    return emojis[figure + light_dark]


def letter_to_emoji(letter: str) -> str:
    if letter.lower() == "r":
        return "🇷"
    return f"🇦🇧🇨🇩🇪🇫🇬🇭"[ord(letter[0]) - ord("a")]


def number_to_emoji(number: str) -> str:
    n = int(number)
    return ["1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣"[i:i + 3] for i in range(0, 8 * 3, 3)][n-1]


def get_letter_by_emote(emote: str) -> str:
    for k, v in emojis.items():
        if v == emote:
            return k[0]


def add_cogs(bot: AutoShardedBot, cogs):
    for cog_c in cogs:
        bot.add_cog(cog_c(bot))

import io
import aiohttp
import random
import discord
from discord.ext import commands
from utils.db import db
from utils.markov_chain import MarkovChain

class Waifu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = "https://www.thiswaifudoesnotexist.net/example-{}.jpg"

    @commands.command()
    async def waifu(self, ctx, *args):
        if len(args):
            random.seed(" ".join(args))
        else:
            random.seed()
        num = random.randint(0, 199999)
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url.format(num)) as r:
                if r.status != 200:
                    return await ctx.message.channel.send("I couldn't get you a waifu...")
                img = io.BytesIO(await r.read())
                await ctx.message.channel.send(file=discord.File(img, f'waifu-{num}.jpg', spoiler=True))

class Markov(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def levenshtein(a, b):
        v0 = list(range(len(b) + 1))
        v1 = [0] * (len(b) + 1)
        for i in range(len(a)):
            v1[0] = i + 1
            for j in range(len(b)):
                deletion_cost = v0[j + 1] + 1
                insertion_cost = v1[j] + 1
                substitution_cost = v0[j] if a[i] == b[j] else v0[j] + 1
                v1[j + 1] = min(deletion_cost, insertion_cost, substitution_cost)
            v0 = v1[:]
        return v0[len(b)]

    @staticmethod
    def fuzzy_match(term, member):
        nick_dist = float("inf")
        if member.nick:
            nick_dist = Markov.levenshtein(term, member.nick)
        name_dist = Markov.levenshtein(term, member.name)
        return min(nick_dist, name_dist)

    @commands.command()
    async def markov(self, ctx, user_handle):
        try:
            user = ctx.message.guild.get_member(int(user_handle.strip("<>@!")))
        except ValueError:
            user = sorted([(m, self.fuzzy_match(user_handle, m)) for m in ctx.guild.members], key=lambda x: x[1])[0][0]
        if not user:
            await ctx.send(f"I couldn't find {user_handle}")
            return
        curs = db.cursor()
        statement = ("select content from messages where u_id=? and g_id=?")
        text = ""
        for message in curs.execute(statement, [user.id, ctx.guild.id]):
            text += message[0].replace("\n", " ") + "\n"
        mc = MarkovChain()
        mc.train(text)
        msg = mc.generate()
        if msg == "":
            msg = f"{user.nick} hasn't sent enough messages for me to generate anything..."
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(Waifu(bot))
    bot.add_cog(Markov(bot))

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

    @commands.command()
    async def markov(self, ctx, user_mention):
        user = ctx.message.guild.get_member(int(user_mention.strip("<>@!")))
        curs = db.cursor()
        statement = ("select content from messages where u_id=? and g_id=?")
        text = ""
        for message in curs.execute(statement, [user.id, ctx.guild.id]):
            text += message[0].replace("\n", " ") + "\n"
        mc = MarkovChain()
        mc.train(text)
        await ctx.send(mc.generate())

def setup(bot):
    bot.add_cog(Waifu(bot))
    bot.add_cog(Markov(bot))

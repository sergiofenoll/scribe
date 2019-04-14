import os
import re
import discord
from discord.ext import commands
from math import ceil

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dog(self, ctx, aaa=""):
        if re.match("a+", aaa):
            amt = min(ceil(len(aaa) / 3), 3)
        else:
            amt = 1
        for _ in range(amt):
            await ctx.message.channel.send(file=discord.File(os.path.join(os.path.dirname(__file__), "..", "static" ,"dogaaaa.png")))
        


def setup(bot):
    bot.add_cog(Reactions(bot))

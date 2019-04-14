import asyncio
import os
import re
import discord
from discord.ext import commands
from math import ceil

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.max_dog = 3
        self.dog_multiplier = None

    async def increment_dog_multiplier(self):
        self.max_dog += 1
        await asyncio.sleep(10)
        self.max_dog = 3

    @commands.command()
    async def dog(self, ctx, aaa=""):
        if re.match("a+", aaa):
            amt = min(ceil(len(aaa) / 3), self.max_dog)
        else:
            amt = 1
        if self.dog_multiplier is not None:
            self.dog_multiplier.cancel()
        self.dog_multiplier = asyncio.create_task(self.increment_dog_multiplier())
        for _ in range(amt):
            await ctx.message.channel.send(file=discord.File(os.path.join(os.path.dirname(__file__), "..", "static" ,"dogaaaa.png")))
        


def setup(bot):
    bot.add_cog(Reactions(bot))

import aiohttp
import asyncio
import discord
import io
import os
import random
import re
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

    async def send_dogs(self, message, aaa, min_amt=1):
        if re.match("a+", aaa, re.IGNORECASE):
            amt = min(ceil(len(aaa) / 3), self.max_dog)
        else:
            amt = min_amt
        if self.dog_multiplier is not None:
            self.dog_multiplier.cancel()
        self.dog_multiplier = asyncio.create_task(self.increment_dog_multiplier())
        for _ in range(amt):
            await message.channel.send(file=discord.File(os.path.join(os.path.dirname(__file__), "..", "static" ,"dogaaaa.png")))

    @commands.command()
    async def dog(self, ctx, aaa=""):
        await self.send_dogs(ctx.message, aaa)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(self.bot.command_prefix):
            # Get the first "word" from the message and remove command_prefix
            aaa = message.content.split(' ', 1)[0].strip(self.bot.command_prefix)
            await self.send_dogs(message, aaa, min_amt=0)

    @commands.command(name="not-funny")
    async def not_funny(self, ctx):
        await ctx.send(file=discord.File(os.path.join(os.path.dirname(__file__), "..", "static", "not-funny.mp4")))


def setup(bot):
    bot.add_cog(Reactions(bot))

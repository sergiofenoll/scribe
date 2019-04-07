import io
import aiohttp
import random
import discord
from discord.ext import commands

class Waifu:
    def __init__(self, bot):
        self.bot = bot
        self.url = "https://www.thiswaifudoesnotexist.net/example-{}.jpg"

    @commands.command()
    async def waifu(self, ctx, *args):
        if len(args):
            random.seed(" ".join(args))
        num = random.randint(0, 99999)
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url.format(num)) as r:
                if r.status != 200:
                    return await ctx.message.channel.send("I couldn't get you a waifu...")
                img = io.BytesIO(await r.read())
                await ctx.message.channel.send(file=discord.File(img, f'waifu-{num}.jpg'))


def setup(bot):
    bot.add_cog(Waifu(bot))

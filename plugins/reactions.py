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

    @commands.command()
    async def d2(self, ctx, *args):
        query = None
        if len(args):
            query = " ".join(args)

        async with aiohttp.ClientSession() as session:

            params = {"client_id": 9587, "client_secret": "18e5358b2471eb06a2e6b08d2251d80d", "grant_type": "client_credentials"}
            async with session.get("https://www.deviantart.com/oauth2/token", params=params) as r:
                payload = await r.json()
                access_token = payload["access_token"]

            params = {"access_token": access_token, "limit": 1, "offset": 0, "mature_content": 1, "q": "#nsfw", "timerange": "alltime"}
            if query:
                params["q"] = query + " #nsfw"

            async with session.get("https://www.deviantart.com/api/v1/oauth2/browse/popular", params=params) as r:
                payload = await r.json()
                total_posts = payload["estimated_total"]
                if total_posts == 0:
                    return await ctx.channel.send("I couldn't find any content using that search term")

            params["offset"] = random.randint(0, min(15999, total_posts))

            async with session.get("https://www.deviantart.com/api/v1/oauth2/browse/popular", params=params) as r:
                payload = await r.json()
                if "content" in payload["results"][0]:
                    async with session.get(payload["results"][0]["content"]["src"]) as r2:
                        fname = payload["results"][0]["content"]["src"].rsplit('/', 1)[1]
                        img = io.BytesIO(await r2.read())
                        await ctx.channel.send(f"<{payload['results'][0]['url']}>", file=discord.File(img, "fuck.png", spoiler=True))
                else:
                    await ctx.channel.send(f"<{payload['results'][0]['url']}>")

def setup(bot):
    bot.add_cog(Reactions(bot))

import discord
from discord.ext import commands
from config import plugins
from utils.plugin_cache import plugin_cache

def plugin_manager_permissions(ctx):
    return ctx.author.id == 160462583453712386 or ctx.author.guild_permissions.administrator

class PluginManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(plugin_manager_permissions)
    async def load(self, ctx, plugin):
        if plugin in plugin_cache.plugins:
            plugin_cache.load_plugin(ctx.guild.id, plugin)
            await ctx.send(f"The plugin {plugin} was loaded.")
        else:
            await ctx.send(f"The plugin {plugin} was not found. The available plugins are: {', '.join(plugin_cache.plugins)}")

    @commands.command()
    @commands.check(plugin_manager_permissions)
    async def unload(self, ctx, plugin):
        if plugin == "PluginManager":
            await ctx.send("PluginManager cannot be unloaded")
        elif plugin in plugin_cache.plugins:
            plugin_cache.unload_plugin(ctx.guild.id, plugin)
            await ctx.send(f"The plugin {plugin} was unloaded.")
        else:
            await ctx.send(f"The plugin {plugin} was not found. The available plugins are: {', '.join(plugin_cache.plugins)}")

    @commands.command()
    @commands.check(plugin_manager_permissions)
    async def loaded(self, ctx):
        await ctx.send(f"Currently loaded plugins: {', '.join(plugin for plugin in plugin_cache.cache if ctx.guild.id in plugin_cache.cache[plugin])}")

def setup(bot):
    bot.add_cog(PluginManager(bot))

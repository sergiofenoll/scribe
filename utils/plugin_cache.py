from utils.db import db

class PluginCache:
    def __init__(self):        
        self.plugins = list()
        self.cache = dict()

    def create_cache(self, bot):
        self.plugins = [cog for cog in bot.cogs.keys()]

        for guild in db.get_all_guilds():
            db.update_plugins({"plugin_name": "PluginManager", "g_id": guild[0], "loaded": True})
            self.cache[guild[0]] = {"PluginManager"}
        
        for plugin, guild_id, loaded in db.get_all_plugins():
            if loaded:
                self.cache[guild_id].add(plugin)

    def load_plugin(self, guild_id, plugin):
        if plugin not in self.cache[guild_id]:
            self.cache[guild_id].add(plugin)
            db.update_plugins({"plugin_name": plugin, "g_id": guild_id, "loaded": True})

    def unload_plugin(self, guild_id, plugin):
        if plugin in self.cache[guild_id]:
            self.cache[guild_id].remove(plugin)
            db.update_plugins({"plugin_name": plugin, "g_id": guild_id, "loaded": False})
            

plugin_cache = PluginCache()
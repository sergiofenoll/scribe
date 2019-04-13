from utils.db import db

class PluginCache:
    def __init__(self):        
        self.plugins = list()
        self.cache = dict()

    def create_cache(self, bot):
        self.plugins = [cog for cog in bot.cogs.keys()]
        self.cache = dict([(plugin, set()) for plugin in self.plugins])

        for guild in db.get_all_guilds():
            db.update_plugins({"plugin_name": "PluginManager", "g_id": guild[0], "loaded": True})

        for plugin, guild_id, loaded in db.get_all_plugins():
            if loaded:
                self.cache[plugin].add(guild_id)

    def load_plugin(self, guild_id, plugin):
        if guild_id not in self.cache[plugin]:
            self.cache[plugin].add(guild_id)
            db.update_plugins({"plugin_name": plugin, "g_id": guild_id, "loaded": True})

    def unload_plugin(self, guild_id, plugin):
        if guild_id in self.cache[plugin]:
            self.cache[plugin].remove(guild_id)
            db.update_plugins({"plugin_name": plugin, "g_id": guild_id, "loaded": False})
            

plugin_cache = PluginCache()
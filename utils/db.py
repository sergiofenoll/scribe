import sqlite3
import os

class DB:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '..', "messages.db"))
        # exit()

    def create_db(self):
        curs = self.cursor()
        curs.execute(
            "create table if not exists users(u_id bigint, g_id bigint references guilds(g_id), username text, discriminator text, nick text, left bool, start_time timestamp, end_time timestamp, primary key(u_id, g_id))"
        )
        curs.execute(
            "create table if not exists messages(m_id bigint primary key, sent_time timestamp, content text, u_id bigint references users(u_id), c_id bigint references channels(c_id), g_id bigint references guilds(g_id) on delete cascade, edited bool, edited_count int, edited_time timestamp, deleted bool, deleted_time timestamp)"
        )
        curs.execute(
            "create table if not exists emojis(e_id varchar primary key, g_id bigint references guilds(g_id), name text, animated bool, created_time timestamp)"
        )
        curs.execute(
            "create table if not exists reactions(m_id bigint references messages(m_id) on delete cascade, e_id varchar references emojis(e_id), count integer, primary key(m_id, e_id))"
        )
        curs.execute(
            "create table if not exists guilds(g_id bigint, name text, start_time timestamp, end_time timestamp, primary key(g_id, start_time))"
        )
        curs.execute(
            "create table if not exists channels(c_id bigint, g_id bigint references guilds(g_id) on delete cascade, name text, topic text, start_time timestamp, end_time timestamp, primary key(c_id, start_time))"
        )
        curs.execute(
            "create table if not exists bans(count integer default 0, u_id bigint references users(u_id) on delete cascade, g_id bigint references guilds(g_id) on delete cascade, primary key(u_id, g_id))"
        )
        curs.execute(
            "create table if not exists plugins(plugin_name text, g_id bigint references guilds(g_id) on delete cascade, loaded bool, primary key(plugin_name, g_id))"
        )
        self.conn.commit()

    def user_exists(self, filters):
        curs = self.cursor()
        statement = "select * from users where " + (
            " and ".join(key + " = ?" for key in filters.keys())
        )
        result = curs.execute(statement, list(filters.values())).fetchone()
        self.conn.commit()
        return result is not None

    def add_user(self, data):
        curs = self.cursor()
        statement = (
            "insert or replace into users values("
            + ("?," * len(data.values()))[:-1]
            + ")"
        )
        curs.execute(statement, list(data.values()))
        self.conn.commit()

    def delete_user(self, filters, data):
        curs = self.cursor()
        statement = "update users set left = ? where " + (
            " and ".join(key + " = ?" for key in filters.keys())
        )
        curs.execute(statement, [data["left"]] + list(filters.keys()))
        self.conn.commit()

    def edit_user(self, filters, data):
        curs = self.cursor()
        statement = "update users set end_time = ? where " + (
            " and ".join(key + " = ?" for key in filters.keys())
        )
        curs.execute(statement, [data["start_time"]] + list(filters.values()))
        self.conn.commit()
        self.add_user(data)

    def get_user(self, filters):
        curs = self.cursor()
        statement = "select * from users where " + (
            " and ".join(key + " = ?" for key in filters.keys())
        )
        return curs.execute(statement, list(filters.values())).fetchone()

    def guild_exists(self, filters):
        curs = self.cursor()
        statement = "select * from guilds where " + (
            " and ".join(key + " = ?" for key in filters.keys())
        )
        result = curs.execute(statement, list(filters.values())).fetchone()
        self.conn.commit()
        return result is not None

    def add_guild(self, data):
        curs = self.cursor()
        statement = (
            "insert or replace into guilds values("
            + ("?," * len(data.values()))[:-1]
            + ")"
        )
        curs.execute(statement, list(data.values()))
        self.conn.commit()

    def delete_guild(self, filters, data):
        curs = self.cursor()
        statement = "update guilds set end_time = ? where " + (
            " and ".join(key + " = ?" for key in filters.keys())
        )
        print(statement)
        curs.execute(statement, [data["end_time"]] + list(filters.keys()))
        self.conn.commit()

    def edit_guild(self, filters, data):
        curs = self.cursor()
        statement = "update guilds set end_time ? where " + (
            " and ".join(key + " = ?" for key in filters.keys())
        )
        curs.execute(statement, [data["start_time"]] + list(filters.values()))
        self.conn.commit()
        self.add_guild(data)
    
    def get_all_guilds(self):
        curs = self.cursor()
        statement = (
            "select * from guilds"
        )
        result = curs.execute(statement)
        self.conn.commit()
        return result

    def channel_exists(self, filters):
        curs = self.cursor()
        statement = "select * from channels where " + (
            " and ".join(key + " = ?" for key in filters.keys())
        )
        result = curs.execute(statement, list(filters.values())).fetchone()
        self.conn.commit()
        return result is not None

    def add_channel(self, data):
        curs = self.cursor()
        statement = (
            "insert or replace into channels values("
            + ("?," * len(data.values()))[:-1]
            + ")"
        )
        curs.execute(statement, list(data.values()))
        self.conn.commit()

    def delete_channel(self, filters, data):
        curs = self.cursor()
        statement = "update channels set end_time = ? where " + (
            " and ".join(key + " = ?" for key in filters.keys())
        )
        curs.execute(statement, [data["end_time"]] + list(filters.values()))
        self.conn.commit()

    def edit_channel(self, filters, data):        
        curs = self.cursor()
        statement = "update channels set end_time = ? where " + (
            " and ".join(key + " = ?" for key in filters.keys())
        )
        curs.execute(statement, [data["start_time"]] + list(filters.values()))
        self.conn.commit()
        self.add_channel(data)

    def get_messages(self, filters):
        curs = self.cursor()
        curs.execute("select * from messages where m_id = ?", filters["message_id"])
        return curs.fetchall()

    def add_message(self, data):
        curs = self.cursor()
        statement = (
            "insert or replace into messages values("
            + ("?," * len(data.values()))[:-1]
            + ")"
        )
        curs.execute(statement, list(data.values()))
        self.conn.commit()

    def edit_message(self, filters, data):
        curs = self.cursor()
        statement = (
            "update messages set content = ?, edited_time = ?, edited = 1, edited_count = edited_count + 1 where "
            + (" and ".join(key + " = ?" for key in filters.keys()))
        )
        curs.execute(
            statement, [data["content"], data["edited_time"]] + list(filters.keys())
        )
        self.conn.commit()

    def delete_message(self, filters, data):
        curs = self.cursor()
        statement = (
            "update messages set content = NULL, deleted_time = ?, deleted = 1 where "
            + (" and ".join(key + " = ?" for key in filters.keys()))
        )
        curs.execute(statement, [data["deleted_time"]] + list(filters.keys()))
        self.conn.commit()

    def update_emoji(self, data):
        curs = self.cursor()
        statement = (
            "insert or replace into emojis values("
            + ("?," * len(data.values()))[:-1]
            + ")"
        )
        curs.execute(statement, list(data.values()))
        self.conn.commit()

    def update_reaction(self, data):
        curs = self.cursor()
        statement = (
            "insert or replace into reactions values("
            + ("?," * len(data.values()))[:-1]
            + ")"
        )
        curs.execute(statement, list(data.values()))
        self.conn.commit()

    def update_bans(self, data):
        curs = self.cursor()
        statement = (
            "insert or replace into bans values("
            + ("?," * len(data.values()))[:-1]
            + ")"
        )
        curs.execute(statement, list(data.values()))
        self.conn.commit()

    def get_bans(self, filters):
        curs = self.cursor()
        statement = (
            "select count from bans where u_id = ? and g_id = ?"
        )
        result = curs.execute(statement, [filters["u_id"], filters["g_id"]]).fetchone()
        self.conn.commit()
        if result is None:
            return (0,)
        else:
            return result

    def update_plugins(self, data):
        curs = self.cursor()
        statement = (
            "insert or replace into plugins values("
            + ("?," * len(data.values()))[:-1]
            + ")"
        )
        curs.execute(statement, list(data.values()))
        self.conn.commit()

    def get_plugins(self, filters):
        curs = self.cursor()
        statement = (
            "select * from plugins where plugin_name = ? and g_id = ?"
        )
        result = curs.execute(statement, [filters["plugin_name"], filters["g_id"]])
        self.conn.commit()
        return result

    def get_all_plugins(self):
        curs = self.cursor()
        statement = (
            "select * from plugins"
        )
        result = curs.execute(statement)
        self.conn.commit()
        return result

    def cursor(self):
        return self.conn.cursor()


db = DB()

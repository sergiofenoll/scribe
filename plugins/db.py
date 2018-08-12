import sqlite3

class DB():
    def __init__(self):
        conn = sqlite3.connect("messages.db")

    def create_db():
        curs = self.cursor()
        curs.execute("create table if not exists messages(m_id bigint primary key, sent_time timestamp, content text, author text, channel text, guild text, attachments text[], edited bool, deleted bool")
        curs.execute("create table if not exists reactions(m_id bigint references messages(m_id) on delete cascade, reaction_name text, reaction_count integer")
        self.conn.commit()

    def get_messages():
        curs = self.cursor()
        curs.execute("select * from messages where m_id = ?", message_id)
        return curs.fetchall()

    def add_message():
        pass

    def edit_message()

    def remove_message():
        pass

    def add_reaction():
        pass

    def remove_reaction():
        pass

    def cursor():
        return self.conn.cursor()

db = DB()

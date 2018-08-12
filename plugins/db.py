import sqlite3

class DB():
    def __init__(self):
        self.conn = sqlite3.connect("messages.db")

    def create_db(self):
        curs = self.cursor()
        curs.execute("create table if not exists messages(m_id bigint primary key, sent_time timestamp, content text, author text, channel text, guild text, edited bool, deleted bool)")
        curs.execute("create table if not exists reactions(m_id bigint references messages(m_id) on delete cascade, reaction_name text, reaction_count integer)")
        self.conn.commit()

    def get_messages(self):
        curs = self.cursor()
        curs.execute("select * from messages where m_id = ?", message_id)
        return curs.fetchall()

    def add_message(self, content):
        curs = self.cursor()
        statement = "insert into messages values(" + ("?," * len(content.values()))[:-1] + ")"
        curs.execute(statement, content.values())
        self.conn.commit()

    def edit_message(self):
        pass

    def delete_message(self):
        pass

    def add_reaction(self):
        pass

    def remove_reaction(self):
        pass

    def cursor(self):
        return self.conn.cursor()

db = DB()

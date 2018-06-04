import psycopg2
from config import config

class DBConnection:
    def __init__(self,
            db_name=config['DBNAME'],
            db_user=config['DBUSER'],
            db_pass=config['DBPASS']):
        self.conn = psycopg2.connect('dbname={} user={} password={}'.format(
            db_name, db_user, db_pass))

    def setup(self):
        try:
            with self.conn:
                with self.conn.cursor() as curs:
                    curs.execute(
                            """CREATE TABLE IF NOT EXISTS MESSAGES (
                            M_ID BIGINT PRIMARY KEY,
                            SENT_TIME TIMESTAMP,
                            CONTENT TEXT,
                            AUTHOR TEXT,
                            CHANNEL TEXT,
                            SERVER TEXT,
                            ATTACHMENTS TEXT[],
                            DELETED BOOL
                            );""")
                    curs.execute(
                            """CREATE TABLE IF NOT EXISTS EDITED (
                            M_ID BIGINT REFERENCES MESSAGES(M_ID) ON DELETE CASCADE,
                            EDITED_TIME TIMESTAMP,
                            EDITED_CONTENT TEXT
                            );""")
                    curs.execute(
                            """CREATE TABLE IF NOT EXISTS REACTIONS (
                            M_ID BIGINT REFERENCES MESSAGES(M_ID) ON DELETE CASCADE,
                            REACTION_NAME TEXT,
                            REACTION_COUNT INTEGER
                            );""")
        except Exception as e:
            print(e)
            print('Exception in db_connection.py, check what exception it is and handle it separately.')

    def create_log_from_message(self, message):
        try:
            with self.conn as conn:
                with conn.cursor() as curs:
                    curs.execute(
                            """INSERT INTO MESSAGES VALUES(
                            %(m_id)s, %(sent_time)s, %(content)s,
                            %(author)s, %(channel)s, %(server)s,
                            %(attachments)s, NULL
                            );""",
                            {
                                'm_id': message.id, 'sent_time': message.created_at,
                                'content': message.clean_content, 'author': message.author.name,
                                'channel': message.channel.name, 'server': str(message.guild),
                                'attachments': list([atch.url for atch in message.attachments]),
                            })
        except Exception as e:
            print(e)

    def delete_log_from_channel(self, channel):
        try:
            with self.conn as conn:
                with conn.cursor() as curs:
                    curs.execute('DELETE FROM MESSAGES WHERE CHANNEL = %s', (channel.name,))
        except Exception as e:
            print(e)

    def get_oldest_log_from_channel(self, channel):
        try:
            with self.conn as conn:
                with conn.cursor() as curs:
                    curs.execute(
                            """SELECT MIN(SENT_TIME) 
                            FROM MESSAGES WHERE CHANNEL = %s;""",
                            (channel.name,))
                    return curs.fetchone()[0]
                    
        except Exception as e:
            print(e)

    def connection(self):
        return self.conn

DBConnectionInstance = DBConnection()

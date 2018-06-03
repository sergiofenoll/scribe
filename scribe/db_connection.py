import psycopg2
from config import config

class DBConnection:
    def __init__(self,
            db_name=config['DBNAME'],
            db_user=config['DBUSER'],
            db_pass=config['DBPASS']):
        self.conn = psycopg2.connect('dbname={} user={} password={}'.format(
            db_name, db_user, db_pass))

    def setupDB(self):
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

    def connection(self):
        return self.conn

DBConnectionInstance = DBConnection()

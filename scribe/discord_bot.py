import asyncio
import discord
from db_connection import DBConnectionInstance as dbc

client = discord.Client()

@client.event
async def on_message(message):
    try:
        with dbc.connection() as conn:
            with conn.cursor() as curs:
                curs.execute(
                        """INSERT INTO MESSAGES VALUES(
                        %(m_id)s, %(sent_time)s, %(content)s,
                        %(author)s, %(channel)s, %(attachments)s, NULL
                        );""",
                        {
                            'm_id': message.id, 'sent_time': message.created_at,
                            'content': message.clean_content, 'author': message.author.name,
                            'channel': message.channel.name,
                            'attachments': list([atch.url for atch in message.attachments]),
                        })
    except Exception as e:
        print(e)
        print('Exception in discord_bot.py, check what exception it is and handle it separately')

@client.event
async def on_raw_message_edit(payload):
    try:
        with dbc.connection() as conn:
            with conn.cursor() as curs:
                curs.execute(
                        """INSERT INTO EDITED VALUES (
                        %s, %s, %s
                        );""", (
                            payload.data['id'],
                            payload.data['edited_timestamp'],
                            payload.data['content']))
    except Exception as e:
        print(e)

@client.event
async def on_raw_message_delete(payload):
    try:
        with dbc.connection() as conn:
            with conn.cursor() as curs:
                curs.execute('UPDATE MESSAGES SET DELETED = TRUE WHERE M_ID = %s',
                        (payload.message_id,))
    except Exception as e:
        print(e)

@client.event
async def on_raw_reaction_add(payload):
    try:
        with dbc.connection() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """INSERT INTO REACTIONS VALUES(%s, %s, %s)
                    ON CONFLICT (REACTION_NAME) DO NOTHING;""",
                    (payload.message_id, str(payload.emoji), 0))
                curs.execute(
                    """UPDATE REACTIONS SET 
                    REACTION_COUNT = REACTION_COUNT + 1
                    WHERE REACTION_NAME = %s;""",
                    (str(payload.emoji),))
    except Exception as e:
        print(e)

@client.event
async def on_raw_reaction_add(payload):
    try:
        with dbc.connection() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """UPDATE REACTIONS SET 
                    REACTION_COUNT = REACTION_COUNT - 1
                    WHERE REACTION_NAME = %s;""",
                    (str(payload.emoji),))
    except Exception as e:
        print(e)

client.run('MzgyOTk2OTI0NDAxNDUxMDEx.Dby1OA.1uFNc506yFY9KBwbIBy59RjPQ50')

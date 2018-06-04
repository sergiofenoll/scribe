import asyncio
import discord
from db_connection import DBConnectionInstance as dbc

client = discord.Client()

@client.event
async def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + str(client.user.id))

@client.event
async def on_message(message):
    # Preconditions
    if message.author.id == client.user.id:
        return
    if str(message.channel) != 'bottlegrounds':
        return
    if not message.content.startswith('!'):
        return
    # Preconditions passed, handle message

    dbc.create_log_from_message(message)

    if message.content.startswith('!log'):
        await log_command(message)
    elif message.content.startswith('!help'):
        await help_command(message)
    else:
        await message.channel.send("Hello, this is Scribe!\nI can't recognize the command you sent so I'll tell you about what I can do.")
        await help_command(message)

async def help_command(message):
        await message.channel.send(
"""```
!log create #channel-name-1 #channel-name-2 ...
    Creates log for all the messages in #channel-name-i
    from the oldest message on the Discord server to the oldest logged message.
!log create all
    Creates log for all the messages in all the channels
    from the oldest message on the Discord server to the oldest logged message.

!log delete #channel-name-1 #channel-name-2 ...
    Deletes logs for all the messages in #channel-name-i.
!log delete all
    Deletes logs for all messages.

!help
    Prints this help message
```""")


async def log_command(message):
    split_content = message.content.split()
    
    if len(split_content) < 3:
        await message.channel.send('Unknown command, please check `!help`.')
    
    if split_content[1] == 'create':
        # !log create [#channel-name]
        if len(message.channel_mentions):
            async with message.channel.typing():
                for channel in message.channel_mentions:
                    if message.guild.me.permissions_in(channel).read_message_history:
                        # Get timestamp of oldest logged message
                        oldest_logged = dbc.get_oldest_log_from_channel(channel)
                        async for log_message in channel.history(limit=None, before=oldest_logged):
                            dbc.create_log_from_message(log_message)
                await message.channel.send('Finished creating logs!')
        # !log create all
        elif split_content[2] == 'all':
            async with message.channel.typing():
                for channel in message.guild.text_channels:
                    if message.guild.me.permissions_in(channel).read_message_history:
                        # Get timestamp of oldest logged message
                        oldest_logged = dbc.get_oldest_log_from_channel(channel)
                        async for log_message in channel.history(limit=None, before=oldest_logged):
                            dbc.create_log_from_message(log_message)
                await message.channel.send('Finished creating logs!')

    elif split_content[1] == 'delete':
        # Only I can delete logs... for now
        if message.author.id != 160462583453712386:
            return
        # !log delete [#channel-name]
        if len(message.channel_mentions):
            async with message.channel.typing():
                for channel in message.channel_mentions:
                    if message.guild.me.permissions_in(channel).read_message_history:
                        dbc.delete_log_from_channel(channel)
                await message.channel.send('Finished deleting logs!')
        # !log delete all
        elif split_content[2] == 'all':
            async with message.channel.typing():
                for channel in message.guild.text_channels:
                    if message.guild.me.permissions_in(channel).read_message_history:
                        dbc.delete_log_from_channel(channel)
                await message.channel.send('Finished deleting logs!')
    # !log xxx
    else:
        await message.channel.send('Unknown command, please check `!help`.')


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

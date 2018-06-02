import discord
import asyncio

client = discord.Client()

@client.event
@asyncio.coroutine
def on_message(message):
    with open('discord_log.log', 'a') as f:
        f.write(str(message.timestamp) + ' - ' + message.author.nick + ': ' + message.content + '\n')
        # print(message.attachments)
        # print(message.clean_content)

client.run('MzgyOTk2OTI0NDAxNDUxMDEx.Dby1OA.1uFNc506yFY9KBwbIBy59RjPQ50')

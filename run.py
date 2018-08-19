# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import asyncio
import psycopg2

# from discord.ext import commands

import os

try:
      from local_settings import *
except ImportError:
      token = os.environ['TOKEN']
      url = os.environ['DATABASE_URL']

#from datetime import datetime

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    # purging
    # if message.content.startswith('!purge '):
    #     isMod = False
    #     for r in message.author.roles:
    #         if r.name == 'Fisting Fairy' or r.name == 'Here is my Glamour Luke':
    #             isMod = True
    #     if isMod:
    #         try:
    #             number = int(message.content[7:])
    #             await client.purge_from(message.channel, limit=number)
    #         except ValueError:
    #             msg = 'Enter a real number, you fucking idiot'.format(message)
    #             await client.send_message(message.channel, msg)
    #     else:
    #         msg = 'Nice try, baby bitch'.format(message)
    #         await client.send_message(message.channel, msg)

    # auto-replies
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!die'):
        msg = 'Oh :('.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!hendy'):
        msg = 'NO'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('?google') or message.content.startswith('!google'):
        msg = 'Bots can\'t use Google anymore, you dumb bitch'.format(message)
        await client.send_message(message.channel, msg)

    # if message.content.startswith('!birthday'): #!birthday YYYY-mm-dd
    #     msg = '{0.author.mention}\'s birthday recorded.'.format(message)
    #     await client.send_message(message.channel, msg)

async def check_for_retweets():
    await client.wait_until_ready()
    try:
        while not client.is_closed:
            print('------')

            #pull already retweeted messages from database
            conn = psycopg2.connect(url, sslmode='require')
            cur = conn.cursor()

            cur.execute("SELECT messageid FROM retweeted_messages;")
            retweeted_messages = [x[0] for x in cur.fetchall()]

            new_messages = []
            new_messages_timestamps = []
            new_messages_rcount = []

            #get all messages with the proper number of retweet emojis
            for c in client.get_all_channels():
                async for m in client.logs_from(client.get_channel(c.id), limit=100000):
                    for r in m.reactions:
                        if r.custom_emoji:
                            # if r.emoji.name == 'retweet' and r.count > 2 and m.timestamp >= datetime.strptime('Aug 14 2018  5:00PM', '%b %d %Y %I:%M%p')\
                            if r.emoji.name == 'retweet' and r.count > 2 and m.id not in retweeted_messages \
                                    and m.author != client.user:
                                new_messages.append(m)
                                new_messages_timestamps.append(m.timestamp)
                                new_messages_rcount.append(r.count)

            #post messages in order of timestamp
            timestamps_order = sorted(range(len(new_messages_timestamps)), key=lambda k: new_messages_timestamps[k]) # indices of sorted
            for index in timestamps_order:
                m = new_messages[index]
                msg = '<:retweet:449394937541427230> x ' + str(new_messages_rcount[index])
                em = discord.Embed(description=m.content, colour=0000000)
                if len(m.attachments) > 0:
                    image_url = m.attachments[0].get('url')
                    em.set_image(url=image_url)
                    print(image_url)
                if len(m.embeds) > 0:
                    print(m.embeds[0].get('url') != None)
                    if m.embeds[0].get('description') != None: #text embed
                        content = ''
                        if m.embeds[0].get('title') != None:
                            content = m.embeds[0].get('title') + '\n'
                        content = content + m.embeds[0].get('description') + '\n'
                        if m.embeds[0].get('footer') != None:
                            content = content + m.embeds[0].get('footer').get('text')
                        em = discord.Embed(description=content, colour=0000000)
                    if m.embeds[0].get('url') != None: #image embed
                        image_url = m.embeds[0].get('url')
                        em.set_image(url=image_url)
                        print(image_url)
                if hasattr(m.author, 'nick'):
                    nickname = m.author.nick
                    em.set_author(name=nickname, icon_url=m.author.avatar_url)
                else:
                    nickname = m.author.name
                    em.set_author(name=nickname, icon_url=m.author.avatar_url)
                em.set_footer(text="#" + m.channel.name)
                print(nickname)
                print(m.timestamp)
                print(msg)
                print(em.description)
                await client.send_message(client.get_channel('448621029930303488'),
                                          msg,
                                          embed=em)

            #write new message ids to database
            for m in new_messages:
                cur.execute("INSERT INTO retweeted_messages (messageid) VALUES (%s)" % m.id)

            conn.commit()
            cur.close()
            conn.close()

            print('Sleeping')
            await asyncio.sleep(60)  # task runs every 60 seconds
    except Exception:
        print(Exception.with_traceback())
        await asyncio.sleep(60)

@client.event
async def on_ready():
    # conn = psycopg2.connect(url, sslmode='require')
    # cur = conn.cursor()
    #
    # cur.execute("SELECT messageid FROM retweeted_messages;")
    # retweeted_messages = [x[0] for x in cur.fetchall()]

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    # for x in client.get_all_channels():
    #     print(x)
    #     print(x.id)
    print('------')

client.loop.create_task(check_for_retweets())

client.run(token)

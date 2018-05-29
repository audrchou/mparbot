# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord

TOKEN = 'NDQ4NTQzNjgwNDU0ODUyNjI4.DeZPaw.RHAWgz1vmD2B_uq7-4HtJuf--Tw'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    #checks for retweet emojis
    file = open('retweeted_messages.txt', 'r+')
    retweeted_messages = []
    for m in file.readlines():
        retweeted_messages.append(m.strip())
    new_messages = []
    for c in client.get_all_channels():
        async for m in client.logs_from(client.get_channel(c.id), limit = 100000):
            for r in m.reactions:
                if r.custom_emoji:
                    if r.emoji.name == 'retweet' and r.count > 2 and m.id not in retweeted_messages \
                            and message.author != client.user:
                        new_messages.append(m.id)
                        msg = '<:retweet:449394937541427230> x ' + str(r.count)
                        em = discord.Embed(description=m.content, title="#" + c.name, colour=0000000)
                        if m.author.nick is None:
                            nickname = m.author.name
                            em.set_author(name=nickname, icon_url=m.author.avatar_url)
                        else:
                            nickname = m.author.nick
                            em.set_author(name=nickname, icon_url=m.author.avatar_url)
                        if len(m.attachments) > 0:
                            image_url = m.attachments[0].get('url')
                            em.set_image(url=image_url)

                        await client.send_message(client.get_channel('448621029930303488'),
                                                  msg.format(message),
                                                  embed = em)
    for m in new_messages:
        file.write(m + '\n')
    file.close()

    # purging
    if message.content.startswith('!purge '):
        isMod = False
        for r in message.author.roles:
            if r.name == 'Fisting Fairy' or r.name == 'Here is my Glamour Luke':
                isMod = True
        if isMod:
            try:
                number = int(message.content[7:])
                await client.purge_from(message.channel, limit=number)
            except ValueError:
                msg = 'Enter a real number, you fucking idiot'.format(message)
                await client.send_message(message.channel, msg)
        else:
            msg = 'Nice try, baby bitch'.format(message)
            await client.send_message(message.channel, msg)

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

@client.event
async def on_ready():
    # write all previous retweeted messages to txt file so they don't appear
    file = open('retweeted_messages.txt', 'r+')
    retweeted_messages = []
    for m in file.readlines():
        retweeted_messages.append(m.strip())
    new_messages = []
    for c in client.get_all_channels():
        async for m in client.logs_from(client.get_channel(c.id), limit = 100000):
            for r in m.reactions:
                if r.custom_emoji:
                    if r.emoji.name == 'retweet' and r.count > 2 and m.id not in retweeted_messages:
                        new_messages.append(m.id)
    for m in new_messages:
        file.write(m + '\n')
    file.close()

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    # for x in client.get_all_channels():
    #     print(x)
    #     print(x.id)
    print('------')
client.run(TOKEN)
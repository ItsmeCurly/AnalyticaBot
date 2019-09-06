import discord

client = discord.Client()

prefix = '--'

def read_token():
    file = open('token.txt')
    lines = file.readlines()
    return lines[0].strip()

#begin async functions

async def create_emoji(message, content):
    pass

async def set_prefix(message, content):
    file = open('valid_prefixes.txt')
    prefixes = file.readlines()

    valid_prefix = False

    #must check in this order
    for line in prefixes:
        if line.strip() in content:
            valid_prefix = True

    if len(content) != 1 and len(content) != 2:
        valid_prefix = False

    global prefix
    if valid_prefix:
        prefix = content
        await message.channel.send("New prefix: " + content)

async def get_prefix(message, content):
    await message.channel.send(prefix)

async def handleCommand(message):
    print('Command: ' + message.content)
    content = message.content[len(prefix):]
    if content.startswith('create_emoji'):
        await create_emoji(message, content[len('create_emoji'):])

    elif content.startswith('set_prefix'):
        await set_prefix(message, content[len('set_prefix'):].strip())

    elif content.startswith('get_prefix'):
        await get_prefix(message, content[len('get_prefix'):].strip())

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if(message.content.startswith(prefix)):
        await handleCommand(message)

    ##print('Message from {0.author}: {0.content}'.format(message))

    ##await channel.send('hello')

client.run(read_token())

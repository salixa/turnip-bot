# bot.py
import os
import discord
from dotenv import load_dotenv
from commands import Commands

load_dotenv()
COMMAND_PREFIX = '!t'
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    print(message)
    if message.author.bot is True:
        return
    tokens = message.content.lower().split()
    if tokens[0] != COMMAND_PREFIX:
        return
    if is_help_command(tokens):
        return await handle_help(tokens, message.channel)
    if tokens[1] == 'add':
        return await handle_add(tokens, message.channel)
    return await message.channel.send('Invalid command!\nAvailable Commands: ' + ','.join([e.value for e in Commands]))

def is_help_command(tokens):
    #TODO refactor this
    try:
        if len(tokens) == 1 or \
                (len(tokens) == 2 and Commands(tokens[1]) is Commands.HELP) or \
                (len(tokens) == 3 and Commands(tokens[2]) is not None):
            return True
        return False
    except ValueError:
        return False

async def handle_help(tokens, channel):
    if len(tokens) < 3 or Commands(tokens[2]) is Commands.HELP:
        return await channel.send('Available Commands: ' + ','.join([e.value for e in Commands]) + '\nFor more detailed usage information, type "!t help <command>"')
    if Commands(tokens[2]) is Commands.ADD:
        return await channel.send('Record turnip prices. Supports a variety of formats. Examples:'
                                  '\n```!t add 115'
                                  '\n!t add 115 pm'
                                  '\n!t add 4/20/20 AM 115```'
                                  '\nDate (MM/DD/YY) and AM/PM are optional, and if not provided will be inferred from timestamp in EST.'
                                  '\nIf a Date is provided, AM/PM must also be provided.')
    if Commands(tokens[2]) is Commands.SHOW:
        return await channel.send('Prints out a table of the current week\'s turnip prices. Example:\n```'
                                  '\n            User1  User2'
                                  '\n4/19 BUY    96     99'
                                  '\n4/20 AM     77     105'
                                  '\n4/20 PM     69     103'
                                  '```')

async def handle_add(tokens, channel):
    return

async def handle_show(tokens, channel):
    return

client.run(TOKEN)

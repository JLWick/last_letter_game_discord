# This is a bot that takes all of the words said in a channel,
# and if anyone repeats a word, it reacts with a recycle emoji
import discord
import consts
import csv

intents = discord.Intents.default() # enable most permissions
intents.message_content = True # allow bot to read messages

client = discord.Client(intents=intents)

previous_words = csv.reader(open("src\\history.csv"))
appender = csv.writer(open("src\\history.csv"))

@client.event
async def on_ready():
    print("logged in")

@client.event
async def on_message(message):
    if message.author == client.user: #make sure the bot didn't send it
        return

    # look through each message and compare it
    

    if message.channel.name == consts.CHANNEL_NAME:
        # look through each message and compare it
        seen = False
        for item in previous_words:
            if item == message.content:
                seen = True

        if not seen:
            previous_words

        await message.channel.send('Hello!')
        await message.add_reaction(consts.RECYCLE_EMOJI)

token_file = open("src\\token.txt")
token = token_file.read()
client.run(token)
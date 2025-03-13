# This is a bot that takes all of the words said in a channel,
# and if anyone repeats a word, it reacts with a recycle emoji
import discord
import consts
import os

intents = discord.Intents.default() # enable most permissions
intents.message_content = True # allow bot to read messages

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("logged in")

@client.event
async def on_message(message):
    if message.author == client.user: #make sure the bot didn't send it
        return

    if message.channel.name == consts.CHANNEL_NAME:
        # look through each message and compare it
        seen = False
        last_letter_matches = False
        with open("src\\history.txt", "+br") as file:
            try:
                file.seek(-2, os.SEEK_END)
                while file.read(1) != b"\n":
                    file.seek(-2, os.SEEK_CUR)
            except OSError:
                file.seek(0)
            last_line = file.readline().decode()
            if last_line[-2:-1] == message.content.lower()[0]:
                last_letter_matches = True

        if not last_letter_matches:
            await message.add_reaction(consts.WRONG_EMOJI)
        else:
            with open("src\\history.txt") as previous_words:
                for item in previous_words:
                    if item[:-1] == message.content.lower():
                        seen = True

            if not seen:
                # add message to list
                with open("src\\history.txt", "a") as file:
                    file.write(message.content.lower() + "\n")
            else:
                await message.add_reaction(consts.RECYCLE_EMOJI)


token_file = open("src\\token.txt")
token = token_file.read()
client.run(token)
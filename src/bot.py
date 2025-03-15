# This is a bot that takes all of the words said in a channel,
# and if anyone repeats a word, it reacts with a recycle emoji
import discord
import consts
import os
import re

intents = discord.Intents.default() # enable most permissions
intents.message_content = True # allow bot to read messages

client = discord.Client(intents=intents)


def emote_removal(bad_text: str) -> str:
    """removes emote-like expressions from a string"""
    pattern = r'^[^:]+:[a-zA-Z_]+:[^:]+$'
    while bool(re.match(pattern, bad_text)):
        """bad string, has an emote in it, removing it"""
        # find a :
        first_colon = bad_text.find(":")
        
        # find a second colon, making sure its a valid emote along the way
        for j in range(first_colon+1, len(bad_text)):
            if not bad_text[j].isalpha or bad_text[j] != "_":
                # colon was not emote start, remove
                bad_text = bad_text[:first_colon] + bad_text[first_colon + 1:]
            elif bad_text[j] == ":":
                #found the end of our emote
                bad_text = bad_text[:first_colon] + bad_text[j + 1:]
    return bad_text
                

            






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
            last_line = emote_removal(file.readline().decode().lower())


            for i in range(1, len(last_line)+1):
                if last_line[-i].isalpha():
                    last_letter = last_line[-i]
                    break

            line_to_test = message.content.lower()

            first_letter = ""
            
            for i in range(len(line_to_test)):
                if line_to_test[i].isalpha():
                    first_letter = line_to_test[i]
                    break

            if last_letter == first_letter:
                last_letter_matches = True

        if not last_letter_matches:
            await message.add_reaction(consts.WRONG_EMOJI)
            log = "last letter was " + last_line[-1] + " you dingus"
            print(log)
        else:
            with open("src\\history.txt") as previous_words:
                for item in previous_words:
                    if item[:-1] == line_to_test:
                        seen = True

            if not seen:
                # add message to list
                with open("src\\history.txt", "a") as file:
                    line_to_save = ""
                    for i in range(len(line_to_test)):
                        if line_to_test[i].isalpha():
                            line_to_save += line_to_test[i]
                    file.write("\n" + line_to_save)
            else:
                await message.add_reaction(consts.RECYCLE_EMOJI)


token_file = open("src\\token.txt")
token = token_file.read()
client.run(token)
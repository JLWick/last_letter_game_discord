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
    pattern = r"^.*(:[a-zA-Z_~0-9]+:).*$"
    while bool(re.match(pattern, bad_text)):
        """bad string, has an emote in it, removing it"""
        # find a :
        first_colon = bad_text.find(":")

        
        # find a second colon, making sure its a valid emote along the way
        for j in range(first_colon+1, len(bad_text)):
            
            if bad_text[j] == ":":
                #found the end of our emote
                bad_text = bad_text[:first_colon] + bad_text[j + 1:]
                break
            elif not bad_text[j].isalpha() and bad_text[j] != "_":
                # colon was not emote start, remove
                bad_text = bad_text[:first_colon] + bad_text[first_colon + 1:]
                break

    # <emote:123098123098> style
    pattern = r"^.*(<.+>).*$"
    while bool(re.match(pattern, bad_text)):
        """bad string, has an emote in it, removing it"""
        # find a <
        emote_start = bad_text.find("<")

        #find a > after that
        emote_end = bad_text.find(">", emote_start)

        bad_text = bad_text[:emote_start] + bad_text[emote_end + 1:]


    return bad_text



def is_last_letter_matching(last_line: str, line_to_test: str) -> bool:
    last_letter_matches = False
    for i in range(1, len(last_line)+1):
        if last_line[-i].isalpha():
            last_letter = last_line[-i]
            break

    first_letter = ""

    for i in range(len(line_to_test)):
        if line_to_test[i].isalpha():
            first_letter = line_to_test[i]
            break

    if last_letter == first_letter:
        last_letter_matches = True

    return last_letter_matches

def is_seen_before(line_to_test: str) -> bool:
    seen = False

    with open("src\\history.txt") as previous_words:
                    for item in previous_words:
                        if item[:-1] == line_to_test:
                            seen = True

    return seen





@client.event
async def on_ready():
    print("logged in")

@client.event
async def on_message(message):
    if message.author == client.user: #make sure the bot didn't send it
        return

    if message.channel.name == consts.CHANNEL_NAME:

        with open("src\\history.txt", "+br") as file:
            try:
                file.seek(-2, os.SEEK_END)
                while file.read(1) != b"\n":
                    file.seek(-2, os.SEEK_CUR)
            except OSError:
                file.seek(0)
            last_line = file.readline().decode()

        line_to_test = emote_removal(message.content.lower())
        print(line_to_test)

        last_letter_matches = is_last_letter_matching(last_line, line_to_test)

        if not last_letter_matches:
            await message.add_reaction(consts.WRONG_EMOJI)
            log = "last letter was " + last_line[-1] + " you dingus"
            print(log)
        else:
            seen = is_seen_before(line_to_test)

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
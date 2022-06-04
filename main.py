import os
import datetime
import random
import discord
import pytz
import urllib.parse

import giphy_client
from giphy_client.rest import ApiException

from discord.ext import tasks
from wte import get_place

# global cruft
my_secret = my_secret = os.environ.get('TOKEN')
channel_id_general = 743673283878322230
channel_id_voice = 743673622664708217
intents = discord.Intents().default()
intents.members = True
client = discord.Client(intents=intents)
users_time = {}
google_search_string = 'https://www.google.com/search?&q='


def AZTimeNow():
    return datetime.datetime.now(pytz.timezone('US/Arizona'))


def IsSpam(author):
    retval = False
    now = AZTimeNow()
    if author in users_time:
        # 55 min debounce
        if (now - users_time[author]).total_seconds() / 60 < 55:
            retval = True

    users_time[author] = now
    return retval


@tasks.loop(minutes=1)
async def FridayOrSaturdayNightCheck():
    now = AZTimeNow()
    if now.weekday() == 4 or now.weekday() == 5:
        str = "@everyone IT'S\n"
        if now.hour == 12 + 7 and now.minute == 30:
            general = client.get_channel(channel_id_general)
            if now.weekday() == 4:
                str = f'{str} Friday NIGHT!!!'
            if now.weekday() == 5:
                str = f'{str} Saturday NIGHT!!!'
            voice = client.get_channel(channel_id_voice)
            for x in voice.members:
                str += f"{x.name} is ready!\n"
            await general.send(str)


# Determine if its one of the squad
def IsHudson(author):
    if author.startswith('hudxy') or author.startswith('QuarterPounder'):
        return True
    return False


def IsWally(author):
    if author.startswith('Zeke22') or author.startswith('King Wallace'):
        return True
    return False


def IsLaurence(author):
    if author.startswith('abigguyforyou'):
        return True
    return False


def IsBrandon(author):
    if author.startswith('Gene Parmesan'):
        return True
    return False


def IsJason(author):
    if author.startswith('jaxyc'):
        return True
    return False


def IsConnor(author):
    if author.startswith('CoClark'):
        return True
    return False


@client.event
async def on_ready():
    print(f'Logged in as {client.user}\n Time is {AZTimeNow()}')
    FridayOrSaturdayNightCheck.start()


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    # Author specific messages
    name = msg.author.name
    # if IsWally(name) and not IsSpam(name):
    #     await msg.channel.send('Literally no one cares, Wally...')

    # if IsConnor(name) and not IsSpam(name):
    #     await msg.channel.send('Connor is ALIVE')

    # if IsJason(name) and not IsSpam(name):
    # 		await msg.channel.send('Jason has the floor!')

    # if IsBrandon(name) and not IsSpam(name):
    # 		await msg.channel.send('Brandon needs to get good at Pokemon')

    # if IsLaurence(name) and not IsSpam(name):
    # 		await msg.channel.send('Hope your Wok isn\'t ruined!')

    # if IsHudson(name) and not IsSpam(name):
    #     await msg.channel.send('Never Trust Wally with Betting Advice')

    # !commands
    if msg.content.startswith('!yo'):
        api_key = '4FUDW4xORmITPqmh1FW3lNk9G4dezDfk'
        api_instance = giphy_client.DefaultApi()
        await msg.chanel.send('testing yo')
        try:
            api_response = api_instance.gifs_search_get(
                api_key, 'where\'s everyone at', limit=5, rating='g')
            lst = list(api_response.data)
            gif = random.choice(lst)

            await msg.chanel.send(gif.embed.url)

        except ApiException as e:
            print("exception calling api")

    if msg.content.startswith('!hello'):
        await msg.channel.send('Don\'t talk back to me...')

    if msg.content.startswith('!heyheyhey'):
        await msg.channel.send('IT\'S FAT ALBERT!')

    if msg.content.startswith('!wally'):
        await msg.channel.send('Is a bitch')

    if msg.content.startswith('!warn'):
        await msg.channel.send(f'{name} has initiated a 5 minute warning before starting a game!')

    if msg.content.startswith('!food') or msg.content.startswith('!what to eat') or msg.content.startswith('!wte'):
        x = msg.content.split()
        if len(x) > 1:
            zip_code = x[1]
            place_result = get_place(zip_code)
            if type(place_result) == type(""):
                url_encoded_search = urllib.parse.quote_plus(
                    place_result + ' ' + zip_code)
                await msg.channel.send(f'Eat at {place_result}!\n Google Search: {google_search_string + url_encoded_search}')
            else:
                await msg.channel.send('Something went wrong with the command, blame Laurence...')
        else:
            await msg.channel.send('Wrong format for command. Format:\n !<food, wte, what to eat> <zipcode>')


client.run(my_secret)

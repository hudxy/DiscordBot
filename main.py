import os
import discord
from discord.ext import tasks
import datetime
import pytz

# global cruft
my_secret = my_secret = os.environ.get('TOKEN')
channel_id_general = 743673283878322230
channel_id_voice = 743673622664708217
intents = discord.Intents().default()
intents.members = True
client = discord.Client(intents=intents)
users_time = {}


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
async def MondayNightCheck():
	now = AZTimeNow()
	if now.weekday() == 0 and now.hour == 12 + 8 and now.minute == 30:
		general = client.get_channel(channel_id_general)
		str = "@everyone IT'S MONDAY NIGHT!!!\n"
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
    MondayNightCheck.start()


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    # Author specific messages
    name = msg.author.name
    if IsWally(name) and not IsSpam(name):
        await msg.channel.send('Literally no one cares, Wally...')

    if IsConnor(name) and not IsSpam(name):
        await msg.channel.send('Connor is ALIVE')

    if IsJason(name) and not IsSpam(name):
    		await msg.channel.send('Jason has the floor!')

    if IsBrandon(name) and not IsSpam(name):
    		await msg.channel.send('Brandon needs to get good at Pokemon')

    if IsLaurence(name) and not IsSpam(name):
    		await msg.channel.send('Hope your Wok isn\'t ruined!')

    if IsHudson(name) and not IsSpam(name):
		    await msg.channel.send('Never Trust Wally with Betting Advice')

    # !commands
    if msg.content.startswith('!hello'):
        await msg.channel.send('Don\'t talk back to me...')

    if msg.content.startswith('!heyheyhey'):
        await msg.channel.send('IT\'S FAT ALBERT!')

    if msg.content.startswith('!wally'):
        await msg.channel.send('Is a bitch')
		
    if msg.content.startswith('!warn'):
      await msg.channel.send(f'{name} has initiated a 5 minute warning before starting a game!')


client.run(my_secret)

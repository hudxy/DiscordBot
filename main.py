import os
import datetime
import random
import discord
import pytz
import urllib.parse
import giphy_client
import psycopg2

from giphy_client.rest import ApiException
from discord.ext import tasks
from dotenv import load_dotenv
from wte import get_place

# global cruft
load_dotenv()

my_secret = os.environ.get('TOKEN')
DATABASE_URL = os.environ.get('DATABASE_URL')

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


@tasks.loop(minutes=1)
async def FridayVideo():
    now = AZTimeNow()
    if now.weekday() == 4:
        if now.hour == 12 and now.minute == 30:
            general = client.get_channel(channel_id_general)
            await general.send("https://www.youtube.com/watch?v=1AnG04qnLqI")


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

def getMovieList():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM movies""")
            result = cursor.fetchall()

        if result is None:
            # No movies in db
            print(f"{AZTimeNow()}: Access Movies Failed! No entries in db.")

            return False
        movies = []
        for x in result:
            # Movies DB: x[0] = (int) id, x[1] = (str) title, x[2] = (timestamp) created_on
            movies.append(str(x[1]))
        return movies

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error in transaction, reverting all changes using rollback ", error)
        conn.rollback()
 
    finally:
        # closing database connection.
        if conn:
            # closing connections
            cursor.close()
            conn.close()

def addMovie(title: str):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO movies(title, created_on) 
                VALUES (%(title)s,  CURRENT_TIMESTAMP)
                """, {
                'title': title
            })
            result = cursor.rowcount
        
        return result == 1 #success if row count from cursor is 1
    
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error in transaction, reverting all changes using rollback ", error)
        conn.rollback()
 
    finally:
        # closing database connection.
        if conn:
            conn.commit()
            # closing connections
            cursor.close()
            conn.close()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}\n Time is {AZTimeNow()}')
    FridayOrSaturdayNightCheck.start()
    FridayVideo.start()


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

    lowercase_msg = msg.content.lower()
    # !commands
    if lowercase_msg.startswith('!yo'):
        api_key = '4FUDW4xORmITPqmh1FW3lNk9G4dezDfk'
        api_instance = giphy_client.DefaultApi()
        param = lowercase_msg.split()
        searchQuery = 'where\'s everyone'
        if len(param) > 1:
            searchQuery = " ".join(param[1:])
        try:
            api_response = api_instance.gifs_search_get(
                api_key, searchQuery, limit=50)
            lst = list(api_response.data)
            gif = random.choice(lst)

            await msg.channel.send(gif.embed_url)

        except ApiException as e:
            print("exception calling api")
    
    if lowercase_msg.startswith('!byron'):
        await msg.channel.send("https://gfycat.com/lineddefenselessduckbillplatypus")

    if lowercase_msg.startswith('!bingbong'):
        await msg.channel.send("https://gfycat.com/vacantgorgeousbaiji")

    if lowercase_msg.startswith('!hello'):
        await msg.channel.send('Don\'t talk back to me...')

    if lowercase_msg.startswith('!heyheyhey'):
        await msg.channel.send('IT\'S FAT ALBERT!')

    if lowercase_msg.startswith('!wally'):
        await msg.channel.send('Is a bitch')

    if lowercase_msg.startswith('!warn'):
        await msg.channel.send(f'{name} has initiated a 5 minute warning before starting a game!')

    if lowercase_msg.startswith('!food') or lowercase_msg.startswith('!what to eat') or lowercase_msg.startswith('!wte'):
        x = lowercase_msg.split()
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
    # Watchlist command 
    if lowercase_msg.startswith('!watch'):
        command_list = lowercase_msg.split()
        if len(command_list) < 2:
            await msg.channel.send('Wrong format for command. Format:\n !watch <list>')
            return

        second_command = command_list[1]

        if second_command.startswith('list'):
            movies = getMovieList()
            string = f""
            for x in range(len(movies)):
                string += f"{x+1}. {movies[x]}\n"
            await msg.channel.send(string)
            return

        if second_command.startswith('add'):
            remaing_message = msg.content.split()[2:]
            title = " ".join(remaing_message)
            if addMovie(title):
                await msg.channel.send(f"{title} was added to the watchlist!")
            else:
                await msg.channel.send(f"There was a problem with adding to the watchlist...")
            return
        



client.run(my_secret)

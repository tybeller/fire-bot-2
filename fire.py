import discord
from discord import app_commands
from discord.ext import commands
import datetime 
from datetime import timezone, datetime, timedelta
from collections import defaultdict
from embed import create_embed, create_leaderboard_embed
from heapq import heapify, heappush, heappop
from dotenv import load_dotenv
import logging
import os


load_dotenv()

admin_id = int(os.getenv("ADMIN_ID"))

leaderboard_size = 3

intents = discord.Intents.default()
intents.reactions = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def sync(ctx):
    print("sync started")
    if ctx.author.id == admin_id:
        for guild in bot.guilds:
            print(f'syncing to guild', guild.id)

            await bot.tree.sync(guild=guild)
        print("Cmd tree synced")
    else:
        print("not ty")
        await ctx.response.send_message("You are not Ty")



@bot.tree.command(
    name="fire_weekly",
    description="Posts a leaderboard of the top fire reacted messages in the past week"
)
async def fire_weekly(interaction):
    if not interaction.user.id == admin_id:
        print("User ", ctx.author.display_name, " attempted to invoke weekly post")
        return
    try:
        print("fire weekly")
        channel = bot.get_channel(interaction.channel_id)
        
        print("awaiting")
        embeds = await build_embeds(interaction, channel)
        print("embeds complete")
       
        message = """
        # 🔥 WEEKLY FIRE REACT ROUNDUP 🔥
        ## Who got the most fire reacts this past week
        """
        print("message")

        await channel.send(content=message, embeds=embeds)


    except discord.NotFound:
        print("channel not found")
    except discord.Forbidden:
        print("channel forbidden")
    except discord.HTTPException as e:
        print("exception")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


async def build_embeds(interaction, channel):
    print("starting build embeds")
    current_datetime_utc = datetime.now(timezone.utc)
    one_week_ago_datetime_utc = current_datetime_utc - timedelta(weeks=1)
    
    #min heap. will take in tuples of (fire_count, message).
    message_min_heap = []
    heapify(message_min_heap) 

    #dictionary stores all fire reactions recieved by a user in the week
    fire_reacts_per_user = defaultdict(int)
    
    print("parsing messages")
    async for message in channel.history(before=current_datetime_utc, after=one_week_ago_datetime_utc, limit=None):
        for reaction in message.reactions:
            if reaction.emoji == "🔥":
                #when we have a message with fire reacts, push it into the heap sorted by react count
                heappush(message_min_heap, (reaction.count, message.id))
                #if the heap is greater than the leaderboard_size, remove the message with the least fire reacts.
                if len(message_min_heap) > leaderboard_size:
                    heappop(message_min_heap)
                
                #add fire reacts to user's count
                fire_reacts_per_user[message.author.display_name] += reaction.count
    
    #now our heap contains the messages with the most fire reacts in the past week.
    embeds = []
    print("creating embeds")
    while not len(message_min_heap) == 0:
        fire_count, message_id = heappop(message_min_heap)

        message = await channel.fetch_message(message_id)
        embeds.insert(0, create_embed(message, fire_count, len(message_min_heap)+1))
    
    #sort users by fire reactions
    leaderboard = ""
    print("leaderboard")
    for place, fire_tuple in enumerate(sorted(fire_reacts_per_user.items(), key=lambda item:item[1], reverse=True)):
        user, fire_count = fire_tuple
        place_ending = lambda n: str(n)+'tsnrhtdd'[n%5*(n%100^15>4>n%10)::4] #https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd?page=1&tab=scoredesc#tab-top

        prefix = ""
        if place + 1 == 1:
            prefix = "# "
        elif place + 1 == 2:
            prefix = "## "
        elif place + 1 == 3:
            prefix = "### "
        leaderboard += prefix + f'**{place_ending(place+1)}: {user}** - {fire_count}\n'
    embeds.insert(0, create_leaderboard_embed(leaderboard))
    return embeds



handler = logging.FileHandler(filename='discord,log', encoding='utf-8', mode='w')
bot.run(os.getenv("TOKEN"), log_handler=handler)

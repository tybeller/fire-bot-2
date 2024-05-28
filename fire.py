import discord
from discord import app_commands
from discord.ext import commands
import datetime 
from datetime import timezone, datetime, timedelta
from embed import create_embed
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
    try:
        print("start weekly")
        channel = bot.get_channel(interaction.channel_id)
        current_datetime_utc = datetime.now(timezone.utc)
        one_week_ago_datetime_utc = current_datetime_utc - timedelta(weeks=1)
        
        #min heap. will take in tuples of (fire_count, message).
        message_min_heap = []
        heapify(message_min_heap) 

        async for message in channel.history(before=current_datetime_utc, after=one_week_ago_datetime_utc):
            for reaction in message.reactions:
                if reaction.emoji == "🔥":
                    #when we have a message with fire reacts, push it into the heap sorted by react count
                    heappush(message_min_heap, (reaction.count, message.id))
                    #if the heap is greater than the leaderboard_size, remove the message with the least fire reacts.
                    if len(message_min_heap) > leaderboard_size:
                        heappop(message_min_heap)

        #now our heap contains the messages with the most fire reacts in the past week.
        embeds = []
        while not len(message_min_heap) == 0:
            fire_count, message_id = heappop(message_min_heap)

            message = await channel.fetch_message(message_id)
            embeds.insert(0, create_embed(message, fire_count, len(message_min_heap)+1))
        
        await channel.send(embeds=embeds)


    except discord.NotFound:
        print("channel not found")
    except discord.Forbidden:
        print("channel forbidden")
    except discord.HTTPException as e:
        print("exception")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


handler = logging.FileHandler(filename='discord,log', encoding='utf-8', mode='w')
bot.run(os.getenv("TOKEN"), log_handler=handler)

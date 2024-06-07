import discord
from datetime import datetime, timezone, timedelta

def create_leaderboard_embed(leaderboard_str):
    embed = discord.Embed(
        title = "🏆 **Leaderboard** 🏆",
        color=discord.Color.teal(),
        description=leaderboard_str
    )
    return embed

def create_embed(message, fire_count, rank):
    
    place_ending = lambda n: str(n)+'tsnrhtdd'[n%5*(n%100^15>4>n%10)::4] #https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd?page=1&tab=scoredesc#tab-top
    title = f'{place_ending(rank)} '
    color = discord.Color.yellow()

    if rank == 2:
        title += "🥈"
        color = discord.Color.blue()
    elif rank == 3:
        title += "🥉"
        color = discord.Color.red()
    else: 
        title += "🥇"
    title += ""

    description = None

    if message.content.strip() != "":
        description = "# " + message.content
    
    embed = discord.Embed(
        title = title,
        color = color,
        description = description
    )
    est = timezone(timedelta(hours=-5))

    message_datetime_est = message.created_at.astimezone(est)

    time_str = message_datetime_est.strftime("%I:%M %p")
    date_str = message_datetime_est.strftime("%m/%d/%y")

    embed.add_field(name="Time", value=time_str, inline=True)
    embed.add_field(name="Date", value=date_str, inline=True)
    embed.add_field(name="Link", value=f'[Jump To]({message.jump_url})', inline=True)
    embed.add_field(name="🔥 Reacts", value=fire_count, inline=False)

    
    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    #embed.set_thumbnail(url=message.author.display_avatar.url)
    
    if message.attachments:
        embed.set_image(url=message.attachments[0].url)
    
    return embed
    

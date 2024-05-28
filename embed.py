import discord

def create_embed(message, fire_count, rank):
    title = "🔥🔥🔥 MOST FYE 🔥🔥🔥"
    color = discord.Color.yellow()
    if rank == 2:
        title = "🔥🔥 SECOND MOST FYE 🔥🔥"
        color = discord.Color.blue()
    elif rank == 3:
        title = "🔥 THIRD MOST FYE 🔥"
        color = discord.Color.red()
    
    embed = discord.Embed(
        title = title,
        color = color,
        description = message.content
    )
    
    embed.add_field(name="🔥 Reacts", value=fire_count, inline=True)
    embed.add_field(name="Date", value=message.created_at.strftime("%m/%d/%Y, %H:%M:%S"), inline=True)
    
    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    embed.set_thumbnail(url=message.author.display_avatar.url)
    
    if message.attachments:
        embed.set_image(url=message.attachments[0].url)
    
    return embed
    

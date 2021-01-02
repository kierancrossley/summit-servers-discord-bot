import discord
import os
from os import chdir, makedirs, remove
from os.path import isfile, dirname, realpath
import random
import time
import asyncio
from discord.ext import commands
from discord.utils import get
from json import load, dump
import datetime

# In-file configuration

global_prefix = "."
welcome_channel_id = 654807115898159134
log_channel_id = 665652891725463583
status_message = "with the Summit community! | .help"
serverip = "51.75.174.11:27016"

modules = ["fun", "moderation", "administration"]

client = commands.Bot(command_prefix = global_prefix)
client.remove_command('help')

# On bot ready

@client.event
async def on_ready():
    print("===================================================================")
    print("Success! Bot has loaded and is ready for use. Logged in as:")
    print("User:", client.user.name + "#" + client.user.discriminator)
    print("UserID:", client.user.id)
    print("===================================================================")
    print("Current modules listed:", modules)
    print("===================================================================")

    channel = client.get_channel(log_channel_id)

    status_log = discord.Embed(
        title = f':robot: BOT STATUS',
        colour = discord.Colour.green()
    )

    status_log.add_field(name="Bot status:", value="Online", inline=True)

    await channel.send(embed=status_log)
    await client.change_presence(activity=discord.Game(name=status_message))

# On error

'''@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):

        author = ctx.message.author

        error_MissingRequiredArgument = discord.Embed(
            title = f':skull_crossbones: An error has occured.',
            description = "Please pass in all required fields!",
            colour = discord.Colour.red()
        )

        error_MissingRequiredArgument.set_footer(text=f'Errored by {author}', icon_url=ctx.author.avatar_url)

        error_MRA = await ctx.send(embed=error_MissingRequiredArgument, delete_after=5)

    if isinstance(error, commands.CommandNotFound):

        author = ctx.message.author

        error_CommandNotFound = discord.Embed(
            title = f':skull_crossbones: An error has occured.',
            description = "The command you ran was not found!",
            colour = discord.Colour.red()
        )

        error_CommandNotFound.set_footer(text=f'Errored by {author}', icon_url=ctx.author.avatar_url)

        await ctx.message.delete()
        error_CNF = await ctx.send(embed=error_CommandNotFound, delete_after=5)

    else:

        author = ctx.message.author

        error_Unknown = discord.Embed(
            title = f':skull_crossbones: An error has occured.',
            description = "An unknown error has occured. Please message the server owner.",
            colour = discord.Colour.red()
        )

        error_Unknown.set_footer(text=f'Errored by {author}', icon_url=ctx.author.avatar_url)

        await ctx.message.delete()
        error_U = await ctx.send(embed=error_Unknown, delete_after=5)'''

# Join and leave messages

@client.event
async def on_member_join(member):
    channel = client.get_channel(welcome_channel_id)
    role = discord.utils.get(member.guild.roles, name="👤 Guest")

    join = discord.Embed(
        title = f':wave: {member} has joined the server.',
        colour = discord.Colour.green()
    )

    # await member.send("Welcome!")
    await channel.send(embed=join)
    await member.add_roles(role)
    print(f'[WELCOME] {member} joined the server.')

@client.event
async def on_member_remove(member):
    channel = client.get_channel(welcome_channel_id)

    leave = discord.Embed(
        title = f':cry: {member} has left the server.',
        colour = discord.Colour.red()
    )

    # await member.send("Welcome!")
    await channel.send(embed=leave)
    print(f'[WELCOME] {member} left the server.')

# Ping command

@client.command()
async def ping(ctx):

    author = ctx.message.author

    ping_update = discord.Embed(
        title = ":ping_pong: PING",
        colour = discord.Colour.purple()
    )

    ping_update.add_field(name="Current ping:", value=f'{round(client.latency * 1000)}ms')
    ping_update.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)

    await ctx.message.delete()
    await ctx.send(embed=ping_update, delete_after=10)
    print(f'[PING] Current ping is {round(client.latency * 1000)}ms. Ran by {author}.')

# Help command

@client.command(pass_context=True)
async def help(ctx):

    author = ctx.message.author

    main = discord.Embed(
        title = ":question: MAIN HELP MENU",
        description = "The following commands are listed below.",
        colour = discord.Colour.red()
    )

    main.add_field(name=global_prefix+"help", value="Sends this help message.", inline=False)
    main.add_field(name=global_prefix+"ping", value="Check the connection to the server.", inline=False)
    main.add_field(name=global_prefix+"connect", value="Check players and connect to the server.", inline=False)

    fun = discord.Embed(
        title = ":8ball: FUN HELP MENU",
        description = "The following fun commands are listed below.",
        colour = discord.Colour.blue()
    )

    fun.add_field(name=global_prefix+"8ball", value="Ask the magic 8ball a queston.", inline=False)
    fun.add_field(name=global_prefix+"dice", value="Roll a dice!", inline=False)

    moderation = discord.Embed(
        title = ":hammer: MODERATION HELP MENU",
        description = "The following moderation commands are listed below.",
        colour = discord.Colour.green()
    )

    moderation.add_field(name=global_prefix+"purge", value="Clear a certain amount of messages.", inline=False)
    moderation.add_field(name=global_prefix+"mute", value="Mute a member.", inline=False)
    moderation.add_field(name=global_prefix+"unmute", value="Unmute a member.", inline=False)
    moderation.add_field(name=global_prefix+"kick", value="Kick a member from the Discord.", inline=False)
    moderation.add_field(name=global_prefix+"ban", value="Ban a member from the Discord.", inline=False)
    moderation.add_field(name=global_prefix+"unban", value="Unban a member from the Discord.", inline=False)
    moderation.add_field(name=global_prefix+"suggest", value="Suggest something to add.", inline=False)
    moderation.add_field(name=global_prefix+"serverinfo", value="View server information.", inline=False)

    administration = discord.Embed(
        title = ":briefcase: ADMINISTRATION HELP MENU",
        description = "The following administration commands are listed below.",
        colour = discord.Colour.orange()
    )

    administration.add_field(name=global_prefix+"load", value="Loads a module.", inline=False)
    administration.add_field(name=global_prefix+"unload", value="Unoads a module.", inline=False)
    administration.add_field(name=global_prefix+"reload", value="Reloads module.", inline=False)
    administration.add_field(name=global_prefix+"status", value="Sets the bot's status.", inline=False)
    administration.add_field(name=global_prefix+"embed", value="Embed a message.", inline=False)
    administration.add_field(name=global_prefix+"maintainance", value="Announce maintainance.", inline=False)

    notify_help = discord.Embed(
        title = ":inbox_tray: Please check your DMs.",
        colour = discord.Colour.red()
    )

    notify_help.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)

    await ctx.send(embed=notify_help)

    await author.send(embed=main)
    await author.send(embed=fun)
    await author.send(embed=moderation)
    await author.send(embed=administration)
    print(f'[HELP] Help command sent to {author}.')

# Connect

@client.command()
async def connect(ctx):
    image = f'https://cache.gametracker.com/server_info/{serverip}/banner_560x95.png?'
    author = ctx.message.author

    serverConnect = discord.Embed(
        title = f':zap: SERVER CONNECT',
        description = f'Click to connect: steam://connect/{serverip}',
        colour = discord.Colour.red()
    )

    serverConnect.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)
    serverConnect.set_image(url=image)

    await ctx.message.delete()
    await ctx.send(embed=serverConnect)
    print(f'[CONNECT] {author} ran the connect command.')

# Loading commands

@client.command()
@commands.has_any_role('root', '🏆 Community Owner', '🛡️ Community Manager')
async def load(ctx, extension):

    author = ctx.message.author
    extension = extension.lower()

    loadnotify_success = discord.Embed(
        title = f':white_check_mark: Loaded {extension}.',
        colour = discord.Colour.green()
    )

    loadnotify_success.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)

    loadnotify_failed = discord.Embed(
        title = f':skull_crossbones: Could not load {extension}.',
        description = "Error: module not found!",
        colour = discord.Colour.red()
    )

    loadnotify_failed.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)

    if extension in modules:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(embed=loadnotify_success)
    else:
        await ctx.send(embed=loadnotify_failed)
    print(f'[MODULE] {author} loaded {extension}.')

@client.command()
@commands.has_any_role('root', '🏆 Community Owner', '🛡️ Community Manager')
async def unload(ctx, extension):

    author = ctx.message.author
    extension = extension.lower()

    unloadnotify_success = discord.Embed(
        title = f':white_check_mark: Unloaded {extension}.',
        colour = discord.Colour.green()
    )

    unloadnotify_success.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)

    unloadnotify_failed = discord.Embed(
        title = f':skull_crossbones: Could not unload {extension}.',
        description = "Error: module not found!",
        colour = discord.Colour.red()
    )

    unloadnotify_failed.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)

    if extension in modules:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(embed=unloadnotify_success)
    else:
        await ctx.send(embed=unloadnotify_failed)
    print(f'[MODULE] {author} unloaded {extension}.')

@client.command()
@commands.has_any_role('root', '🏆 Community Owner', '🛡️ Community Manager')
async def reload(ctx, extension):

    author = ctx.message.author
    extension = extension.lower()

    reloadnotify_success = discord.Embed(
        title = f':white_check_mark: Reloaded {extension}.',
        colour = discord.Colour.green()
    )

    reloadnotify_success.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)

    reloadnotify_failed = discord.Embed(
         title = f':skull_crossbones: Could not reload {extension}.',
        description = "Error: module not found!",
        colour = discord.Colour.red()
    )

    reloadnotify_failed.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)

    if extension in modules:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(embed=reloadnotify_success)
    else:
        await ctx.send(embed=reloadnotify_failed)
    print(f'[MODULE] {author} reloaded {extension}.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# Running the bot

client.run(os.environ['BOT_TOKEN'])

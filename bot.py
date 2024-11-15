#importing discord and dotenv
import discord
from dotenv import load_dotenv
from discord.ext import commands as cmds

#import file manager
import os

#stating necessary intents of the bot (can view members)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

#grabs the discord token and servers from another file (.env)
load_dotenv(f'{os.path.dirname(os.path.realpath(__file__))}\\data\\.env')
TOKEN = os.getenv('DISCORD_TOKEN')

#sets the client to be a discord client with the chosen intents
boi = cmds.Bot(command_prefix='!',intents=intents)

@boi.command(aliases=["stop", "exit"], hidden=True)
@cmds.is_owner()
async def quit(ctx):
	await boi.close()

@boi.command(hidden=True)
@cmds.is_owner()
async def reload(ctx):
    await boi.reload_extension(f'cogs.secret_santa')

#This is for the example purposes only and should only be used for debugging
@boi.command()
async def sync(ctx: cmds.Context):
    # sync to the guild where the command was used
    boi.tree.copy_global_to(guild=ctx.guild)
    await boi.tree.sync(guild=ctx.guild)
    await ctx.send("Commands Synced", ephemeral=True)


#load command cogs
@boi.event
async def on_ready():
    await boi.load_extension('cogs.secret_santa')
    for boiGuild in boi.guilds:
        await boi.tree.sync(guild=boiGuild)
    print("\nAll Cogs Loaded")

try:
    print("\033[32mThe Boi rises.\033[0m")
    boi.run(TOKEN)
    print("\033[34mThe Boi is dead.\033[0m")
except TypeError:
    print('\033[1;31mMissing Token\nPlease create a .env file and add the line:\n"DISCORD_TOKEN={your bot token}"\033[0m')
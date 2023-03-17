import random

# Import discord.py library
import discord
from discord.ext import commands

# Create a bot instance
bot = commands.Bot(command_prefix="!")


@bot.command()
async def mafia_start(ctx):
    # Get the list of members in the voice channel of the author
    members = ctx.author.voice.channel.members
    # Check if there are at least 7 players
    if len(members) < 7:
        await ctx.send("Not enough players to start a game.")
        return
    # Shuffle the list of members
    random.shuffle(members)
    # Assign roles to each member based on their position in the list
    roles = ["Mafia", "Doctor", "Sheriff", "Jester",
             "Investigator", "Escort", "Townie"]
    for i, member in enumerate(members):
        role = roles[i % len(roles)]
        # Send a private message to each member with their role
        await member.send(f"Your role is {role}.")
    # Announce that the game has started and send instructions
    await ctx.send("The game has started. Check your DMs for your role. The night phase begins now. Mafia, choose someone to kill. Doctor, choose someone to heal. Sheriff, choose someone to investigate.")

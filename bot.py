# Import os and dotenv modules
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Import the discord module
import discord

# Create an instance of the client class
client = discord.Client(intents=discord.Intents(messages=True))

# Define an event handler for when the bot is ready
@client.event
async def on_ready():
    # Print a message to the terminal
    print(f"{client.user} has connected to Discord!")

# Define an event handler for when the bot receives a message
@client.event
async def on_message(message):
    # Ignore messages from bots or from itself
    if message.author.bot:
        return

    # Check if the message starts with "!hello"
    if message.content.startswith("!hello"):
        # Reply with "Hello, world!"
        await message.channel.send("Hello, world!")

# Run the bot using the token
client.run(os.getenv("DISCORD_TOKEN"))
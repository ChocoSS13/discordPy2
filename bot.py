# Import os and dotenv modules
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

import discord
import discord.ext.commands as commands

# Import random module for shuffling roles
import random
import TownOfSalem

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Define a list of possible roles for the game (based on Town of Salem)
ROLES = ['Мафия', 'Доктор', 'Детектив', 'Мирный', 'Шериф', 'Серийный убийца', 'Ведьма']

# Define a class for the game logic and state
class MafiaGame:
    # Initialize the game with the channel where it is played and an empty list of players
    def __init__(self, channel):
        self.channel = channel # The text channel where the game is played
        self.players = [] # A list of player objects who joined the game
        self.started = False # A boolean flag indicating if the game has started or not 
        self.phase = None # A string indicating the current phase of the game ('night' or 'day')
        self.day_count = 0 # An integer counting the number of days passed in the game 
        self.night_count = 0 # An integer counting the number of nights passed in the game 
        self.votes = {} # A dictionary mapping players to their votes during the day 
        self.targets = {} # A dictionary mapping players to their targets during the night 
        self.deaths = [] # A list of players who died during the night 
        self.winner = None # A string indicating the winner of the game ('mafia', 'town' or 'serial killer')

    # Add a player to the game if they are not already in it and the game has not started yet
    def add_player(self, player):
        # Check if the game has started or not
        if self.started:
            return 'Игра уже началась. Вы не можете присоединиться.'
        
        # Check if the player is already in the game or not
        if player in self.players:
            return 'Вы уже в игре.'
        
        # Add the player to the list of players and return a confirmation message
        self.players.append(player)
        return f'Вы присоединились к игре. Текущее количество игроков: {len(self.players)}'
    
    # Start the game if there are enough players and assign roles to them randomly 
    def start_game(self):
        # Check if there are enough players or not (at least 7)
        if len(self.players) < 7:
            return 'Недостаточно игроков для начала игры. Нужно минимум 7.'
        
        # Set the started flag to True and shuffle the roles list 
        self.started = True 
        random.shuffle(ROLES)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    # If the message starts with 'мафия старт', start a new game of mafia (based on https://github.com/aeternalis1/mafiabot)
    if message.content.startswith('мафия старт'):
        # Check if there is already a game running in this channel
        if hasattr(client, 'mafia_game') and client.mafia_game.channel == message.channel:
            await message.channel.send('Игра уже идет в этом канале.')
            return
        
        # Create a new game object and store it as an attribute of the client object (this allows only one game per bot instance)
        client.mafia_game = MafiaGame(message.channel)

        # Send a welcome message and instructions on how to join the game
        await message.channel.send('Новая игра в мафию началась! Чтобы присоединиться к игре, напишите "мафия присоединиться".')

client.run(os.getenv("DISCORD_TOKEN"))
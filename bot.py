import discord
import os

# Set up intents
intents = discord.Intents.default()
intents.message_content = True   # <-- critical so bot can read messages

# Create client with intents
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Respond to !ping
    if message.content == '!ping':
        await message.channel.send('pong')

# Run bot with token from environment variable
client.run(os.getenv("TOKEN"))

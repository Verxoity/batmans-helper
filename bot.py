import discord
from discord.ext import commands
import os

# --- Intents setup ---
intents = discord.Intents.default()
intents.message_content = True   # Needed to read messages
intents.members = True           # Needed for ban/kick/mute

# --- Bot setup ---
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# --- Commands ---

# Ping command
@bot.command()
async def ping(ctx):
    await ctx.send("pong")

# Ban command
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} has been banned. Reason: {reason}")

# Kick command
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} has been kicked. Reason: {reason}")

# Mute command (timeout for 10 minutes)
@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    duration = discord.utils.utcnow() + discord.timedelta(minutes=10)
    await member.timeout(until=duration, reason=reason)
    await ctx.send(f"{member} has been muted for 10 minutes. Reason: {reason}")

# --- Run bot ---
bot.run(os.getenv("TOKEN"))
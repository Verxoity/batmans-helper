import discord
from discord.ext import commands
import os
import datetime

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
async def ban(ctx, member: discord.Member, *, reason: str | None = None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned. Reason: {reason or 'No reason provided.'}")
    except discord.Forbidden:
        await ctx.send("I don’t have permission to ban that user.")
    except discord.HTTPException:
        await ctx.send("Ban failed due to an HTTP error.")

# Kick command
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str | None = None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked. Reason: {reason or 'No reason provided.'}")
    except discord.Forbidden:
        await ctx.send("I don’t have permission to kick that user.")
    except discord.HTTPException:
        await ctx.send("Kick failed due to an HTTP error.")

# Mute command (timeout for 10 minutes)
@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, *, reason: str | None = None):
    try:
        until = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        await member.timeout(until=until, reason=reason)
        await ctx.send(f"{member.mention} has been muted for 10 minutes. Reason: {reason or 'No reason provided.'}")
    except discord.Forbidden:
        await ctx.send("I don’t have permission to mute that user.")
    except discord.HTTPException:
        await ctx.send("Mute failed due to an HTTP error.")

# --- Run bot ---
bot.run(os.getenv("TOKEN"))
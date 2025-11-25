import discord
from discord.ext import commands
import os
import datetime

# --- Intents setup ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# --- Bot setup ---
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Commands loaded:", [c.name for c in bot.commands])

# --- Commands ---
@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned. Reason: {reason or 'No reason provided.'}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kicked. Reason: {reason or 'No reason provided.'}")

@bot.command(name="timeout")
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int = 10, *, reason=None):
    until = datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)
    await member.timeout(until=until, reason=reason)
    await ctx.send
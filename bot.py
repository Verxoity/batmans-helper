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

# --- Error handling ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing argument. Try `!kick @user reason` or `!ban @user reason`.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use `!help` to see available commands.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don’t have permission to use that command.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("❌ I’m missing required permissions to perform that action.")
    else:
        await ctx.send(f"❌ Error: {error}")

# --- Commands ---

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.mention} has been banned. Reason: {reason or 'No reason provided.'}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.mention
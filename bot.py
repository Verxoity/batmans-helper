import discord
from discord.ext import commands
import os
import datetime

# --- Intents ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# --- Bot setup ---
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print("✅ Commands loaded:", [c.name for c in bot.commands])

# --- Error handling ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing argument. Example: `!ban @user reason`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Couldn’t find that user. Mention them like `@username`.")
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
    await ctx.send(f"👢 {member.mention} has been kicked. Reason: {reason or 'No reason provided.'}")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int = 10, *, reason=None):
    until = datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)
    await member.timeout(until, reason=reason)
    await ctx.send(f"⏳ {member.mention} has been timed out for {minutes} minutes. Reason: {reason or 'No reason provided.'}")

# --- Run bot ---
bot.run(os.getenv("TOKEN"))

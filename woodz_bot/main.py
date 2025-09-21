    # main.py
import discord
from discord.ext import commands
from config import DISCORD_BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True  # Enable if you need message content

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# Example command
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Run bot
if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
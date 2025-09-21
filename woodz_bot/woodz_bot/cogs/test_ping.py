import discord
from discord.ext import commands
from discord import app_commands

class TestPing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="testping", description="Test ping command")
    async def testping(self, interaction: discord.Interaction):
        await interaction.response.send_message("pong (from test ping)")

async def setup(bot: commands.Bot):
    await bot.add_cog(TestPing(bot))
    print("✅ test_ping cog setup() ran")
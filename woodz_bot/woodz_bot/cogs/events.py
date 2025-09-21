import discord
from discord.ext import commands
from discord import app_commands
from woodz_bot.utils.card_data import card_data

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.event_active = False

    # /event add
    @app_commands.command(name="event_add", description="Add an event card 🎉")
    @app_commands.checks.has_role("Card Adders")
    async def event_add(self, interaction: discord.Interaction, idol: str, group: str, rarity: str, code: str, photo: str):
        card = {
            "idol": idol,
            "group": group,
            "rarity": rarity,
            "code": code,
            "photo": photo,
            "event": True
        }
        card_data.add_card(card)
        await interaction.response.send_message("✅ Event card added!", ephemeral=True)

    # /event start
    @app_commands.command(name="event_start", description="Start an event 🚀")
    @app_commands.checks.has_role("Admin")
    async def event_start(self, interaction: discord.Interaction):
        self.event_active = True
        await interaction.response.send_message("🎉 Event has started! Event cards can now drop.")

    # /event end
    @app_commands.command(name="event_end", description="End an event 🛑")
    @app_commands.checks.has_role("Admin")
    async def event_end(self, interaction: discord.Interaction):
        self.event_active = False
        await interaction.response.send_message("🛑 Event has ended. Event cards will no longer drop.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))
    print("✅ Events cog setup() ran")
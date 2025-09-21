    # woodz_bot/cogs/work.py
import discord
from discord import app_commands
from discord.ext import commands
import random
from woodz_bot.utils.cooldowns import cooldown_manager
from woodz_bot.utils.card_data import card_data  # ✅ use the same system as daily/drop

class Work(commands.Cog):
        def __init__(self, bot: commands.Bot):
            self.bot = bot

        @app_commands.command(name="work", description="Work to earn some leaves 🌲")
        async def work(self, interaction: discord.Interaction):
            user_id = str(interaction.user.id)

            # --- Cooldown check (5 min = 300s) ---
            on_cd, remaining = cooldown_manager.is_on_cooldown("work", user_id, 300)
            if on_cd:
                minutes, seconds = divmod(int(remaining), 60)
                return await interaction.response.send_message(
                    f"⏳ {interaction.user.mention}, you’re tired! "
                    f"Try again in **{minutes}m {seconds}s.**",
                    ephemeral=True
                )

            # --- Load profile from card_data ---
            profile = card_data.get_user_profile(user_id)

            # --- Random earnings ---
            amount = random.randint(80, 120)
            profile["currency"] = profile.get("currency", 0) + amount

            # --- Save back ---
            card_data.save_user_profile(user_id, profile)

            # --- Update cooldown ---
            cooldown_manager.update_last_used("work", user_id)

            # --- Success message ---
            await interaction.response.send_message(
                f"🌳 {interaction.user.mention}, you worked hard and earned "
                f"🍃 **{amount} leaves**!\n"
                f"💰 Your new balance: **{profile['currency']} leaves**"
            )


async def setup(bot: commands.Bot):
        await bot.add_cog(Work(bot))
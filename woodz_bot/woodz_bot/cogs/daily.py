    # daily.py
import discord
from discord import app_commands
from discord.ext import commands
import random
from woodz_bot.utils.card_data import card_data
from woodz_bot.utils.cooldowns import cooldown_manager


class Daily(commands.Cog):
        def __init__(self, bot):
            self.bot = bot

        @app_commands.command(name="daily", description="Claim your daily reward")
        async def daily(self, interaction: discord.Interaction):
            user_id = str(interaction.user.id)

            # -------------------------------
            # Cooldown check (24h = 86400s)
            # -------------------------------
            on_cd, remaining = cooldown_manager.is_on_cooldown("daily", user_id, 86400)
            if on_cd:
                hours, remainder = divmod(int(remaining), 3600)
                minutes, seconds = divmod(remainder, 60)
                embed = discord.Embed(
                    title="⏳ On Cooldown",
                    description=f"You already claimed your daily!\n"
                                f"Come back in **{hours}h {minutes}m {seconds}s**.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # -------------------------------
            # Rewards
            # -------------------------------
            reward_currency = 2000
            reward_logs = 30

            # Only rarity 4 cards should drop here
            reward_card = card_data.get_random_card(rarity="4")
            if not reward_card:
                reward_card = {"idol": "Random Idol", "group": "Random Group", "rarity": 4}

            # -------------------------------
            # Save to profile
            # -------------------------------
            profile = card_data.get_user_profile(user_id)
            profile["currency"] = profile.get("currency", 0) + reward_currency
            profile["logs"] = profile.get("logs", 0) + reward_logs
            profile.setdefault("cards", []).append(reward_card)

            card_data.save_user_profile(user_id, profile)

            # -------------------------------
            # Build response embed
            # -------------------------------
            rarity_display = "🌕" * int(reward_card.get("rarity", 1))
            embed = discord.Embed(
                title="🎁 Daily Reward",
                description=(
                    f"You claimed your daily reward!\n\n"
                    f"🍃 **+{reward_currency} currency**\n"
                    f"🪵 **+{reward_logs} logs**"
                ),
                color=discord.Color.green()
            )
            embed.add_field(
                name="🃏 Bonus Card",
                value=f"{reward_card.get('idol')} ({reward_card.get('group')})\n{rarity_display}",
                inline=False
            )
            if reward_card.get("photo"):
                embed.set_thumbnail(url=reward_card["photo"])

            await interaction.response.send_message(embed=embed)

            # -------------------------------
            # Update cooldown
            # -------------------------------
            cooldown_manager.update_last_used("daily", user_id)


async def setup(bot):
        await bot.add_cog(Daily(bot))
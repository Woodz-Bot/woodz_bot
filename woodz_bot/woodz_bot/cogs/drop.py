    # woodz_bot/cogs/drop.py
import random
import logging
import discord
from discord.ext import commands
from discord import app_commands

from woodz_bot.utils.card_data import card_data
from woodz_bot.utils.cooldowns import cooldown_manager

logger = logging.getLogger(__name__)


class Drop(commands.Cog):
        def __init__(self, bot: commands.Bot):
            self.bot = bot

        @app_commands.command(name="drop", description="Drop a random card 🎴")
        async def drop(self, interaction: discord.Interaction):
            """Drop a random card and save to user profile."""
            user_id = str(interaction.user.id)

            # -------------------------------
            # Cooldown check (5 min = 300s)
            # -------------------------------
            on_cd, remaining = cooldown_manager.is_on_cooldown("drop", user_id, 300)
            if on_cd:
                minutes, seconds = divmod(int(remaining), 60)
                embed = discord.Embed(
                    title="⏳ On Cooldown",
                    description=f"You must wait **{minutes}m {seconds}s** before using /drop again.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            try:
                # Defer so Discord won’t timeout the interaction
                await interaction.response.defer(thinking=True)

                # --- Check event status (robust) ---
                events_cog = self.bot.get_cog("Events") or self.bot.get_cog("events")
                if events_cog is None:
                    for c in self.bot.cogs.values():
                        if getattr(c, "event_active", False):
                            events_cog = c
                            break
                event_active = bool(getattr(events_cog, "event_active", False))

                # --- drop rates ---
                rarities = ["1", "2", "3", "4"]
                chances = [0.5, 0.3, 0.15, 0.05]
                chosen_rarity = random.choices(rarities, weights=chances, k=1)[0]

                # --- get all cards ---
                cards_source = None
                if hasattr(card_data, "get_all_cards"):
                    try:
                        cards_source = card_data.get_all_cards()  # type: ignore
                    except Exception:
                        cards_source = None
                if cards_source is None and hasattr(card_data, "cards"):
                    cards_source = getattr(card_data, "cards")
                if cards_source is None and getattr(card_data, "data", None):
                    cards_source = card_data.data.get("cards", [])

                if cards_source is None:
                    await interaction.followup.send(
                        "⚠️ Card storage not available. Contact the bot maintainer.",
                        ephemeral=True
                    )
                    return

                # --- filter by event ---
                if event_active:
                    available = [c for c in cards_source if c.get("event")]
                else:
                    available = [c for c in cards_source if not c.get("event")]

                # --- filter by rarity ---
                available = [c for c in available if str(c.get("rarity", "")).strip() == str(chosen_rarity)]
                if not available:
                    await interaction.followup.send(
                        "⚠️ No cards available for this rarity right now. Try again later.",
                        ephemeral=True
                    )
                    return

                # pick card
                card = random.choice(available)

                # Save to profile
                profile = card_data.get_user_profile(user_id)
                profile.setdefault("cards", [])
                profile["cards"].append(card)
                if hasattr(card_data, "save_user_profile"):
                    card_data.save_user_profile(user_id, profile)
                elif hasattr(card_data, "save_user_data"):
                    card_data.user_data[user_id] = profile
                    card_data.save_user_data()
                else:
                    logger.warning("card_data has no save method; user profile not persisted.")

                # --- rarity display ---
                rarity_value = str(card.get("rarity", "1"))
                try:
                    rarity_num = int(rarity_value)
                    rarity_display = "🌕" * max(1, rarity_num)
                except Exception:
                    rarity_display = rarity_value

                rarity_colors = {
                    "1": discord.Color.light_grey(),
                    "2": discord.Color.blue(),
                    "3": discord.Color.gold(),
                    "4": discord.Color.purple()
                }
                embed_color = rarity_colors.get(rarity_value, discord.Color.default())

                # embed
                embed = discord.Embed(title="🎴 A card has dropped!", color=embed_color)
                if card.get("photo"):
                    embed.set_image(url=card["photo"])
                embed.add_field(name="Name", value=card.get("idol", "Unknown"), inline=False)
                embed.add_field(name="Group", value=card.get("group", "Unknown"), inline=False)
                embed.add_field(name="Rarity", value=rarity_display, inline=False)
                embed.add_field(name="Code", value=str(card.get("code", "N/A")), inline=False)

                await interaction.followup.send(embed=embed)

                # -------------------------------
                # Update cooldown
                # -------------------------------
                cooldown_manager.update_last_used("drop", user_id)

            except Exception as exc:
                logger.exception("Error in /drop command")
                try:
                    await interaction.followup.send(
                        "❌ An error occurred while processing the drop. Check the bot console.",
                        ephemeral=True
                    )
                except Exception:
                    try:
                        await interaction.response.send_message(
                            "❌ An error occurred while processing the drop. Check the bot console.",
                            ephemeral=True
                        )
                    except Exception:
                        pass

        async def cog_load(self):
            GUILD_ID = 1413243368711917609
            try:
                self.bot.tree.add_command(self.drop, guild=discord.Object(id=GUILD_ID))
            except Exception:
                try:
                    self.bot.tree.add_command(self.drop)
                except Exception as e:
                    logger.exception("Failed to add drop command to tree: %s", e)


async def setup(bot: commands.Bot):
        await bot.add_cog(Drop(bot))
        logger.info("Drop cog setup ran")
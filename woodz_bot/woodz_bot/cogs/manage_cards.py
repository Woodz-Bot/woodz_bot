import discord
from discord.ext import commands
from discord import app_commands
from woodz_bot.utils.card_data import card_data
import json
import os


class ManageCards(commands.Cog):
        def __init__(self, bot: commands.Bot):
            self.bot = bot
           
        @app_commands.command(name="addcard", description="Add a new card (Card Adder Role Only)")
        async def addcard(
            self,
            interaction: discord.Interaction,
            idol: str,
            group: str,
            rarity: str,
            code: str,
            photo: str = "https://via.placeholder.com/150"
        ):
            role_id = 1418338132239192224  # ✅ Card Adder role ID
            log_channel_id = 1418338132239192224  # 🔄 replace with your staff log channel ID

            # Make sure we’re in a guild
            if interaction.guild is None:
                await interaction.response.send_message(
                    "❌ This command can only be used inside a server.",
                    ephemeral=True
                )
                return

            # Get Member object safely
            member = interaction.guild.get_member(interaction.user.id)
            if member is None:
                await interaction.response.send_message(
                    "⚠️ Could not verify your roles (are you in the server?).",
                    ephemeral=True
                )
                return

            # Role / Admin check
            has_role = any(role.id == role_id for role in member.roles)
            if not has_role and not member.guild_permissions.administrator:
                await interaction.response.send_message(
                    "❌ You do not have permission to use this command.",
                    ephemeral=True
                )
                return

            # Build card
            card = {
                "idol": idol,
                "group": group,
                "rarity": rarity,
                "code": code,
                "photo": photo,
                "added_by": str(interaction.user.id),
            }
            card_data.add_card(card)

            # Confirmation embed
            embed = discord.Embed(
                title="✅ Card Added!",
                description=f"**{idol}** ({rarity}) from **{group}** added successfully.",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=photo)
            await interaction.response.send_message(embed=embed, ephemeral=True)

            # Staff log embed
            log_channel = interaction.guild.get_channel(log_channel_id)
            if isinstance(log_channel, discord.TextChannel):
                log_embed = discord.Embed(
                    title="📝 Card Added",
                    description=f"**{idol}** ({rarity}) from **{group}**",
                    color=discord.Color.orange()
                )
                log_embed.set_thumbnail(url=photo)
                log_embed.add_field(name="Code", value=code)
                log_embed.add_field(name="Added By", value=interaction.user.mention)
                await log_channel.send(embed=log_embed)

CARDS_FILE = "cards.json"

def load_cards():
        if not os.path.exists(CARDS_FILE):
            return []
        with open(CARDS_FILE, "r") as f:
            return json.load(f)

async def cog_load(self):
            GUILD_ID = 1413243368711917609  # replace with your server ID
            self.bot.tree.add_command(self.addcard, guild=discord.Object(id=GUILD_ID))


async def setup(bot: commands.Bot):
        await bot.add_cog(ManageCards(bot))
        print("✅ ManageCards cog setup() ran")
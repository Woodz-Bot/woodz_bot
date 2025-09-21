import discord
from discord import app_commands
from discord.ext import commands

from woodz_bot.utils.card_data import card_data
from woodz_bot.utils.cooldowns import cooldown_manager
from typing import Optional


class Profile(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # /inventory
    @app_commands.command(name="inventory",
                          description="View your card inventory 📦")
    async def inventory(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        profiles = card_data.load_profiles()
        profile = profiles.get(user_id, {
            "currency": 0,
            "logs": 0,
            "cards": []
        })

        cards = profile.get("cards", [])
        if not cards:
            return await interaction.response.send_message(
                "📭 Your inventory is empty.")

        description_lines = []
        for i, card in enumerate(cards, start=1):
            moons = "🌕" * int(card.get("rarity", 1))
            description_lines.append(
                f"**{i}. {card.get('idol','Unknown')} ({moons})**\n"
                f"Group: {card.get('group','Unknown')}\n"
                f"Code: {card.get('code','N/A')}\n")

        embed = discord.Embed(
            title=f"{interaction.user.display_name}'s Inventory",
            description="\n".join(description_lines),
            color=discord.Color.blurple())
        await interaction.response.send_message(embed=embed)

    # /profile_edit
    @app_commands.command(name="profile_edit",
                          description="Set favorite card and bio")
    async def profile_edit(self,
                           interaction: discord.Interaction,
                           favorite_code: Optional[str] = None,
                           bio: Optional[str] = None):
        user_id = str(interaction.user.id)
        profiles = card_data.load_profiles()
        profile = profiles.get(user_id, {
            "currency": 0,
            "logs": 0,
            "cards": []
        })

        if favorite_code:
            if not any(
                    c.get("code") == favorite_code
                    for c in profile.get("cards", [])):
                return await interaction.response.send_message(
                    "❌ You don't own that card.")
            profile["favorite_card"] = favorite_code

        if bio is not None:
            if len(bio) > 500:
                return await interaction.response.send_message(
                    "❌ Bio too long (max 500).")
            profile["bio"] = bio

        profiles[user_id] = profile
        card_data.save_profiles(profiles)

        await interaction.response.send_message("✅ Profile updated!")

    # /profile
    @app_commands.command(name="profile", description="View your profile 📜")
    async def profile(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        profiles = card_data.load_profiles()
        profile = profiles.get(user_id, {
            "currency": 0,
            "logs": 0,
            "cards": []
        })

        embed = discord.Embed(
            title=f"{interaction.user.display_name}'s Profile",
            color=discord.Color.blurple())
        embed.set_thumbnail(url=interaction.user.display_avatar.url)

        embed.add_field(name="📝 Bio",
                        value=profile.get("bio", "No bio set."),
                        inline=False)
        embed.add_field(name="🍃 Balance",
                        value=str(profile.get("currency", 0)))
        embed.add_field(name="🪵 Logs", value=str(profile.get("logs", 0)))
        embed.add_field(name="🌙 Cards",
                        value=str(len(profile.get("cards", []))))

        fav_code = profile.get("favorite_card")
        if fav_code:
            fav = next((c for c in profile.get("cards", [])
                        if c.get("code") == fav_code), None)
            if fav:
                moons = "🌕" * int(fav.get("rarity", 1))
                embed.add_field(name="⭐ Favorite Card",
                                value=f"**{fav.get('idol','Unknown')}**\n"
                                f"Group: {fav.get('group','Unknown')}\n"
                                f"Rarity: {moons}\n"
                                f"Code: {fav.get('code','N/A')}",
                                inline=False)
                if fav.get("photo"):
                    embed.set_image(url=fav["photo"])
            else:
                embed.add_field(name="⭐ Favorite Card",
                                value=fav_code,
                                inline=False)
        else:
            embed.add_field(name="⭐ Favorite Card", value="None", inline=False)

        await interaction.response.send_message(embed=embed)

    # /view
    @app_commands.command(name="view", description="View a card you own 🔎")
    async def view(self, interaction: discord.Interaction, code: str):
        user_id = str(interaction.user.id)
        profiles = card_data.load_profiles()
        profile = profiles.get(user_id, {
            "currency": 0,
            "logs": 0,
            "cards": []
        })

        matching = [
            c for c in profile.get("cards", []) if c.get("code") == code
        ]
        if not matching:
            return await interaction.response.send_message(
                "❌ You don't own this card.")

        card = matching[0]
        rarity = str(card.get("rarity", "1"))
        moons = "🌕" * (int(rarity) if rarity.isdigit() else 1)

        embed = discord.Embed(title=f"🔎 {card.get('idol','Unknown')}",
                              color=discord.Color.green())
        embed.add_field(name="Group", value=card.get("group", "Unknown"))
        embed.add_field(name="Rarity", value=moons)
        embed.add_field(name="Code", value=card.get("code", "N/A"))
        embed.add_field(name="Amount Owned", value=str(len(matching)))
        if card.get("photo"):
            embed.set_image(url=card["photo"])

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Profile(bot))
    print("✅ Profile cog loaded")

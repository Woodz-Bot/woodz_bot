import discord
from discord.ext import commands
from discord import app_commands
import time

from woodz_bot.utils.cooldowns import cooldown_manager


class Cooldowns(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cooldown", description="Check your cooldowns ⏳")
    async def cooldown(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)

        # Helper to format cooldown
        def format_cd(cmd: str, duration: int) -> str:
            on_cd, remaining = cooldown_manager.is_on_cooldown(cmd, user_id, duration)
            if on_cd:
                minutes, seconds = divmod(int(remaining), 60)
                hours, minutes = divmod(minutes, 60)
                if hours > 0:
                    return f"{hours}h {minutes}m {seconds}s left"
                elif minutes > 0:
                    return f"{minutes}m {seconds}s left"
                else:
                    return f"{seconds}s left"
            return "Ready ✅"

        # Cooldown statuses
        work_status = format_cd("work", 300)      # 5m
        daily_status = format_cd("daily", 86400) # 24h
        drop_status = format_cd("drop", 300)     # 5m

        embed = discord.Embed(
            title=f"⏳ Cooldowns for {interaction.user.display_name}",
            color=discord.Color.green()
        )
        embed.add_field(name="💼 Work", value=work_status, inline=False)
        embed.add_field(name="🎁 Daily", value=daily_status, inline=False)
        embed.add_field(name="🪂 Drop", value=drop_status, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Cooldowns(bot))
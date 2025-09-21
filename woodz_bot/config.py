import os

# Load your Discord bot token from environment variables
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not DISCORD_BOT_TOKEN:
    raise ValueError("No DISCORD_BOT_TOKEN found in environment variables!")

# Role ID that can use /cardadd
ADMIN_ROLE_ID = 1418338132239192224

# Cooldowns in seconds
DROP_COOLDOWN = 300      # 5 min
WORK_COOLDOWN = 300      # 5 min
DAILY_BOOST_DURATION = 3600  # 1 hour

DAILY_REWARD = {
    "leaves": 2000,
    "logs": 30
}
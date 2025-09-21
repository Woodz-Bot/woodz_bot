import time

class CooldownManager:
    def __init__(self):
        # {command_name: {user_id: last_used_time}}
        self.cooldowns = {}

    def is_on_cooldown(self, command: str, user_id: str, cooldown_seconds: int):
        now = time.time()
        user_last = self.cooldowns.get(command, {}).get(user_id, 0)
        remaining = cooldown_seconds - (now - user_last)
        return remaining > 0, max(0, remaining)

    def update_last_used(self, command: str, user_id: str):
        now = time.time()
        if command not in self.cooldowns:
            self.cooldowns[command] = {}
        self.cooldowns[command][user_id] = now


# ✅ shared instance for the whole bot
cooldown_manager = CooldownManager()
import json
import os
from typing import Dict, Any

class UserData:
        def __init__(self, filename: str = "users.json"):
            self.filename = filename
            self.users: Dict[str, Any] = {}
            self.load()

        # ---------------------------
        # Load / Save user data
        # ---------------------------
        def load(self):
            if os.path.exists(self.filename):
                try:
                    with open(self.filename, "r", encoding="utf-8") as f:
                        self.users = json.load(f)
                    print(f"📂 Loaded {len(self.users)} user profiles")
                except Exception as e:
                    print(f"⚠️ Failed to load {self.filename}: {e}")
            else:
                self.users = {}

        def save(self):
            try:
                with open(self.filename, "w", encoding="utf-8") as f:
                    json.dump(self.users, f, indent=4, ensure_ascii=False)
                print(f"💾 Saved {len(self.users)} user profiles")
            except Exception as e:
                print(f"⚠️ Failed to save {self.filename}: {e}")

        # ---------------------------
        # User profile management
        # ---------------------------
        def get_profile(self, user_id: str) -> Dict[str, Any]:
            if user_id not in self.users:
                self.users[user_id] = {
                    "bio": "No bio set.",
                    "favorite_card": None,
                    "currency": 0,
                    "logs": 0,
                    "cards": []
                }
                self.save()
            return self.users[user_id]

        def save_profile(self, user_id: str, profile: Dict[str, Any]):
            self.users[user_id] = profile
            self.save()


    # Shared instance
user_data = UserData()
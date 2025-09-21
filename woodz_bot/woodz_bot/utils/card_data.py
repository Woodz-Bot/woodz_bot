import json
import os
import random
from typing import Dict, Any, Optional, List

class CardData:
    def __init__(self, filename="cards.json", user_filename="users.json"):
        self.filename = filename              # cards.json
        self.user_filename = user_filename    # users.json
        self.cards: List[Dict[str, Any]] = [] # all card definitions
        self.data: Dict[str, Any] = {"cards": []}
        self.user_data: Dict[str, Any] = {}   # all user profiles

        self.load_data()
        self.load_user_data()

    # -------------------------------
    # Load / Save card definitions
    # -------------------------------
    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                    self.cards = self.data.get("cards", [])
                print(f"✅ Loaded {len(self.cards)} cards from {self.filename}")
            except Exception as e:
                print(f"⚠️ Failed to load {self.filename}: {e}")

    def save_data(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            print(f"💾 Saved {len(self.cards)} cards to {self.filename}")
        except Exception as e:
            print(f"⚠️ Failed to save {self.filename}: {e}")

    # -------------------------------
    # Load / Save user data
    # -------------------------------
    def load_user_data(self):
        if os.path.exists(self.user_filename):
            try:
                with open(self.user_filename, "r", encoding="utf-8") as f:
                    self.user_data = json.load(f)
            except Exception as e:
                print(f"⚠️ Failed to load {self.user_filename}: {e}")

    def save_user_data(self):
        try:
            with open(self.user_filename, "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Failed to save {self.user_filename}: {e}")

    # -------------------------------
    # User profile helpers
    # -------------------------------
    def get_user_profile(self, user_id: str) -> dict:
        if user_id not in self.user_data:
            self.user_data[user_id] = {"currency": 0, "logs": 0, "cards": []}
        return self.user_data[user_id]

    def save_user_profile(self, user_id: str, profile: dict):
        self.user_data[user_id] = profile
        self.save_user_data()

    # -------------------------------
    # Card utilities
    # -------------------------------
    def add_card(self, card: Dict[str, Any]):
        self.cards.append(card)
        self.data["cards"] = self.cards
        self.save_data()

    def get_random_card(self, rarity: str) -> Optional[Dict[str, Any]]:
        available = [c for c in self.cards if c.get("rarity") == rarity]
        if not available:
            return None
        return random.choice(available)

    # -------------------------------
    # Backwards compatibility wrappers
    # -------------------------------
    def load_profiles(self) -> Dict[str, Any]:
        """Alias for old code that expected load_profiles()."""
        return self.user_data

    def save_profiles(self, profiles: Dict[str, Any]):
        """Alias for old code that expected save_profiles()."""
        self.user_data = profiles
        self.save_user_data()


# ✅ single shared instance
card_data: "CardData" = CardData()
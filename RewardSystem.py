import random
from Config import REWARD_SYSTEM, STICKER_COLLECTION

class RewardSystem:
    def __init__(self):
        self.sticker_collection = STICKER_COLLECTION.copy()
        self.games_played_today = 0
        self.total_stars_earned = 0
        self.player_stats = {
            "total_games_played": 0,
            "total_questions_answered": 0,
            "total_correct_answers": 0,
            "favorite_category": "",
            "best_score": 0
        }
        self.category_stats = {}

    def calculate_stars(self, percentage):
        """Menghitung bintang berdasarkan persentase score."""
        if percentage == 100:
            return REWARD_SYSTEM["perfect_score"]
        elif percentage >= 80:
            return REWARD_SYSTEM["excellent_score"]
        elif percentage >= 60:
            return REWARD_SYSTEM["good_score"]
        else:
            return REWARD_SYSTEM["nice_try"]

    def check_sticker_unlock(self):
        """Cek apakah dapat stiker baru."""
        if self.games_played_today >= REWARD_SYSTEM["sticker_unlock_threshold"]:
            locked_stickers = [sid for sid, data in self.sticker_collection.items() 
                             if not data["unlocked"]]
            if locked_stickers:
                sticker_id = random.choice(locked_stickers)
                self.sticker_collection[sticker_id]["unlocked"] = True
                self.games_played_today = 0
                return self.sticker_collection[sticker_id]["name"]
        return None

    def update_player_stats(self, category, score, total_questions):
        """Update statistik pemain."""
        self.player_stats["total_games_played"] += 1
        self.player_stats["total_questions_answered"] += total_questions
        self.player_stats["total_correct_answers"] += score
        
        # Update best score
        percentage = (score / total_questions) * 100
        if percentage > self.player_stats["best_score"]:
            self.player_stats["best_score"] = percentage
        
        # Update favorite category
        self.category_stats[category] = self.category_stats.get(category, 0) + 1
        if self.category_stats:
            self.player_stats["favorite_category"] = max(self.category_stats, key=self.category_stats.get)
        else:
            self.player_stats["favorite_category"] = "Belum ada"

    def get_sticker_progress(self):
        """Mendapatkan progress menuju stiker berikutnya."""
        games_to_next = REWARD_SYSTEM["sticker_unlock_threshold"] - self.games_played_today
        unlocked_count = sum(1 for data in self.sticker_collection.values() if data["unlocked"])
        total_count = len(self.sticker_collection)
        
        return games_to_next, unlocked_count, total_count

    def get_accuracy(self):
        """Menghitung akurasi pemain."""
        if self.player_stats["total_questions_answered"] > 0:
            return (self.player_stats["total_correct_answers"] / self.player_stats["total_questions_answered"]) * 100
        return 0
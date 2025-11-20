# --- PENGATURAN GAMBAR ---
QUESTION_IMAGE_WIDTH = 250
QUESTION_IMAGE_HEIGHT = 200

# --- PENGATURAN GAME ---
MAX_QUESTIONS_PER_GAME = 10  # Maksimal soal per game
MIN_QUESTIONS_FOR_GAME = 3   # Minimal soal untuk bisa main

# --- PENGATURAN WARNA (TEMA ALAM: KREM & HIJAU) ---
WARNA_LATAR = "#F5F5DC"          # Beige (Krem)
WARNA_TOMBOL_DEFAULT = "#8FBC8F" # DarkSeaGreen (Hijau lumut)
WARNA_TOMBOL_BENAR = "#77DD77"   # Pastel Green
WARNA_TOMBOL_SALAH = "#FF6961"   # Pastel Red
WARNA_TEKS_TOMBOL = "#FFFFFF"   # Putih (agar kontras di tombol hijau)
WARNA_TEKS_JUDUL = "#006400"    # DarkGreen (Hijau Tua)
WARNA_TEKS_BIASA = "#3A3B3C"    # Hitam arang (untuk teks soal)

# --- REWARD SYSTEM ---
REWARD_SYSTEM = {
    "perfect_score": "⭐️⭐️⭐️⭐️⭐️",      # 5 bintang untuk score 100%
    "excellent_score": "⭐️⭐️⭐️⭐️",       # 4 bintang untuk score 80-99%
    "good_score": "⭐️⭐️⭐️",              # 3 bintang untuk score 60-79%
    "nice_try": "⭐️⭐️",                  # 2 bintang untuk score <60%
    "sticker_unlock_threshold": 3        # Main 3 game dapat stiker
}

STICKER_COLLECTION = {
    "math_master": {"name": "Jago Matematika", "image": "stickers/math.png", "unlocked": False},
    "animal_expert": {"name": "Pakar Hewan", "image": "stickers/animal.png", "unlocked": False},
    "color_genius": {"name": "Jago Warna", "image": "stickers/color.png", "unlocked": False},
    "shape_pro": {"name": "Ahli Bentuk", "image": "stickers/shape.png", "unlocked": False},
    "speed_king": {"name": "Raja Cepat", "image": "stickers/speed.png", "unlocked": False},
    "nature_lover": {"name": "Pencinta Alam", "image": "stickers/nature.png", "unlocked": False},
    "super_reader": {"name": "Pembaca Hebat", "image": "stickers/reading.png", "unlocked": False},
    "creative_mind": {"name": "Anak Kreatif", "image": "stickers/creative.png", "unlocked": False}
}

# --- SOUND PATHS ---
PATH_SUARA_BENAR = "Sound/correct.mp3"
PATH_SUARA_SALAH = "Sound/salah.mp3"
PATH_SUARA_STIKER = "Sound/sticker_unlock.mp3"
PATH_SUARA_BINTANG = "Sound/star_reward.mp3"

PATH_MUSIK_MENU = "Sound/Cuckoo Clock.mp3"
PATH_MUSIK_GAMBAR = "Sound/Kevin MacLeod_ Barroom Ballet.mp3"
PATH_MUSIK_UMUM = "Sound/Musik backsound instrumen ceria (NoCopyright) Gratis (Happy Instrumental) Sand Castle.mp3"
PATH_MUSIK_HEWAN = "Sound/Super Mario Bros. Theme Song.mp3"
PATH_MUSIK_MATEMATIKA = "Sound/The Green Orbs - After School Jamboree.mp3"
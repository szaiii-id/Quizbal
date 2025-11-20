import random
from PIL import Image, ImageTk
import os
from Config import *

class GameManager:
    def __init__(self, database, sound_manager):
        self.database = database
        self.sound_manager = sound_manager
        self.current_quiz_data = []
        self.current_question = 0
        self.score = 0
        self.question_image_reference = None

    def start_quiz(self, game_type_key, all_quizzes):
        """Memulai kuis baru."""
        default_questions = list(all_quizzes.get(game_type_key, []))
        custom_questions = self.database.get_custom_questions(game_type_key)
        
        combined = default_questions + custom_questions

        if not combined:
            return False, "Game ini belum memiliki soal."
            
        # Cek apakah ada cukup soal
        if len(combined) < MIN_QUESTIONS_FOR_GAME:
            return False, f"Game ini hanya memiliki {len(combined)} soal. Minimal {MIN_QUESTIONS_FOR_GAME} soal untuk bisa bermain."

        # Set background music
        music_map = {
            "gambar": PATH_MUSIK_GAMBAR,
            "umum": PATH_MUSIK_UMUM, 
            "hewan": PATH_MUSIK_HEWAN,
            "matematika": PATH_MUSIK_MATEMATIKA
        }
        
        music_file = music_map.get(game_type_key, PATH_MUSIK_UMUM)
        self.sound_manager.play_bgm(music_file)

        # GUNAKAN SEMUA SOAL YANG TERSEDIA (MAX 10)
        num_questions = min(MAX_QUESTIONS_PER_GAME, len(combined))
        self.current_quiz_data = random.sample(combined, num_questions)
        self.current_question = 0
        self.score = 0
        
        return True, f"Game dimulai dengan {num_questions} soal!"

    def get_current_question(self):
        """Mendapatkan soal saat ini."""
        if self.current_question < len(self.current_quiz_data):
            return self.current_quiz_data[self.current_question]
        return None

    def display_question_image(self, image_label):
        """Menampilkan gambar soal."""
        self.question_image_reference = None
        data = self.get_current_question()
        
        if not data:
            return
            
        q_image_file = data.get("question_image")
        if q_image_file and os.path.exists(q_image_file):
            try:
                img = Image.open(q_image_file)
                img = img.resize((QUESTION_IMAGE_WIDTH, QUESTION_IMAGE_HEIGHT), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                image_label.config(image=photo)
                self.question_image_reference = photo
            except: 
                image_label.config(image="")
        else: 
            image_label.config(image="")

    def check_answer(self, selected_index):
        """Memeriksa jawaban dan memberikan feedback."""
        data = self.get_current_question()
        if not data:
            return False, None

        selected_option = data["options"][selected_index]
        correct_answer = data["answer"]
        
        if selected_option == correct_answer:
            self.score += 1
            self.sound_manager.play_sound_effect("correct")
            return True, "Hore! Benar! 👍"
        else:
            self.sound_manager.play_sound_effect("wrong")
            return False, "Oops, Salah!"

    def get_correct_answer_index(self):
        """Mendapatkan index jawaban yang benar."""
        data = self.get_current_question()
        if not data:
            return -1
            
        correct_answer = data["answer"]
        options = data["options"]
        
        try:
            return options.index(correct_answer)
        except:
            return -1

    def next_question(self):
        """Pindah ke soal berikutnya."""
        self.current_question += 1
        return self.current_question < len(self.current_quiz_data)

    def get_results(self):
        """Mendapatkan hasil kuis."""
        total_questions = len(self.current_quiz_data)
        score_percentage = (self.score / total_questions) * 100 if total_questions > 0 else 0
        
        return {
            "score": self.score,
            "total_questions": total_questions,
            "percentage": score_percentage
        }

    def reset_quiz(self):
        """Reset state kuis."""
        self.current_quiz_data = []
        self.current_question = 0
        self.score = 0
        self.question_image_reference = None
        self.sound_manager.stop_all_sounds()

    def get_question_count(self):
        """Mendapatkan jumlah soal dalam kuis saat ini."""
        return len(self.current_quiz_data)
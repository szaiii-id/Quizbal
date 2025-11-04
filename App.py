import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os      
import random  


from Config import *
from Data import ALL_QUIZZES



class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Seru Anak Balita")
        self.root.geometry("600x700")
        self.root.config(bg=WARNA_LATAR)

        self.current_quiz_data = []
        self.current_question = 0
        self.score = 0
        self.question_image_reference = None 

        self.main_menu_frame = tk.Frame(root, bg=WARNA_LATAR)
        self.game_selection_frame = tk.Frame(root, bg=WARNA_LATAR)
        self.quiz_frame = tk.Frame(root, bg=WARNA_LATAR)
        self.current_frame = None 

        self.create_main_menu()
        self.create_game_selection()
        self.create_quiz_screen()

        self.show_frame(self.main_menu_frame)

    def show_frame(self, frame_to_show):
        if self.current_frame:
            self.current_frame.pack_forget() 
        self.current_frame = frame_to_show
        self.current_frame.pack(fill="both", expand=True) 

    # --- LAYAR 1: MAIN MENU ---
    def create_main_menu(self):
        frame = self.main_menu_frame
        tk.Label(frame, text="Quiz Seru Balita", font=("Arial", 32, "bold"), 
                 bg=WARNA_LATAR, fg=WARNA_TEKS_JUDUL).pack(pady=(150, 20))
        tk.Label(frame, text="Ayo kita bermain sambil belajar!", font=("Arial", 16), 
                 bg=WARNA_LATAR, fg=WARNA_TEKS_BIASA).pack(pady=10)
        
        play_btn = tk.Button(frame, text="MAIN", font=("Arial", 24, "bold"), 
                             bg=WARNA_TEKS_JUDUL, fg="white", width=15, height=2,
                             relief="raised", borderwidth=3,
                             command=lambda: self.show_frame(self.game_selection_frame))
        play_btn.pack(pady=50)

    # --- LAYAR 2: PILIH GAME ---
    def create_game_selection(self):
        frame = self.game_selection_frame
        tk.Label(frame, text="Pilih Permainan", font=("Arial", 28, "bold"), 
                 bg=WARNA_LATAR, fg=WARNA_TEKS_JUDUL).pack(pady=(80, 30))
        
        btn_style = {"font": ("Arial", 16, "bold"), "width": 25, "pady": 15, 
                     "bg": WARNA_TOMBOL_DEFAULT, "fg": WARNA_TEKS_TOMBOL,
                     "relief": "raised", "borderwidth": 3}
                     
        tk.Button(frame, text="1. Tebak Benda", **btn_style, 
                  command=lambda: self.start_quiz("gambar")).pack(pady=10)
        tk.Button(frame, text="2. Pengetahuan Umum", **btn_style, 
                  command=lambda: self.start_quiz("umum")).pack(pady=10)
        tk.Button(frame, text="3. Tebak Hewan", **btn_style, 
                  command=lambda: self.start_quiz("hewan")).pack(pady=10)
        tk.Button(frame, text="4. Matematika Seru", **btn_style, 
                  command=lambda: self.start_quiz("matematika")).pack(pady=10)
        
        tk.Button(frame, text="Kembali ke Menu", font=("Arial", 12), 
                  bg="#FFFFFF", fg=WARNA_TEKS_JUDUL,
                  command=lambda: self.show_frame(self.main_menu_frame)).pack(pady=30)

    # --- LAYAR 3: KUIS BERLANGSUNG ---
    def create_quiz_screen(self):
        frame = self.quiz_frame
        
        self.question_image_label = tk.Label(frame, bg=WARNA_LATAR)
        self.question_image_label.pack(pady=(20, 10))

        self.question_label = tk.Label(frame, text="", font=("Arial", 20, "bold"), 
                                        wraplength=550, bg=WARNA_LATAR, 
                                        fg=WARNA_TEKS_BIASA, pady=10)
        self.question_label.pack()
        
        self.options_frame = tk.Frame(frame, bg=WARNA_LATAR)
        self.options_frame.pack(pady=10)

        self.option_buttons = []
        btn_font = ("Arial", 16, "bold")
        for i in range(3):
            btn = tk.Button(self.options_frame, text="", font=btn_font, 
                            width=20, height=2,
                            bg=WARNA_TOMBOL_DEFAULT, fg=WARNA_TEKS_TOMBOL,
                            relief="raised", borderwidth=3,
                            command=lambda i=i: self.check_answer(i))
            btn.pack(pady=8)
            self.option_buttons.append(btn)

        self.feedback_label = tk.Label(frame, text="", font=("Arial", 16, "italic"), 
                                        bg=WARNA_LATAR, pady=15)
        self.feedback_label.pack()
        tk.Button(frame, text="Keluar dari Game", font=("Arial", 12),
                  bg="#FFFFFF", fg=WARNA_TEKS_JUDUL, 
                  command=self.quit_quiz).pack(side="bottom", pady=20)

    # --- 3. LOGIKA KUIS (OFFLINE + ACAK) ---
    def start_quiz(self, game_type_key):
        if game_type_key not in ALL_QUIZZES or not ALL_QUIZZES[game_type_key]:
            messagebox.showerror("Oops! Soal Kosong", 
                                 f"Maaf, soal untuk '{game_type_key}' belum dibuat.")
            return 
        
        original_questions = ALL_QUIZZES[game_type_key]
        num_questions = min(len(original_questions), 10)
        questions_to_ask = random.sample(original_questions, num_questions)
        
        self.current_quiz_data = questions_to_ask
        self.current_question = 0
        self.score = 0
        
        self.show_frame(self.quiz_frame)
        self.display_question()

    def display_question(self):
        self.feedback_label.config(text="")
        self.question_image_reference = None
        self.toggle_option_buttons(disabled=False) 

        data = self.current_quiz_data[self.current_question]
        
        # q_image_file sekarang berisi path lengkap, e.g., "Image/Benda/q_apel.png"
        q_image_file = data.get("question_image")
        
        if q_image_file and os.path.exists(q_image_file):
            try:
                img = Image.open(q_image_file)
                img = img.resize((QUESTION_IMAGE_WIDTH, QUESTION_IMAGE_HEIGHT), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                self.question_image_label.config(image=photo)
                self.question_image_reference = photo
            except Exception as e:
                print(f"Error memuat gambar soal {q_image_file}: {e}")
                self.question_image_label.config(image="")
        else:
            self.question_image_label.config(image="")
            if q_image_file:
                # Ini akan memberitahu Anda jika path di Data.py salah
                print(f"Peringatan: File gambar soal '{q_image_file}' tidak ditemukan.")

        self.question_label.config(text=data["question"])

        options = data["options"]
        for i in range(3):
            option_text = options[i]
            btn = self.option_buttons[i]
            
            btn.config(
                text=option_text,
                image="",
                compound=tk.NONE,
                bg=WARNA_TOMBOL_DEFAULT,
                fg=WARNA_TEKS_TOMBOL
            )

    def check_answer(self, selected_index):
        self.toggle_option_buttons(disabled=True) 
        
        data = self.current_quiz_data[self.current_question]
        selected_option = data["options"][selected_index]
        correct_answer = data["answer"]

        selected_btn = self.option_buttons[selected_index]
        
        correct_index = data["options"].index(correct_answer)
        correct_btn = self.option_buttons[correct_index]

        if selected_option == correct_answer:
            self.score += 1
            self.feedback_label.config(text="Hore! Benar! 👍", fg="green")
            selected_btn.config(bg=WARNA_TOMBOL_BENAR, fg=WARNA_TEKS_BIASA)
        else:
            self.feedback_label.config(text="Oops, salah!", fg="red")
            selected_btn.config(bg=WARNA_TOMBOL_SALAH, fg="white")
            correct_btn.config(bg=WARNA_TOMBOL_BENAR, fg=WARNA_TEKS_BIASA)

        self.root.after(2000, self.next_question)

    def next_question(self):
        self.current_question += 1
        
        if self.current_question < len(self.current_quiz_data):
            self.display_question()
        else:
            self.show_results()

    def show_results(self):
        messagebox.showinfo("Kuis Selesai!",
                            f"Permainan Selesai!\n\n"
                            f"Skor kamu: {self.score} dari {len(self.current_quiz_data)} soal")
        self.show_frame(self.game_selection_frame) 
        
    def quit_quiz(self):
        if messagebox.askyesno("Yakin?", "Yakin mau keluar? Skor kamu akan hilang."):
            self.show_frame(self.game_selection_frame)

    def toggle_option_buttons(self, disabled=True):
        state = "disabled" if disabled else "normal"
        for btn in self.option_buttons:
            btn.config(state=state)

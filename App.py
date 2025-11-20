import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from Database import DatabaseManager
from RewardSystem import RewardSystem
from SoundManager import SoundManager
from GameManager import GameManager
from UIManager import UIManager
from Config import *
from Data import ALL_QUIZZES

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Seru Anak Balita 🎮")
        self.root.geometry("600x750")
        self.root.config(bg=WARNA_LATAR)

        # Initialize managers
        self.database = DatabaseManager()
        self.reward_system = RewardSystem()
        self.sound_manager = SoundManager()
        self.game_manager = GameManager(self.database, self.sound_manager)
        self.ui_manager = UIManager(root)

        self.editing_question_id = None
        self.cat_var = None
        self.q_entry = None
        self.img_path_var = None
        self.correct_var = None
        self.filter_var = None
        
        # Create UI screens
        self.create_main_menu()
        self.create_quiz_screen()
        self.create_parent_menu()
        self.create_manage_questions_screen()
        self.create_rewards_screen()
        self.create_stats_screen()

        self.sound_manager.play_bgm(PATH_MUSIK_MENU)
        self.ui_manager.show_frame(self.ui_manager.main_menu_frame)

    # ==========================================
    # UI CREATION METHODS
    # ==========================================
    def create_main_menu(self):
        frame = self.ui_manager.main_menu_frame
        
        # Header
        self.ui_manager.create_label(frame, text="🎮 Quiz Seru Balita", 
                                   font=("Arial", 32, "bold"), fg=WARNA_TEKS_JUDUL).pack(pady=(80, 10))
        self.ui_manager.create_label(frame, text="Ayo main sambil belajar!", 
                                   font=("Arial", 16)).pack(pady=5)
        
        # Main buttons
        button_frame = tk.Frame(frame, bg=WARNA_LATAR)
        button_frame.pack(pady=30)
        
        self.ui_manager.create_button(
            button_frame, text="🎯 MAIN", 
            command=lambda: self.show_frame(self.ui_manager.game_selection_frame),
            font=("Arial", 20, "bold"), width=15, height=2, bg=WARNA_TEKS_JUDUL
        ).pack(pady=10)
        
        self.ui_manager.create_button(
            button_frame, text="⭐ KOLEKSIKU", 
            command=lambda: self.show_frame(self.ui_manager.rewards_frame),
            bg="#FFD700", fg="black", width=15, height=1
        ).pack(pady=5)
        
        self.ui_manager.create_button(
            button_frame, text="📊 STATISTIK", 
            command=lambda: self.show_frame(self.ui_manager.stats_frame),
            bg="#87CEEB", fg="black", width=15, height=1
        ).pack(pady=5)

        # Parent menu button
        self.ui_manager.create_button(
            frame, text="⚙️ Menu Orang Tua", 
            command=lambda: self.show_frame(self.ui_manager.parent_frame),
            bg="#D3D3D3", fg="black", width=20, font=("Arial", 11, "bold")
        ).pack(side="bottom", pady=20)

    def refresh_game_selection_screen(self):
        frame = self.ui_manager.game_selection_frame
        for widget in frame.winfo_children():
            widget.destroy()
        
        self.ui_manager.create_label(frame, text="🎲 Pilih Permainan", 
                                   font=("Arial", 28, "bold"), fg=WARNA_TEKS_JUDUL).pack(pady=(40, 20))

        btn_container = tk.Frame(frame, bg=WARNA_LATAR)
        btn_container.pack(expand=True, fill="both", padx=50)

        categories = self.database.get_all_categories(ALL_QUIZZES.keys())
        
        display_names = {
            "gambar": "🎨 Tebak Benda",
            "umum": "🌍 Pengetahuan Umum", 
            "hewan": "🐯 Tebak Hewan",
            "matematika": "🔢 Matematika Seru"
        }

        for cat in categories:
            if cat in display_names:
                label_text = display_names[cat]
            else:
                label_text = f"🎯 {cat.replace('_', ' ').title()}"

            self.ui_manager.create_button(
                btn_container, text=label_text,
                command=lambda c=cat: self.start_quiz(c),
                font=("Arial", 14, "bold"), width=25, pady=12
            ).pack(pady=8)

        self.ui_manager.create_button(
            frame, text="🏠 Kembali ke Menu", 
            command=self.back_to_menu,
            bg="#FFFFFF", fg=WARNA_TEKS_JUDUL
        ).pack(side="bottom", pady=20)

    def create_quiz_screen(self):
        self.ui_manager.setup_quiz_ui()
        
        # Set button commands
        for i, btn in enumerate(self.ui_manager.option_buttons):
            btn.config(command=lambda idx=i: self.check_answer(idx))
        
        # Set exit button command
        exit_btn = self.ui_manager.quiz_frame.winfo_children()[-1]
        exit_btn.config(command=self.quit_quiz)

    def create_parent_menu(self):
        frame = self.ui_manager.parent_frame
        
        # Header
        header_frame = tk.Frame(frame, bg=WARNA_LATAR)
        header_frame.pack(fill="x", pady=20)
        self.ui_manager.create_label(header_frame, text="👨‍👩‍👧‍👦 Menu Orang Tua", 
                                   font=("Arial", 24, "bold"), fg=WARNA_TEKS_JUDUL).pack()
        
        # Main container
        main_container = tk.Frame(frame, bg=WARNA_LATAR)
        main_container.pack(expand=True, fill="both", padx=50, pady=20)
        
        self.ui_manager.create_button(
            main_container, text="➕ Tambah Soal Baru", 
            command=self.show_add_question_form,
            font=("Arial", 14, "bold"), width=25, pady=12
        ).pack(pady=15)
        
        self.ui_manager.create_button(
            main_container, text="📝 Kelola Soal", 
            command=lambda: self.show_frame(self.ui_manager.manage_questions_frame),
            font=("Arial", 14, "bold"), width=25, pady=12
        ).pack(pady=15)
        
        self.ui_manager.create_button(
            main_container, text="🏠 Kembali ke Menu Utama", 
            command=lambda: self.show_frame(self.ui_manager.main_menu_frame),
            bg="#FFFFFF", fg=WARNA_TEKS_JUDUL, width=20
        ).pack(pady=20)

    def create_manage_questions_screen(self):
        frame = self.ui_manager.manage_questions_frame
        
        self.ui_manager.create_label(frame, text="📝 Kelola Soal Custom", 
                                   font=("Arial", 24, "bold"), fg=WARNA_TEKS_JUDUL).pack(pady=20)
        
        # Filter
        filter_frame = tk.Frame(frame, bg=WARNA_LATAR)
        filter_frame.pack(pady=10)
        
        self.ui_manager.create_label(filter_frame, text="Filter by Kategori:", 
                                   font=("Arial", 11, "bold")).pack(side="left", padx=5)
        
        self.filter_var = tk.StringVar(value="Semua")
        categories = ["Semua"] + self.database.get_all_categories(ALL_QUIZZES.keys())
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                  values=categories, state="readonly", width=20)
        filter_combo.pack(side="left", padx=5)
        filter_combo.bind('<<ComboboxSelected>>', self.refresh_questions_list)
        
        # Questions container
        self.ui_manager.questions_container = tk.Frame(frame, bg=WARNA_LATAR)
        self.ui_manager.questions_container.pack(expand=True, fill="both", padx=30, pady=10)
        
        # Back button
        btn_frame = tk.Frame(frame, bg=WARNA_LATAR)
        btn_frame.pack(side="bottom", pady=20)
        
        self.ui_manager.create_button(
            btn_frame, text="➕ Tambah Soal Baru", 
            command=self.show_add_question_form,
            width=18
        ).pack(side="left", padx=5)
        
        self.ui_manager.create_button(
            btn_frame, text="🏠 Kembali ke Menu Orang Tua", 
            command=lambda: self.show_frame(self.ui_manager.parent_frame),
            bg="#FFFFFF", fg=WARNA_TEKS_JUDUL, width=20
        ).pack(side="left", padx=5)

    def create_rewards_screen(self):
        self.ui_manager.setup_rewards_ui()
        
        # Add navigation buttons
        btn_frame = tk.Frame(self.ui_manager.rewards_frame, bg=WARNA_LATAR)
        btn_frame.pack(side="bottom", pady=20)
        
        self.ui_manager.create_button(
            btn_frame, text="🎯 Main Lagi", 
            command=lambda: self.show_frame(self.ui_manager.game_selection_frame),
            width=15, height=1
        ).pack(side="left", padx=10)
        
        self.ui_manager.create_button(
            btn_frame, text="📊 Lihat Statistik", 
            command=lambda: self.show_frame(self.ui_manager.stats_frame),
            bg="#87CEEB", fg="black", width=15, height=1
        ).pack(side="left", padx=10)
        
        self.ui_manager.create_button(
            btn_frame, text="🏠 Menu Utama", 
            command=lambda: self.show_frame(self.ui_manager.main_menu_frame),
            bg="#FFFFFF", fg=WARNA_TEKS_JUDUL, width=15, height=1
        ).pack(side="left", padx=10)

    def create_stats_screen(self):
        self.ui_manager.setup_stats_ui()
        
        # Add navigation buttons
        btn_frame = tk.Frame(self.ui_manager.stats_frame, bg=WARNA_LATAR)
        btn_frame.pack(side="bottom", pady=20)
        
        self.ui_manager.create_button(
            btn_frame, text="🎯 Main Lagi", 
            command=lambda: self.show_frame(self.ui_manager.game_selection_frame),
            width=15, height=1
        ).pack(side="left", padx=10)
        
        self.ui_manager.create_button(
            btn_frame, text="⭐ Lihat Koleksi", 
            command=lambda: self.show_frame(self.ui_manager.rewards_frame),
            bg="#FFD700", fg="black", width=15, height=1
        ).pack(side="left", padx=10)
        
        self.ui_manager.create_button(
            btn_frame, text="🏠 Menu Utama", 
            command=lambda: self.show_frame(self.ui_manager.main_menu_frame),
            bg="#FFFFFF", fg=WARNA_TEKS_JUDUL, width=15, height=1
        ).pack(side="left", padx=10)

    # ==========================================
    # CORE FUNCTIONALITY
    # ==========================================
    def show_frame(self, frame_to_show):
        if frame_to_show == self.ui_manager.game_selection_frame:
            self.refresh_game_selection_screen()
        elif frame_to_show == self.ui_manager.manage_questions_frame:
            self.refresh_manage_questions_screen()
        elif frame_to_show == self.ui_manager.rewards_frame:
            self.update_rewards_display()
        elif frame_to_show == self.ui_manager.stats_frame:
            self.update_stats_display()

        self.ui_manager.show_frame(frame_to_show)

    def start_quiz(self, game_type_key):
        """Memulai kuis dengan 10 soal."""
        success, message = self.game_manager.start_quiz(game_type_key, ALL_QUIZZES)
        if not success:
            messagebox.showerror("Oops!", message)
            return
        
        # Tampilkan info jumlah soal
        num_questions = self.game_manager.get_question_count()
        messagebox.showinfo("Game Dimulai", 
                          f"{message}\n\nSiap untuk menjawab {num_questions} soal!")
        
        self.show_frame(self.ui_manager.quiz_frame)
        self.root.after(500, self.display_question)

    def display_question(self):
        """Menampilkan soal."""
        if self.game_manager.current_question >= len(self.game_manager.current_quiz_data):
            self.show_results()
            return
            
        data = self.game_manager.get_current_question()
        if not data:
            return

        self.game_manager.display_question_image(self.ui_manager.question_image_label)

        q_text = data["question"]
        self.ui_manager.question_label.config(text=q_text)
        
        # Tampilkan progress soal (contoh: "Soal 3/10")
        current_q = self.game_manager.current_question + 1
        total_q = len(self.game_manager.current_quiz_data)
        progress_text = f"Soal {current_q}/{total_q}"
        self.ui_manager.question_label.config(text=f"{progress_text}\n\n{q_text}")
        
        # Play question voice
        self.root.after(100, lambda: self.sound_manager.play_question_voice(q_text))

        # Display options
        options = data["options"]
        for i in range(3):
            if i < len(options):
                self.ui_manager.option_buttons[i].config(
                    text=options[i], 
                    bg=WARNA_TOMBOL_DEFAULT, 
                    fg=WARNA_TEKS_TOMBOL,
                    state="normal"
                )
            else:
                self.ui_manager.option_buttons[i].config(
                    text="", 
                    bg=WARNA_LATAR, 
                    state="disabled"
                )

    def check_answer(self, selected_index):
        """Memeriksa jawaban."""
        self.toggle_option_buttons(disabled=True)
        self.sound_manager.stop_voice()

        is_correct, message = self.game_manager.check_answer(selected_index)
        selected_btn = self.ui_manager.option_buttons[selected_index]

        if is_correct:
            self.ui_manager.create_feedback_popup(message, WARNA_TOMBOL_BENAR)
            selected_btn.config(bg=WARNA_TOMBOL_BENAR, fg=WARNA_TEKS_BIASA)
        else:
            self.ui_manager.create_feedback_popup(message, WARNA_TOMBOL_SALAH)
            selected_btn.config(bg=WARNA_TOMBOL_SALAH, fg="white")
            
            # Highlight correct answer
            correct_index = self.game_manager.get_correct_answer_index()
            if correct_index != -1:
                self.ui_manager.option_buttons[correct_index].config(
                    bg=WARNA_TOMBOL_BENAR, 
                    fg=WARNA_TEKS_BIASA
                )

        self.root.after(2000, self.next_question)

    def next_question(self):
        """Pindah ke soal berikutnya."""
        if self.game_manager.next_question():
            self.display_question()
        else:
            self.show_results()

    def show_results(self):
        """Menampilkan hasil kuis."""
        self.sound_manager.stop_voice()
        
        results = self.game_manager.get_results()
        stars = self.reward_system.calculate_stars(results["percentage"])
        self.reward_system.total_stars_earned += len([s for s in stars if s == "⭐"])
        
        # Update player stats
        self.reward_system.games_played_today += 1
        self.reward_system.update_player_stats("unknown", results["score"], results["total_questions"])
        
        # Check for sticker unlock
        sticker_unlocked = self.reward_system.check_sticker_unlock()
        
        # Show results with rewards
        result_message = f"🎊 Kuis Selesai! 🎊\n\n"
        result_message += f"Skor: {results['score']}/{results['total_questions']}\n"
        result_message += f"Bintang: {stars}\n"
        
        if sticker_unlocked:
            result_message += f"\n🎉 SELAMAT! 🎉\nDapat stiker baru:\n{sticker_unlocked}!"
            self.sound_manager.play_sound_effect("sticker")
        
        messagebox.showinfo("Hasil Kuis", result_message)
        
        # Update displays and show rewards
        self.update_rewards_display()
        self.update_stats_display()
        self.show_frame(self.ui_manager.rewards_frame)

    def quit_quiz(self):
        """Keluar dari game."""
        if messagebox.askyesno("Yakin?", "Yakin mau keluar dari game?"):
            self.sound_manager.stop_all_sounds()
            self.back_to_menu()

    def back_to_menu(self):
        """Kembali ke menu utama."""
        self.sound_manager.play_bgm(PATH_MUSIK_MENU)
        self.show_frame(self.ui_manager.main_menu_frame)

    def toggle_option_buttons(self, disabled=True):
        """Enable/disable tombol pilihan."""
        state = "disabled" if disabled else "normal"
        for btn in self.ui_manager.option_buttons:
            btn.config(state=state)

    # ==========================================
    # REWARDS & STATS METHODS
    # ==========================================
    def update_rewards_display(self):
        self.ui_manager.stars_label.config(text=f"Total Bintang: {self.reward_system.total_stars_earned} ⭐")
        
        games_to_next, unlocked_count, total_count = self.reward_system.get_sticker_progress()
        
        if games_to_next > 0:
            self.ui_manager.progress_label.config(text=f"Main {games_to_next} game lagi untuk dapat stiker baru!")
        else:
            self.ui_manager.progress_label.config(text="🎉 Main game berikutnya dapat stiker baru!")
        
        # Update sticker display
        for widget in self.ui_manager.sticker_container.winfo_children():
            widget.destroy()
        
        # Tampilkan progress
        progress_frame = tk.Frame(self.ui_manager.sticker_container, bg=WARNA_LATAR)
        progress_frame.pack(fill="x", pady=10)
        self.ui_manager.create_label(
            progress_frame, 
            text=f"Stiker terkumpul: {unlocked_count}/{total_count}", 
            font=("Arial", 14, "bold"), 
            fg=WARNA_TEKS_JUDUL
        ).pack()
        
        # BUAT GRID UNTUK SEMUA STIKER
        stickers_frame = tk.Frame(self.ui_manager.sticker_container, bg=WARNA_LATAR)
        stickers_frame.pack(expand=True, fill="both", padx=20, pady=10)
        
        row, col = 0, 0
        max_cols = 3
        
        for sticker_id, data in self.reward_system.sticker_collection.items():
            sticker_frame = tk.Frame(stickers_frame, bg=WARNA_LATAR, relief="solid", 
                                    bd=2, width=120, height=140)
            sticker_frame.pack_propagate(False)
            sticker_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            if data["unlocked"]:
                sticker_frame.config(bg="#E8F5E8")
                emoji_map = {
                    "Jago Matematika": "🔢", "Pakar Hewan": "🐯", "Jago Warna": "🎨",
                    "Ahli Bentuk": "⭐", "Raja Cepat": "⚡", "Pencinta Alam": "🌿",
                    "Pembaca Hebat": "📚", "Anak Kreatif": "✨"
                }
                emoji = emoji_map.get(data["name"], "🎁")
                
                self.ui_manager.create_label(sticker_frame, text=emoji, font=("Arial", 24), bg="#E8F5E8").pack(pady=8)
                self.ui_manager.create_label(sticker_frame, text=data["name"], font=("Arial", 10, "bold"), 
                                           bg="#E8F5E8", fg=WARNA_TEKS_JUDUL, wraplength=100).pack(pady=5, fill="x")
                
                # Badge "Terbuka"
                badge = tk.Frame(sticker_frame, bg=WARNA_TOMBOL_BENAR, height=20)
                badge.pack(side="bottom", fill="x", pady=2)
                badge.pack_propagate(False)
                self.ui_manager.create_label(badge, text="✓ Terbuka", font=("Arial", 8, "bold"), 
                                           bg=WARNA_TOMBOL_BENAR, fg="white").pack(expand=True)
            else:
                sticker_frame.config(bg="#F0F0F0")
                self.ui_manager.create_label(sticker_frame, text="🔒", font=("Arial", 24), 
                                           bg="#F0F0F0", fg="#A0A0A0").pack(pady=8)
                self.ui_manager.create_label(sticker_frame, text="???", font=("Arial", 10), 
                                           bg="#F0F0F0", fg="#A0A0A0", wraplength=100).pack(pady=5)
                
                # Badge "Terkunci"
                badge = tk.Frame(sticker_frame, bg=WARNA_TOMBOL_SALAH, height=20)
                badge.pack(side="bottom", fill="x", pady=2)
                badge.pack_propagate(False)
                self.ui_manager.create_label(badge, text="Terkunci", font=("Arial", 8, "bold"), 
                                           bg=WARNA_TOMBOL_SALAH, fg="white").pack(expand=True)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        for i in range(max_cols):
            stickers_frame.grid_columnconfigure(i, weight=1)

    def update_stats_display(self):
        for widget in self.ui_manager.stats_container.winfo_children():
            widget.destroy()
            
        stats = self.reward_system.player_stats
        accuracy = self.reward_system.get_accuracy()
        
        stats_data = [
            ("🎮 Total Game Dimainkan", f"{stats['total_games_played']} game"),
            ("❓ Total Pertanyaan Dijawab", f"{stats['total_questions_answered']} soal"),
            ("✅ Jawaban Benar", f"{stats['total_correct_answers']} jawaban"),
            ("🏆 Skor Terbaik", f"{stats['best_score']}%"),
            ("⭐ Total Bintang", f"{self.reward_system.total_stars_earned} bintang"),
            ("🎯 Kategori Favorit", f"{stats['favorite_category']}"),
            ("📈 Akurasi", f"{accuracy:.1f}%")
        ]
        
        for label, value in stats_data:
            stat_frame = tk.Frame(self.ui_manager.stats_container, bg=WARNA_LATAR)
            stat_frame.pack(fill="x", pady=8)
            
            self.ui_manager.create_label(
                stat_frame, text=label, font=("Arial", 12, "bold"), 
                fg=WARNA_TEKS_JUDUL, width=25, anchor="w"
            ).pack(side="left")
            self.ui_manager.create_label(stat_frame, text=value, font=("Arial", 12)).pack(side="left")

    # ==========================================
    # QUESTION MANAGEMENT METHODS - YANG DIPERBAIKI
    # ==========================================
    def show_add_question_form(self, question_data=None):
        """Menampilkan form tambah/edit soal."""
        for widget in self.ui_manager.parent_frame.winfo_children():
            widget.destroy()
        self.create_question_form(question_data)

    def create_question_form(self, question_data=None):
        """Membuat form untuk menambah/mengedit soal."""
        frame = self.ui_manager.parent_frame
        
        # Header
        title = "✏️ Edit Soal" if question_data else "➕ Tambah Soal Baru"
        self.ui_manager.create_label(frame, text=title, 
                                   font=("Arial", 24, "bold"), fg=WARNA_TEKS_JUDUL).pack(pady=20)
        
        # Main form container
        form_frame = tk.Frame(frame, bg=WARNA_LATAR)
        form_frame.pack(expand=True, fill="both", padx=50, pady=10)
        
        # Category selection
        cat_frame = tk.Frame(form_frame, bg=WARNA_LATAR)
        cat_frame.pack(fill="x", pady=10)
        self.ui_manager.create_label(cat_frame, text="Kategori:", font=("Arial", 12, "bold")).pack(side="left")
        
        self.cat_var = tk.StringVar(value="gambar" if not question_data else question_data.get("category", "gambar"))
        categories = self.database.get_all_categories(ALL_QUIZZES.keys())
        cat_combo = ttk.Combobox(cat_frame, textvariable=self.cat_var, values=categories, state="readonly", width=20)
        cat_combo.pack(side="left", padx=10)
        
        # Question text
        q_frame = tk.Frame(form_frame, bg=WARNA_LATAR)
        q_frame.pack(fill="x", pady=10)
        self.ui_manager.create_label(q_frame, text="Pertanyaan:", font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.q_entry = tk.Text(q_frame, height=3, width=50, font=("Arial", 11))
        self.q_entry.pack(fill="x", pady=5)
        if question_data:
            self.q_entry.insert("1.0", question_data["question"])
        
        # Image selection
        img_frame = tk.Frame(form_frame, bg=WARNA_LATAR)
        img_frame.pack(fill="x", pady=10)
        
        self.img_path_var = tk.StringVar(value=question_data.get("question_image", "") if question_data else "")
        self.ui_manager.create_label(img_frame, text="Gambar (opsional):", font=("Arial", 12, "bold")).pack(anchor="w")
        
        img_select_frame = tk.Frame(img_frame, bg=WARNA_LATAR)
        img_select_frame.pack(fill="x", pady=5)
        
        img_entry = tk.Entry(img_select_frame, textvariable=self.img_path_var, width=40, font=("Arial", 11))
        img_entry.pack(side="left", padx=(0, 10))
        
        self.ui_manager.create_button(
            img_select_frame, text="Pilih File", 
            command=self.browse_image_file,
            width=10
        ).pack(side="left")
        
        # Options
        options_frame = tk.Frame(form_frame, bg=WARNA_LATAR)
        options_frame.pack(fill="x", pady=10)
        self.ui_manager.create_label(options_frame, text="Pilihan Jawaban:", font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.option_entries = []
        for i in range(3):
            opt_frame = tk.Frame(options_frame, bg=WARNA_LATAR)
            opt_frame.pack(fill="x", pady=5)
            
            self.ui_manager.create_label(opt_frame, text=f"Pilihan {i+1}:", width=10).pack(side="left")
            entry = tk.Entry(opt_frame, width=40, font=("Arial", 11))
            entry.pack(side="left", fill="x", expand=True, padx=5)
            if question_data and i < len(question_data["options"]):
                entry.insert(0, question_data["options"][i])
            self.option_entries.append(entry)
        
        # Correct answer
        correct_frame = tk.Frame(form_frame, bg=WARNA_LATAR)
        correct_frame.pack(fill="x", pady=10)
        self.ui_manager.create_label(correct_frame, text="Jawaban Benar:", font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.correct_var = tk.StringVar(value=question_data.get("answer", "") if question_data else "")
        correct_combo = ttk.Combobox(correct_frame, textvariable=self.correct_var, 
                                   values=[], state="readonly", width=20)
        correct_combo.pack(anchor="w", pady=5)
        
        # Update correct answer options when entries change
        def update_correct_options(*args):
            options = [entry.get() for entry in self.option_entries if entry.get().strip()]
            correct_combo['values'] = options
            if options and not self.correct_var.get():
                self.correct_var.set(options[0])
        
        for entry in self.option_entries:
            entry.bind('<KeyRelease>', update_correct_options)
        
        # Button frame - VERSI LENGKAP DENGAN TOMBOL KEMBALI
        btn_frame = tk.Frame(form_frame, bg=WARNA_LATAR)
        btn_frame.pack(pady=20)

        # Tombol simpan/update
        if question_data:
            self.ui_manager.create_button(
                btn_frame, text="💾 Update Soal", 
                command=lambda: self.update_question_in_db(question_data["id"]),
                bg=WARNA_TOMBOL_BENAR, width=15
            ).pack(side="left", padx=5)
        else:
            self.ui_manager.create_button(
                btn_frame, text="💾 Simpan Soal", 
                command=self.save_question_to_db,
                bg=WARNA_TOMBOL_BENAR, width=15
            ).pack(side="left", padx=5)

        # Tombol batal (kembali ke kelola soal)
        self.ui_manager.create_button(
            btn_frame, text="❌ Batal", 
            command=lambda: self.show_frame(self.ui_manager.manage_questions_frame),
            bg=WARNA_TOMBOL_SALAH, width=15
        ).pack(side="left", padx=5)

        # TOMBOL BARU: Kembali ke Menu Utama
        self.ui_manager.create_button(
            btn_frame, text="🏠 Menu Utama", 
            command=lambda: self.show_frame(self.ui_manager.main_menu_frame),
            bg="#FFFFFF", fg=WARNA_TEKS_JUDUL, width=15
        ).pack(side="left", padx=5)
        # Initialize correct answer options
        update_correct_options()

    def browse_image_file(self):
        """Membuka dialog untuk memilih file gambar."""
        filename = filedialog.askopenfilename(
            title="Pilih Gambar",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        if filename:
            self.img_path_var.set(filename)

    def save_question_to_db(self):
        """Menyimpan soal baru ke database."""
        if not self.validate_question_form():
            return
        
        category = self.cat_var.get()
        question = self.q_entry.get("1.0", "end-1c").strip()
        image_path = self.img_path_var.get().strip()
        options = [entry.get().strip() for entry in self.option_entries if entry.get().strip()]
        answer = self.correct_var.get()
        
        try:
            self.database.add_question(category, question, image_path, options, answer)
            messagebox.showinfo("Sukses", "Soal berhasil ditambahkan!")
            self.show_frame(self.ui_manager.parent_frame)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan soal: {str(e)}")

    def update_question_in_db(self, question_id):
        """Update soal yang sudah ada."""
        if not self.validate_question_form():
            return
        
        category = self.cat_var.get()
        question = self.q_entry.get("1.0", "end-1c").strip()
        image_path = self.img_path_var.get().strip()
        options = [entry.get().strip() for entry in self.option_entries if entry.get().strip()]
        answer = self.correct_var.get()
        
        try:
            self.database.update_question(question_id, category, question, image_path, options, answer)
            messagebox.showinfo("Sukses", "Soal berhasil diupdate!")
            self.show_frame(self.ui_manager.manage_questions_frame)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengupdate soal: {str(e)}")

    def validate_question_form(self):
        """Validasi form soal."""
        question = self.q_entry.get("1.0", "end-1c").strip()
        if not question:
            messagebox.showerror("Error", "Pertanyaan tidak boleh kosong!")
            return False
        
        options = [entry.get().strip() for entry in self.option_entries if entry.get().strip()]
        if len(options) < 2:
            messagebox.showerror("Error", "Minimal harus ada 2 pilihan jawaban!")
            return False
        
        if not self.correct_var.get():
            messagebox.showerror("Error", "Harus pilih jawaban yang benar!")
            return False
        
        return True

    def refresh_manage_questions_screen(self):
        """Refresh layar kelola soal - IMPLEMENTASI YANG DIPERBAIKI"""
        frame = self.ui_manager.manage_questions_frame
        
        # Clear container
        for widget in self.ui_manager.questions_container.winfo_children():
            widget.destroy()
        
        # Get questions based on filter
        filter_category = self.filter_var.get()
        if filter_category == "Semua":
            questions = self.database.get_all_questions()
        else:
            questions = self.database.get_all_questions(filter_category)
        
        if not questions:
            self.ui_manager.create_label(
                self.ui_manager.questions_container, 
                text="Belum ada soal custom. Silakan tambah soal baru!",
                font=("Arial", 14), fg=WARNA_TEKS_JUDUL
            ).pack(pady=50)
            return
        
        # Create scrollable area for questions
        canvas, scrollbar, scrollable_frame = self.ui_manager.create_scrollable_frame(self.ui_manager.questions_container)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Display each question
        for i, question in enumerate(questions):
            q_frame = tk.Frame(scrollable_frame, bg=WARNA_LATAR, relief="solid", bd=1)
            q_frame.pack(fill="x", padx=10, pady=5)
            
            # Question info
            info_frame = tk.Frame(q_frame, bg=WARNA_LATAR)
            info_frame.pack(fill="x", padx=10, pady=5)
            
            self.ui_manager.create_label(
                info_frame, 
                text=f"Kategori: {question['category']} | ID: {question['id']}",
                font=("Arial", 10, "bold"), 
                fg=WARNA_TEKS_JUDUL
            ).pack(anchor="w")
            
            self.ui_manager.create_label(
                info_frame, 
                text=question['question'],
                font=("Arial", 11),
                wraplength=400
            ).pack(anchor="w", pady=(2, 0))
            
            # Options
            options_text = "Pilihan: " + " | ".join(question['options'])
            self.ui_manager.create_label(
                info_frame, 
                text=options_text,
                font=("Arial", 10),
                fg="#666666"
            ).pack(anchor="w")
            
            self.ui_manager.create_label(
                info_frame, 
                text=f"Jawaban benar: {question['answer']}",
                font=("Arial", 10, "bold"),
                fg=WARNA_TOMBOL_BENAR
            ).pack(anchor="w")
            
            # Action buttons
            btn_frame = tk.Frame(q_frame, bg=WARNA_LATAR)
            btn_frame.pack(fill="x", padx=10, pady=5)
            
            self.ui_manager.create_button(
                btn_frame, text="✏️ Edit", 
                command=lambda q=question: self.show_add_question_form(q),
                width=8, font=("Arial", 9)
            ).pack(side="left", padx=(0, 5))
            
            self.ui_manager.create_button(
                btn_frame, text="🗑️ Hapus", 
                command=lambda qid=question['id']: self.delete_question(qid),
                bg=WARNA_TOMBOL_SALAH, width=8, font=("Arial", 9)
            ).pack(side="left")
        
        # Update scrollregion after adding all questions
        scrollable_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def delete_question(self, question_id):
        """Hapus soal dengan konfirmasi."""
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus soal ini?"):
            try:
                self.database.delete_question(question_id)
                messagebox.showinfo("Sukses", "Soal berhasil dihapus!")
                self.refresh_manage_questions_screen()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus soal: {str(e)}")

    def refresh_questions_list(self, event=None):
        """Refresh daftar soal ketika filter berubah."""
        self.refresh_manage_questions_screen()
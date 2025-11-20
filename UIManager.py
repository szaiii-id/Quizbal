import tkinter as tk
from tkinter import ttk
from Config import *

class UIManager:
    def __init__(self, root):
        self.root = root
        self.current_frame = None
        
        # Create all frames
        self.main_menu_frame = tk.Frame(root, bg=WARNA_LATAR)
        self.game_selection_frame = tk.Frame(root, bg=WARNA_LATAR) 
        self.quiz_frame = tk.Frame(root, bg=WARNA_LATAR)
        self.parent_frame = tk.Frame(root, bg=WARNA_LATAR) 
        self.manage_questions_frame = tk.Frame(root, bg=WARNA_LATAR)
        self.rewards_frame = tk.Frame(root, bg=WARNA_LATAR)
        self.stats_frame = tk.Frame(root, bg=WARNA_LATAR)

        # Initialize UI components
        self.question_image_label = None
        self.question_label = None
        self.option_buttons = []
        self.sticker_container = None
        self.stats_container = None
        self.questions_container = None

    def show_frame(self, frame_to_show):
        """Menampilkan frame tertentu."""
        if self.current_frame:
            self.current_frame.pack_forget()
        self.current_frame = frame_to_show
        self.current_frame.pack(fill="both", expand=True)

    def create_scrollable_frame(self, parent):
        """Membuat frame yang bisa di-scroll."""
        canvas = tk.Canvas(parent, bg=WARNA_LATAR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=WARNA_LATAR)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        return canvas, scrollbar, scrollable_frame

    def create_button(self, parent, text, command, **kwargs):
        """Membuat tombol dengan style konsisten."""
        default_style = {
            "font": ("Arial", 12),
            "bg": WARNA_TOMBOL_DEFAULT,
            "fg": WARNA_TEKS_TOMBOL,
            "relief": "raised",
            "borderwidth": 3
        }
        default_style.update(kwargs)
        
        return tk.Button(parent, text=text, command=command, **default_style)

    def create_label(self, parent, text, **kwargs):
        """Membuat label dengan style konsisten."""
        default_style = {
            "bg": WARNA_LATAR,
            "fg": WARNA_TEKS_BIASA,
            "font": ("Arial", 12)
        }
        default_style.update(kwargs)
        
        return tk.Label(parent, text=text, **default_style)

    def create_feedback_popup(self, message, color):
        """Membuat popup feedback."""
        popup = tk.Toplevel(self.root)
        popup.config(bg=color)
        popup.overrideredirect(True)
        popup.geometry(f'300x100+{self.root.winfo_x()+150}+{self.root.winfo_y()+300}')
        
        tk.Label(popup, text=message, font=("Arial", 20, "bold"), 
                bg=color, fg="white").pack(expand=True, fill="both")
        
        popup.after(1500, popup.destroy)
        return popup

    def setup_quiz_ui(self):
        """Setup UI untuk layar kuis."""
        frame = self.quiz_frame
        
        # Question image
        self.question_image_label = tk.Label(frame, bg=WARNA_LATAR)
        self.question_image_label.pack(pady=(20, 10))
        
        # Question text
        self.question_label = tk.Label(frame, text="", font=("Arial", 20, "bold"), 
                                      wraplength=550, bg=WARNA_LATAR, fg=WARNA_TEKS_BIASA, pady=10)
        self.question_label.pack()
        
        # Options
        self.options_frame = tk.Frame(frame, bg=WARNA_LATAR)
        self.options_frame.pack(pady=10)
        
        self.option_buttons = []
        for i in range(3):
            btn = self.create_button(
                self.options_frame, 
                text="", 
                command=None,  # Will be set later
                font=("Arial", 16, "bold"),
                width=20,
                height=2
            )
            btn.pack(pady=8)
            self.option_buttons.append(btn)
        
        # Exit button
        self.create_button(
            frame, 
            text="🏠 Keluar dari Game", 
            command=None,  # Will be set later
            bg="#FFFFFF", 
            fg=WARNA_TEKS_JUDUL
        ).pack(side="bottom", pady=20)

    def setup_rewards_ui(self):
        """Setup UI untuk layar rewards."""
        frame = self.rewards_frame
        
        # Header
        self.create_label(frame, text="🎁 Koleksi Hadiahmu!", font=("Arial", 28, "bold"), 
                         fg=WARNA_TEKS_JUDUL).pack(pady=20)
        
        # Stars display
        self.stars_label = self.create_label(frame, text="", font=("Arial", 24), fg="#FFD700")
        self.stars_label.pack(pady=10)
        
        # Progress to next sticker
        self.progress_label = self.create_label(frame, text="", font=("Arial", 14))
        self.progress_label.pack(pady=5)
        
        # Sticker collection title
        self.create_label(frame, text="Stiker yang Kamu Dapat:", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Sticker container dengan scroll
        container_frame = tk.Frame(frame, bg=WARNA_LATAR)
        container_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.sticker_canvas = tk.Canvas(container_frame, bg=WARNA_LATAR, highlightthickness=0)
        self.sticker_scrollbar = ttk.Scrollbar(container_frame, orient="vertical", command=self.sticker_canvas.yview)
        
        self.sticker_container = tk.Frame(self.sticker_canvas, bg=WARNA_LATAR)
        
        self.sticker_container.bind(
            "<Configure>",
            lambda e: self.sticker_canvas.configure(scrollregion=self.sticker_canvas.bbox("all"))
        )
        
        self.sticker_canvas.create_window((0, 0), window=self.sticker_container, anchor="nw")
        self.sticker_canvas.configure(yscrollcommand=self.sticker_scrollbar.set)
        
        self.sticker_canvas.pack(side="left", fill="both", expand=True)
        self.sticker_scrollbar.pack(side="right", fill="y")

    def setup_stats_ui(self):
        """Setup UI untuk layar statistik."""
        frame = self.stats_frame
        
        self.create_label(frame, text="📊 Statistik Permainan", font=("Arial", 28, "bold"), 
                         fg=WARNA_TEKS_JUDUL).pack(pady=20)
        
        # Stats container
        self.stats_container = tk.Frame(frame, bg=WARNA_LATAR)
        self.stats_container.pack(expand=True, fill="both", padx=50, pady=20)
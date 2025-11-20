import pygame
import io
from gtts import gTTS
from Config import *

class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
        self.current_voice_sound = None
        self.load_sounds()

    def load_sounds(self):
        """Memuat semua file suara."""
        try:
            self.suara_benar = pygame.mixer.Sound(PATH_SUARA_BENAR)
            self.suara_salah = pygame.mixer.Sound(PATH_SUARA_SALAH)
            # Try to load reward sounds, but don't crash if they don't exist
            try:
                self.suara_stiker = pygame.mixer.Sound(PATH_SUARA_STIKER)
                self.suara_bintang = pygame.mixer.Sound(PATH_SUARA_BINTANG)
            except:
                self.suara_stiker = None
                self.suara_bintang = None
        except:
            self.suara_benar = None
            self.suara_salah = None
            self.suara_stiker = None
            self.suara_bintang = None

    def play_bgm(self, music_file):
        """Memutar background music."""
        try:
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)
        except: 
            pass

    def play_question_voice(self, text):
        """Memutar suara pertanyaan menggunakan TTS."""
        try:
            if self.current_voice_sound: 
                self.current_voice_sound.stop()
            tts = gTTS(text=text, lang='id', slow=False)
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            self.current_voice_sound = pygame.mixer.Sound(mp3_fp)
            self.current_voice_sound.set_volume(1.0)
            self.current_voice_sound.play()
        except: 
            pass

    def play_sound_effect(self, sound_type):
        """Memutar sound effect."""
        sound_map = {
            "correct": self.suara_benar,
            "wrong": self.suara_salah,
            "sticker": self.suara_stiker,
            "star": self.suara_bintang
        }
        
        sound = sound_map.get(sound_type)
        if sound:
            try:
                sound.play()
            except:
                pass

    def stop_voice(self):
        """Menghentikan suara TTS."""
        if self.current_voice_sound:
            self.current_voice_sound.stop()

    def stop_all_sounds(self):
        """Menghentikan semua suara."""
        self.stop_voice()
        pygame.mixer.music.stop()
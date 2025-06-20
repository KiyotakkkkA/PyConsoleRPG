import pygame

class AudioManager:
    """
    Менеджер аудио для воспроизведения музыки и звуковых эффектов.
    """
    
    __instance = None
    
    @classmethod
    def get_instance(cls):
        if cls.__instance == None:
            cls.__instance = cls()
        return cls.__instance
    
    def __init__(self):
        try:
            pygame.mixer.init()
            self.initialized = True
            self.current_music = None
            self.music_volume = 1
            self.sound_volume = 1
            self.current_sound_multiplier = 0.1
            self.current_music_multiplier = 0.1
            self.sounds_cache = {}
            print("Аудио система инициализирована")
        except Exception as e:
            self.initialized = False
            print(f"Ошибка инициализации аудио: {e}")
            
    def get_current_music_multiplier_as_int(self):
        return int(self.current_music_multiplier * 10)
    
    def get_current_sound_multiplier_as_int(self):
        return int(self.current_sound_multiplier * 10)
    
    def play_music(self, music_file: str, loop: bool = True):
        """
        Воспроизводит фоновую музыку.
        
        Args:
            music_file: Путь к файлу музыки
            loop: Зацикливать музыку
            volume_multiplier: Множитель громкости (0.0 - 1.0)
        """
        if not self.initialized:
            return
            
        if music_file == self.current_music:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1 if loop else 0)
                actual_volume = self.music_volume * self.current_music_multiplier
                pygame.mixer.music.set_volume(actual_volume)
            return
            
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                
            pygame.mixer.music.load(music_file)
            actual_volume = self.music_volume * self.current_music_multiplier
            pygame.mixer.music.set_volume(actual_volume)
            pygame.mixer.music.play(-1 if loop else 0)
            self.current_music = music_file
        except Exception as e:
            pass
    
    def stop_music(self):
        """
        Останавливает воспроизведение музыки.
        """
        if not self.initialized:
            return
            
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        self.current_music = None
    
    def play_sound(self, sound_file: str):
        """
        Воспроизводит звуковой эффект.
        
        Args:
            sound_file: Путь к файлу звукового эффекта
            volume_multiplier: Множитель громкости (0.0 - 1.0), если None - используется текущий множитель
        """
        if not self.initialized:
            return
            
        try:
            actual_multiplier = self.current_sound_multiplier
            
            if sound_file in self.sounds_cache:
                sound = self.sounds_cache[sound_file]
            else:
                sound = pygame.mixer.Sound(sound_file)
                self.sounds_cache[sound_file] = sound
                
            actual_volume = self.sound_volume * actual_multiplier
            sound.set_volume(actual_volume)
                
            sound.play()
            
        except Exception as e:
            pass
    
    def set_music_volume(self, volume: float):
        """
        Устанавливает базовую громкость музыки.
        
        Args:
            volume: Значение громкости от 0.0 до 1.0
        """
        if not self.initialized:
            return
            
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sound_volume(self, volume: float):
        """
        Устанавливает базовую громкость звуковых эффектов.
        
        Args:
            volume: Значение громкости от 0.0 до 1.0
        """
        if not self.initialized:
            return
            
        self.sound_volume = max(0.0, min(1.0, volume))
        # Обновляем громкость для всех кэшированных звуков
        for sound in self.sounds_cache.values():
            sound.set_volume(self.sound_volume)
            
    def apply_music_volume_multiplier(self, multiplier: float):
        """
        Применяет множитель к текущей громкости музыки без изменения базовой громкости.
        
        Args:
            multiplier: Множитель громкости от 0.0 до 1.0
        """
        if not self.initialized:
            return
            
        self.current_music_multiplier = max(0.0, min(1.0, multiplier))
        actual_volume = self.music_volume * self.current_music_multiplier
        pygame.mixer.music.set_volume(actual_volume)
        
    def apply_sound_volume_multiplier(self, multiplier: float):
        """
        Применяет множитель к текущей громкости звуков без изменения базовой громкости.
        
        Args:
            multiplier: Множитель громкости от 0.0 до 1.0
        """
        if not self.initialized:
            return
            
        self.current_sound_multiplier = max(0.0, min(1.0, multiplier))
        actual_volume = self.sound_volume * self.current_sound_multiplier
        for sound in self.sounds_cache.values():
            sound.set_volume(actual_volume)
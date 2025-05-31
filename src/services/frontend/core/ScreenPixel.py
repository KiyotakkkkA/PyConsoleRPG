from src.services.output import Color
from typing import Optional, Union
from rich.text import Text as RichText
import wcwidth

def hash_screen_pixel(char: str, fg_color: str, bg_color: str) -> int:
    return hash((char, fg_color, bg_color))

# Словарь для замены проблемных иконок на простые символы
ICON_FALLBACKS = {
    '🌍': 'O',  # Планета
    '🏰': 'C',  # Замок
    '🏘️': 'H',  # Город
    '📦': 'B',  # Коробка
    '🗝️': 'K',  # Ключ
    '🚪': 'D',  # Дверь
    '🔒': 'L',  # Замок
    '💣': '*',  # Бомба
    '🗡️': '/',  # Меч
    '🛡️': '0',  # Щит
    '🧪': 'P',  # Зелье
    '📜': '=',  # Свиток
    '🔮': '*',  # Магия
    '🏹': '>',  # Стрела
    '⚔️': 'X',  # Бой
    '❤️': '<3', # Здоровье
    '🔥': '^',  # Огонь
    '💧': 'V',  # Вода
    '⭐': '*',  # Звезда
}

class ScreenPixel:
    """
    Класс, представляющий пиксель на экране с поддержкой сложных Unicode-символов
    """
    def __init__(self, char: str = " ", fg_color: str = Color.WHITE, bg_color: str = Color.RESET):
        # Сохраняем оригинальный символ
        self._original_char = char
        
        # Определяем, является ли символ специальной иконкой
        self._is_icon = len(char) > 1 or (char and wcwidth.wcwidth(char) > 1)
        
        # Для отображения в консоли Win используем замену или первый символ
        if self._is_icon and char in ICON_FALLBACKS:
            self._display_char = ICON_FALLBACKS[char]
        elif self._is_icon:
            self._display_char = "?"
        else:
            self._display_char = char
            
        self.fg_color = fg_color
        self.bg_color = bg_color
        self._rich_text: Optional[RichText] = None
        
    def __str__(self) -> str:
        return f"{self.bg_color}{self.fg_color}{self.char}{Color.RESET}"
    
    def copy(self) -> 'ScreenPixel':
        return ScreenPixel(self._original_char, self.fg_color, self.bg_color)
    
    @property
    def char(self) -> str:
        """Возвращает оригинальный символ"""
        return self._original_char
    
    @char.setter
    def char(self, value: str) -> None:
        """Устанавливает новый символ с обновлением отображаемого символа"""
        self._original_char = value
        self._is_icon = len(value) > 1 or (value and wcwidth.wcwidth(value) > 1)
        
        if self._is_icon and value in ICON_FALLBACKS:
            self._display_char = ICON_FALLBACKS[value]
        elif self._is_icon:
            self._display_char = "?"
        else:
            self._display_char = value
        
        # Сбрасываем кэшированный rich_text
        self._rich_text = None
    
    @property
    def rich_text(self) -> RichText:
        """Получить представление пикселя в виде RichText"""
        if self._rich_text is None:
            self._rich_text = RichText(self._original_char or " ")
        return self._rich_text
    
    @property
    def display_char(self) -> str:
        """
        Возвращает символ для отображения в консоли Windows
        """
        if not self._display_char:
            return " "
        return self._display_char

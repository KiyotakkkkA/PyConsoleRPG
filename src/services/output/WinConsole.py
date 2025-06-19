import ctypes
from ctypes import wintypes
import re
import time
from src.services.output import Color
from src.config import Config
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.services.frontend.core import ScreenPixel

kernel32 = ctypes.windll.kernel32

STD_OUTPUT_HANDLE = -11
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
ENABLE_PROCESSED_OUTPUT = 0x0001
ENABLE_WRAP_AT_EOL_OUTPUT = 0x0002

class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes._COORD),
        ("dwCursorPosition", wintypes._COORD),
        ("wAttributes", wintypes.WORD),
        ("srWindow", wintypes.SMALL_RECT),
        ("dwMaximumWindowSize", wintypes._COORD)
    ]

class CONSOLE_CURSOR_INFO(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("bVisible", wintypes.BOOL)
    ]

class CHAR_INFO(ctypes.Structure):
    class Char(ctypes.Union):
        _fields_ = [("UnicodeChar", wintypes.WCHAR), ("AsciiChar", wintypes.CHAR)]
    _fields_ = [("Char", Char), ("Attributes", wintypes.WORD)]

ANSI_REGEX = re.compile(r'\033\[(\d+);?(\d+)?m')

ANSI_TO_WIN_COLOR = {
    Color.BLACK: 0,
    Color.RED: 4,
    Color.GREEN: 2,
    Color.YELLOW: 6,
    Color.BLUE: 1,
    Color.MAGENTA: 5,
    Color.CYAN: 3,
    Color.WHITE: 7,
    
    Color.BOLD_BLACK: 0,
    Color.BOLD_RED: 4,
    Color.BOLD_GREEN: 2,
    Color.BOLD_YELLOW: 6,
    Color.BOLD_BLUE: 1,
    Color.BOLD_MAGENTA: 5,
    Color.BOLD_CYAN: 3,
    Color.BOLD_WHITE: 7,
    
    Color.UNDERLINE_BLACK: 0,
    Color.UNDERLINE_RED: 4,
    Color.UNDERLINE_GREEN: 2,
    Color.UNDERLINE_YELLOW: 6,
    Color.UNDERLINE_BLUE: 1,
    Color.UNDERLINE_MAGENTA: 5,
    Color.UNDERLINE_CYAN: 3,
    Color.UNDERLINE_WHITE: 7,
    
    Color.BRIGHT_BLACK: 8,
    Color.BRIGHT_RED: 12,
    Color.BRIGHT_GREEN: 10,
    Color.BRIGHT_YELLOW: 14,
    Color.BRIGHT_BLUE: 9,
    Color.BRIGHT_MAGENTA: 13,
    Color.BRIGHT_CYAN: 11,
    Color.BRIGHT_WHITE: 15,
    
    Color.BOLD_BRIGHT_BLACK: 8,
    Color.BOLD_BRIGHT_RED: 12,
    Color.BOLD_BRIGHT_GREEN: 10,
    Color.BOLD_BRIGHT_YELLOW: 14,
    Color.BOLD_BRIGHT_BLUE: 9,
    Color.BOLD_BRIGHT_MAGENTA: 13,
    Color.BOLD_BRIGHT_CYAN: 11,
    Color.BOLD_BRIGHT_WHITE: 15,
    
    Color.BG_BLACK: 0 << 4,
    Color.BG_RED: 4 << 4,
    Color.BG_GREEN: 2 << 4,
    Color.BG_YELLOW: 6 << 4,
    Color.BG_BLUE: 1 << 4,
    Color.BG_MAGENTA: 5 << 4,
    Color.BG_CYAN: 3 << 4,
    Color.BG_WHITE: 7 << 4,
    
    Color.BG_BRIGHT_BLACK: 8 << 4,
    Color.BG_BRIGHT_RED: 12 << 4,
    Color.BG_BRIGHT_GREEN: 10 << 4,
    Color.BG_BRIGHT_YELLOW: 14 << 4,
    Color.BG_BRIGHT_BLUE: 9 << 4,
    Color.BG_BRIGHT_MAGENTA: 13 << 4,
    Color.BG_BRIGHT_CYAN: 11 << 4,
    Color.BG_BRIGHT_WHITE: 15 << 4,
    
    Color.RESET: 7
}

class WinConsole:
    color_attr_cache = {}
    
    def __init__(self):
        self.handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        
        mode = wintypes.DWORD()
        kernel32.GetConsoleMode(self.handle, ctypes.byref(mode))
        mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
        mode.value |= ENABLE_PROCESSED_OUTPUT
        mode.value |= ENABLE_WRAP_AT_EOL_OUTPUT
        mode.value |= 0x0008
        kernel32.SetConsoleMode(self.handle, mode)
        
        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        kernel32.GetConsoleScreenBufferInfo(self.handle, ctypes.byref(csbi))
        self.width = csbi.dwSize.X
        self.height = csbi.dwSize.Y
        
        self.prev_buffer = None
        
        self.target_fps = Config.FPS
        self.last_frame_time = time.time()
        
        self.stdscr = None
        
    def get_console_size(self):
        """Получение размеров консоли"""
        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        kernel32.GetConsoleScreenBufferInfo(self.handle, ctypes.byref(csbi))
        return csbi.dwSize.X, csbi.dwSize.Y
        
    def clear_screen(self):
        """Очистка экрана с использованием WinAPI"""
        width, height = self.get_console_size()
        chars_written = wintypes.DWORD(0)
        kernel32.FillConsoleOutputCharacterW(self.handle, ' ', width * height, 
                                        wintypes._COORD(0, 0), ctypes.byref(chars_written))
        kernel32.FillConsoleOutputAttribute(self.handle, 7, width * height,
                                      wintypes._COORD(0, 0), ctypes.byref(chars_written))
        kernel32.SetConsoleCursorPosition(self.handle, wintypes._COORD(0, 0))
        
    def set_cursor_position(self, x, y):
        """Установка позиции курсора"""
        kernel32.SetConsoleCursorPosition(self.handle, wintypes._COORD(x, y))
        
    def set_cursor_visibility(self, visible):
        """Установка видимости курсора"""
        cursor_info = CONSOLE_CURSOR_INFO()
        kernel32.GetConsoleCursorInfo(self.handle, ctypes.byref(cursor_info))
        cursor_info.bVisible = visible
        kernel32.SetConsoleCursorInfo(self.handle, ctypes.byref(cursor_info))
    
    def ansi_to_win_attr(self, fg_color, bg_color):
        """Преобразование ANSI-цветов в атрибут Windows
        
        Поддерживает сложение цветов через оператор '|' (например, Color.BG_BLACK | Color.RED)
        """
        cache_key = (str(fg_color), str(bg_color))
        
        if cache_key in self.__class__.color_attr_cache:
            return self.__class__.color_attr_cache[cache_key]
        
        text_attr = 7
        bg_attr = 0
        
        if fg_color in ANSI_TO_WIN_COLOR:
            if 'BG_' not in str(fg_color):
                text_attr = ANSI_TO_WIN_COLOR[fg_color] & 0x0F
            else:
                win_code = ANSI_TO_WIN_COLOR[fg_color]
                if win_code < 16:
                    bg_attr = win_code << 4
                else:
                    bg_attr = win_code
        
        if bg_color in ANSI_TO_WIN_COLOR:
            if 'BG_' in str(bg_color):
                win_code = ANSI_TO_WIN_COLOR[bg_color]
                if win_code < 16:
                    bg_attr = win_code << 4
                else:
                    bg_attr = win_code
            else:
                win_code = ANSI_TO_WIN_COLOR[bg_color] & 0x0F
                bg_attr = win_code << 4
        
        if hasattr(fg_color, 'code'):
            code_str = fg_color.code
            for color_name, color_obj in vars(Color).items():
                if not isinstance(color_obj, type) and hasattr(color_obj, 'code'):
                    if color_obj.code in code_str:
                        if 'BG_' in color_name:
                            win_code = ANSI_TO_WIN_COLOR.get(color_obj, 0)
                            if win_code < 16:
                                bg_attr |= win_code << 4
                            else:
                                bg_attr |= win_code
                        else:
                            win_code = ANSI_TO_WIN_COLOR.get(color_obj, 7)
                            text_attr = win_code & 0x0F
        
        if hasattr(bg_color, 'code'):
            code_str = bg_color.code
            for color_name, color_obj in vars(Color).items():
                if not isinstance(color_obj, type) and hasattr(color_obj, 'code'):
                    if color_obj.code in code_str:
                        if 'BG_' in color_name:
                            win_code = ANSI_TO_WIN_COLOR.get(color_obj, 0)
                            if win_code < 16:
                                bg_attr |= win_code << 4
                            else:
                                bg_attr |= win_code
                        else:
                            win_code = ANSI_TO_WIN_COLOR.get(color_obj, 7)
                            text_attr = win_code & 0x0F
        
        if bg_color == Color.RESET:
            bg_attr = 0
        
        result = (text_attr & 0x0F) | (bg_attr & 0xF0)
        
        self.__class__.color_attr_cache[cache_key] = result
        
        return result
    
    def write_output_chars(self, chars, fg_colors, bg_colors, start_x=0, start_y=0):
        """Оптимизированная запись с прямым доступом к буферу"""
        if not chars:
            return
            
        length = len(chars)
        
        buffer = (CHAR_INFO * length)()
        attr_cache = {}
        
        for i in range(length):
            buffer[i].Char.UnicodeChar = chars[i]
            
            color_key = (fg_colors[i], bg_colors[i])
            if color_key not in attr_cache:
                attr_cache[color_key] = self.ansi_to_win_attr(fg_colors[i], bg_colors[i])
            
            buffer[i].Attributes = attr_cache[color_key]
        
        rect = wintypes.SMALL_RECT(start_x, start_y, start_x + length - 1, start_y)
        
        kernel32.WriteConsoleOutputW(
            self.handle,
            buffer,
            wintypes._COORD(length, 1),
            wintypes._COORD(0, 0),
            ctypes.byref(rect)
        )
    
    def optimize_frame_rate(self):
        """Ограничение частоты кадров для предотвращения излишнего рендеринга"""
        current_time = time.time()
        elapsed = current_time - self.last_frame_time
        target_frame_time = 1.0 / self.target_fps
        
        if elapsed < target_frame_time:
            time.sleep(target_frame_time - elapsed)
            
        self.last_frame_time = time.time()
    
    def write_output_buffer(self, buffer: List[List['ScreenPixel']], width: int, height: int):
        """Запись всего буфера в консоль за один вызов"""
        if not buffer or width <= 0 or height <= 0:
            return
        
        self.optimize_frame_rate()
        
        char_buffer = (CHAR_INFO * (width * height))()
        
        for y in range(height):
            for x in range(width):
                if y < len(buffer) and x < len(buffer[y]):
                    idx = y * width + x
                    
                    pixel = buffer[y][x]
                    char_buffer[idx].Char.UnicodeChar = pixel.char
                    
                    if pixel.bg_color == Color.RESET or pixel.bg_color == '':
                        bg_color = Color.BG_BLACK
                    else:
                        bg_color = pixel.bg_color
                    
                    char_buffer[idx].Attributes = self.ansi_to_win_attr(pixel.fg_color, bg_color)
        
        rect = wintypes.SMALL_RECT(0, 0, width - 1, height - 1)
        kernel32.WriteConsoleOutputW(
            self.handle,
            char_buffer,
            wintypes._COORD(width, height),
            wintypes._COORD(0, 0),
            ctypes.byref(rect)
        )
        
        self.prev_buffer = [row[:] for row in buffer]

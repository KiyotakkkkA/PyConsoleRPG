import ctypes
from ctypes import wintypes
import re
import time
import curses
import pygame
from pygame import Surface, Color as PygameColor
from src.services.output import Color

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
    pygame_color_cache = {}
    
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
        
        pygame.init()
        pygame.display.init()
        self.surface = Surface((self.width, self.height))
        self.surface.fill((0, 0, 0))
        
        self.prev_buffer = None
        
        self.target_fps = 30
        self.last_frame_time = time.time()
        
        self.use_curses = False
        self.curses_initialized = False
        self.stdscr = None
        
    def init_curses(self):
        """Инициализация curses"""
        if not self.curses_initialized:
            try:
                self.stdscr = curses.initscr()
                
                curses.start_color()
                curses.use_default_colors()
                curses.curs_set(0)
                self.stdscr.keypad(False)
                curses.noecho()
                curses.cbreak()
                curses.halfdelay(1)
                
                for i in range(1, 16):
                    curses.init_pair(i, i % 8, (i // 8) * 8)
                
                self.curses_initialized = True
                return True
            except Exception:
                if self.curses_initialized:
                    self.cleanup_curses()
            self.use_curses = False
            handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            kernel32.SetConsoleMode(handle, ENABLE_PROCESSED_OUTPUT | ENABLE_WRAP_AT_EOL_OUTPUT | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
            return False
        return self.curses_initialized
    
    def cleanup_curses(self):
        """Освобождение ресурсов curses и восстановление настроек терминала"""
        if self.curses_initialized:
            curses.nocbreak()
            self.stdscr.keypad(False)
            curses.echo()
            curses.endwin()
            self.curses_initialized = False
            
            handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            kernel32.SetConsoleMode(handle, ENABLE_PROCESSED_OUTPUT | ENABLE_WRAP_AT_EOL_OUTPUT | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
        
    def get_console_size(self):
        """Получение размеров консоли"""
        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        kernel32.GetConsoleScreenBufferInfo(self.handle, ctypes.byref(csbi))
        return csbi.dwSize.X, csbi.dwSize.Y
        
    def clear_screen(self):
        """Очистка экрана с использованием WinAPI вместо ANSI-последовательностей"""
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
        
        if isinstance(fg_color, str) and '|' in fg_color:
            for part in fg_color.split('|'):
                part = part.strip()
                if part in ANSI_TO_WIN_COLOR:
                    if 'BG_' in part:
                        win_code = ANSI_TO_WIN_COLOR[part]
                        if win_code < 16:
                            bg_attr |= win_code << 4
                        else:
                            bg_attr |= win_code
                    else:
                        text_attr = ANSI_TO_WIN_COLOR[part] & 0x0F
        
        if isinstance(bg_color, str) and '|' in bg_color:
            for part in bg_color.split('|'):
                part = part.strip()
                if part in ANSI_TO_WIN_COLOR:
                    if 'BG_' in part:
                        win_code = ANSI_TO_WIN_COLOR[part]
                        if win_code < 16:
                            bg_attr |= win_code << 4
                        else:
                            bg_attr |= win_code
                    else:
                        text_attr = ANSI_TO_WIN_COLOR[part] & 0x0F
        
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
        
    def ansi_to_pygame_color(self, color_code):
        """Преобразование ANSI-цвета в цвет PyGame"""
        if color_code in self.__class__.pygame_color_cache:
            return self.__class__.pygame_color_cache[color_code]
        
        color_map = {
            Color.BLACK: (0, 0, 0),
            Color.RED: (170, 0, 0),
            Color.GREEN: (0, 170, 0),
            Color.YELLOW: (170, 85, 0),
            Color.BLUE: (0, 0, 170),
            Color.MAGENTA: (170, 0, 170),
            Color.CYAN: (0, 170, 170),
            Color.WHITE: (170, 170, 170),
            
            Color.BG_BLACK: (0, 0, 0),
            Color.BG_RED: (170, 0, 0),
            Color.BG_GREEN: (0, 170, 0),
            Color.BG_YELLOW: (170, 85, 0),
            Color.BG_BLUE: (0, 0, 170),
            Color.BG_MAGENTA: (170, 0, 170),
            Color.BG_CYAN: (0, 170, 170),
            Color.BG_WHITE: (170, 170, 170),
            
            Color.BRIGHT_BLACK: (85, 85, 85),
            Color.BRIGHT_RED: (255, 85, 85),
            Color.BRIGHT_GREEN: (85, 255, 85),
            Color.BRIGHT_YELLOW: (255, 255, 85),
            Color.BRIGHT_BLUE: (85, 85, 255),
            Color.BRIGHT_MAGENTA: (255, 85, 255),
            Color.BRIGHT_CYAN: (85, 255, 255),
            Color.BRIGHT_WHITE: (255, 255, 255),
            
            Color.BG_BRIGHT_BLACK: (85, 85, 85),
            Color.BG_BRIGHT_RED: (255, 85, 85),
            Color.BG_BRIGHT_GREEN: (85, 255, 85),
            Color.BG_BRIGHT_YELLOW: (255, 255, 85),
            Color.BG_BRIGHT_BLUE: (85, 85, 255),
            Color.BG_BRIGHT_MAGENTA: (255, 85, 255),
            Color.BG_BRIGHT_CYAN: (85, 255, 255),
            Color.BG_BRIGHT_WHITE: (255, 255, 255),
            
            Color.RESET: (0, 0, 0),
        }
        
        if color_code in color_map:
            result = color_map[color_code]
            self.__class__.pygame_color_cache[color_code] = result
            return result
        
        if isinstance(color_code, str) and '|' in color_code:
            parts = color_code.split('|')
            for part in parts:
                part = part.strip()
                if part in color_map:
                    result = color_map[part]
                    self.__class__.pygame_color_cache[color_code] = result
                    return result
        
        if hasattr(color_code, 'code'):
            for color_name, color_obj in vars(Color).items():
                if not isinstance(color_obj, type) and hasattr(color_obj, 'code'):
                    if color_obj.code in color_code.code and color_obj in color_map:
                        result = color_map[color_obj]
                        self.__class__.pygame_color_cache[color_code] = result
                        return result
        
        default_color = (170, 170, 170) if not str(color_code).startswith('BG_') else (0, 0, 0)
        self.__class__.pygame_color_cache[color_code] = default_color
        return default_color
    
    def optimize_frame_rate(self):
        """Ограничение частоты кадров для предотвращения излишнего рендеринга"""
        current_time = time.time()
        elapsed = current_time - self.last_frame_time
        target_frame_time = 1.0 / self.target_fps
        
        if elapsed < target_frame_time:
            time.sleep(target_frame_time - elapsed)
            
        self.last_frame_time = time.time()
    
    def write_output_buffer(self, buffer, width, height):
        """Запись всего буфера в консоль за один вызов с использованием curses"""
        if not buffer or width <= 0 or height <= 0:
            return
        
        self.optimize_frame_rate()
        
        if self.use_curses and not self.curses_initialized:
            if not self.init_curses():
                handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
                kernel32.SetConsoleMode(handle, ENABLE_PROCESSED_OUTPUT | ENABLE_WRAP_AT_EOL_OUTPUT | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
        
        if self.use_curses and self.curses_initialized:
            try:
                changed_coords = []
                if self.prev_buffer is None:
                    for y in range(min(height, len(buffer))):
                        for x in range(min(width, len(buffer[y]))):
                            changed_coords.append((x, y))
                else:
                    for y in range(min(height, len(buffer))):
                        for x in range(min(width, len(buffer[y]))):
                            if (y >= len(self.prev_buffer) or 
                                x >= len(self.prev_buffer[y]) or 
                                buffer[y][x] != self.prev_buffer[y][x]):
                                changed_coords.append((x, y))
                
                for x, y in changed_coords:
                    if y < len(buffer) and x < len(buffer[y]):
                        pixel = buffer[y][x]
                        
                        fg_color = pixel.fg_color
                        bg_color = pixel.bg_color if pixel.bg_color != Color.RESET and pixel.bg_color != '' else Color.BG_BLACK
                        
                        attr = self.ansi_to_curses_attr(fg_color, bg_color)
                        
                        try:
                            self.stdscr.addch(y, x, ord(pixel.char), attr)
                        except curses.error:
                            pass
                
                self.stdscr.refresh()
                
                self.prev_buffer = [row[:] for row in buffer]
                return
            except Exception:
                self.cleanup_curses()
                self.use_curses = False
        
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

    def ansi_to_curses_attr(self, fg_color, bg_color):
        """Преобразование ANSI-цветов в атрибуты curses"""
        cache_key = (str(fg_color), str(bg_color))
        
        if cache_key in self.__class__.color_attr_cache:
            return self.__class__.color_attr_cache[cache_key]
        
        fg_map = {
            Color.BLACK: curses.COLOR_BLACK,
            Color.RED: curses.COLOR_RED,
            Color.GREEN: curses.COLOR_GREEN,
            Color.YELLOW: curses.COLOR_YELLOW,
            Color.BLUE: curses.COLOR_BLUE,
            Color.MAGENTA: curses.COLOR_MAGENTA,
            Color.CYAN: curses.COLOR_CYAN,
            Color.WHITE: curses.COLOR_WHITE,
            Color.BRIGHT_BLACK: curses.COLOR_BLACK + 8,
            Color.BRIGHT_RED: curses.COLOR_RED + 8,
            Color.BRIGHT_GREEN: curses.COLOR_GREEN + 8,
            Color.BRIGHT_YELLOW: curses.COLOR_YELLOW + 8,
            Color.BRIGHT_BLUE: curses.COLOR_BLUE + 8,
            Color.BRIGHT_MAGENTA: curses.COLOR_MAGENTA + 8,
            Color.BRIGHT_CYAN: curses.COLOR_CYAN + 8,
            Color.BRIGHT_WHITE: curses.COLOR_WHITE + 8,
        }
        
        bg_map = {
            Color.BG_BLACK: curses.COLOR_BLACK,
            Color.BG_RED: curses.COLOR_RED,
            Color.BG_GREEN: curses.COLOR_GREEN,
            Color.BG_YELLOW: curses.COLOR_YELLOW,
            Color.BG_BLUE: curses.COLOR_BLUE,
            Color.BG_MAGENTA: curses.COLOR_MAGENTA,
            Color.BG_CYAN: curses.COLOR_CYAN,
            Color.BG_WHITE: curses.COLOR_WHITE,
            Color.BG_BRIGHT_BLACK: curses.COLOR_BLACK + 8,
            Color.BG_BRIGHT_RED: curses.COLOR_RED + 8,
            Color.BG_BRIGHT_GREEN: curses.COLOR_GREEN + 8,
            Color.BG_BRIGHT_YELLOW: curses.COLOR_YELLOW + 8,
            Color.BG_BRIGHT_BLUE: curses.COLOR_BLUE + 8,
            Color.BG_BRIGHT_MAGENTA: curses.COLOR_MAGENTA + 8,
            Color.BG_BRIGHT_CYAN: curses.COLOR_CYAN + 8,
            Color.BG_BRIGHT_WHITE: curses.COLOR_WHITE + 8,
        }
        
        fg = curses.COLOR_WHITE
        bg = curses.COLOR_BLACK
        attr = 0
        if fg_color in fg_map:
            fg = fg_map[fg_color]
        elif isinstance(fg_color, str) and '|' in fg_color:
            for part in fg_color.split('|'):
                part = part.strip()
                if part in fg_map:
                    fg = fg_map[part]
        elif hasattr(fg_color, 'code'):
            for color_name, color_obj in vars(Color).items():
                if not isinstance(color_obj, type) and hasattr(color_obj, 'code'):
                    if color_obj.code in fg_color.code and color_obj in fg_map:
                        fg = fg_map[color_obj]
        
        if bg_color in bg_map:
            bg = bg_map[bg_color]
        elif isinstance(bg_color, str) and '|' in bg_color:
            for part in bg_color.split('|'):
                part = part.strip()
                if part in bg_map:
                    bg = bg_map[part]
        elif hasattr(bg_color, 'code'):
            for color_name, color_obj in vars(Color).items():
                if not isinstance(color_obj, type) and hasattr(color_obj, 'code'):
                    if color_obj.code in bg_color.code and color_obj in bg_map:
                        bg = bg_map[color_obj]
        
        pair_num = (fg % 8) + ((bg % 8) * 8)
        if pair_num == 0:
            pair_num = 1
        
        attr = curses.color_pair(pair_num)
        
        if fg >= 8 or bg >= 8:
            attr |= curses.A_BOLD
        
        self.__class__.color_attr_cache[cache_key] = attr
        
        return attr
    
    def __del__(self):
        """Освобождение ресурсов при уничтожении объекта"""
        if hasattr(self, 'curses_initialized') and self.curses_initialized:
            self.cleanup_curses()

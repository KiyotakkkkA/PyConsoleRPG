class ColorCode:
    def __init__(self, code):
        self.code = code
    
    def __or__(self, other):
        if isinstance(other, ColorCode):
            return ColorCode(self.code + other.code)
        return NotImplemented
    
    def __str__(self):
        return self.code
    
    def __call__(self, text):
        """Применяет цветовое форматирование к тексту"""
        return f"{self.code}{text}\033[0m"
    
    def __repr__(self):
        return f"ColorCode('{self.code}')"
    
    def startswith(self, prefix):
        return self.code.startswith(prefix)

class Color:
    BLACK = ColorCode("\033[30m")
    RED = ColorCode("\033[31m")
    GREEN = ColorCode("\033[32m")
    YELLOW = ColorCode("\033[33m")
    BLUE = ColorCode("\033[34m")
    MAGENTA = ColorCode("\033[35m")
    CYAN = ColorCode("\033[36m")
    WHITE = ColorCode("\033[37m")
    
    BOLD_BLACK = ColorCode("\033[1;30m")
    BOLD_RED = ColorCode("\033[1;31m")
    BOLD_GREEN = ColorCode("\033[1;32m")
    BOLD_YELLOW = ColorCode("\033[1;33m")
    BOLD_BLUE = ColorCode("\033[1;34m")
    BOLD_MAGENTA = ColorCode("\033[1;35m")
    BOLD_CYAN = ColorCode("\033[1;36m")
    BOLD_WHITE = ColorCode("\033[1;37m")
    
    UNDERLINE_BLACK = ColorCode("\033[4;30m")
    UNDERLINE_RED = ColorCode("\033[4;31m")
    UNDERLINE_GREEN = ColorCode("\033[4;32m")
    UNDERLINE_YELLOW = ColorCode("\033[4;33m")
    UNDERLINE_BLUE = ColorCode("\033[4;34m")
    UNDERLINE_MAGENTA = ColorCode("\033[4;35m")
    UNDERLINE_CYAN = ColorCode("\033[4;36m")
    UNDERLINE_WHITE = ColorCode("\033[4;37m")
    
    BG_BLACK = ColorCode("\033[40m")
    BG_RED = ColorCode("\033[41m")
    BG_GREEN = ColorCode("\033[42m")
    BG_YELLOW = ColorCode("\033[43m")
    BG_BLUE = ColorCode("\033[44m")
    BG_MAGENTA = ColorCode("\033[45m")
    BG_CYAN = ColorCode("\033[46m")
    BG_WHITE = ColorCode("\033[47m")
    
    BRIGHT_BLACK = ColorCode("\033[0;90m")
    BRIGHT_RED = ColorCode("\033[0;91m")
    BRIGHT_GREEN = ColorCode("\033[0;92m")
    BRIGHT_YELLOW = ColorCode("\033[0;93m")
    BRIGHT_BLUE = ColorCode("\033[0;94m")
    BRIGHT_MAGENTA = ColorCode("\033[0;95m")
    BRIGHT_CYAN = ColorCode("\033[0;96m")
    BRIGHT_WHITE = ColorCode("\033[0;97m")
    
    BOLD_BRIGHT_BLACK = ColorCode("\033[1;90m")
    BOLD_BRIGHT_RED = ColorCode("\033[1;91m")
    BOLD_BRIGHT_GREEN = ColorCode("\033[1;92m")
    BOLD_BRIGHT_YELLOW = ColorCode("\033[1;93m")
    BOLD_BRIGHT_BLUE = ColorCode("\033[1;94m")
    BOLD_BRIGHT_MAGENTA = ColorCode("\033[1;95m")
    BOLD_BRIGHT_CYAN = ColorCode("\033[1;96m")
    BOLD_BRIGHT_WHITE = ColorCode("\033[1;97m")
    
    BG_BRIGHT_BLACK = ColorCode("\033[0;100m")
    BG_BRIGHT_RED = ColorCode("\033[0;101m")
    BG_BRIGHT_GREEN = ColorCode("\033[0;102m")
    BG_BRIGHT_YELLOW = ColorCode("\033[0;103m")
    BG_BRIGHT_BLUE = ColorCode("\033[0;104m")
    BG_BRIGHT_MAGENTA = ColorCode("\033[0;105m")
    BG_BRIGHT_CYAN = ColorCode("\033[0;106m")
    BG_BRIGHT_WHITE = ColorCode("\033[0;107m")
    
    RESET = ColorCode("\033[0m")
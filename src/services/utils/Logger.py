from src.config import Config
from enum import Enum
import os
import datetime
import inspect
import sys
import traceback

class LogLevel(Enum):
    DEBUG = (0, "\033[94m", "DEBUG")
    INFO = (1, "\033[92m", "INFO")
    WARNING = (2, "\033[93m", "WARNING")
    ERROR = (3, "\033[91m", "ERROR")
    CRITICAL = (4, "\033[95m", "CRITICAL")

class Logger:
    """
    Класс для логирования сообщений в файл и консоль
    """
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self, log_file=Config.LOGS_DIR + "/logs.log", min_level=LogLevel.INFO, console_output=False):
        """
        Инициализация логгера
        
        Args:
            log_file: Путь к файлу логов
            min_level: Минимальный уровень логирования
            console_output: Флаг вывода логов в консоль (по умолчанию False)
        """
        self.log_file = log_file
        self.min_level = min_level
        self.console_output = console_output
        
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        if not os.path.exists(log_file):
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"=== Запуск логирования {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    
    def _log(self, level, message, *args):
        """
        Внутренний метод для записи лога
        
        Args:
            level: Уровень логирования
            message: Сообщение
            *args: Аргументы для форматирования сообщения
        """
        if level.value[0] < self.min_level.value[0]:
            return
            
        if args:
            message = message.format(*args)
            
        frame = inspect.currentframe().f_back.f_back
        filename = os.path.basename(frame.f_code.co_filename)
        lineno = frame.f_lineno
        caller_func = frame.f_code.co_name
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted_message = f"[{timestamp}] {level.value[2]:8} | {filename}:{lineno} ({caller_func}) | {message}"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(formatted_message + '\n')
        
        if self.console_output:
            color_code = level.value[1]
            print(f"{color_code}{formatted_message}\033[0m")
    
    def debug(self, message, *args):
        """
        Логирование отладочной информации
        
        Args:
            message: Сообщение
            *args: Аргументы для форматирования сообщения
        """
        self._log(LogLevel.DEBUG, message, *args)
    
    def info(self, message, *args):
        """
        Логирование информационных сообщений
        
        Args:
            message: Сообщение
            *args: Аргументы для форматирования сообщения
        """
        self._log(LogLevel.INFO, message, *args)
    
    def warning(self, message, *args):
        """
        Логирование предупреждений
        
        Args:
            message: Сообщение
            *args: Аргументы для форматирования сообщения
        """
        self._log(LogLevel.WARNING, message, *args)
    
    def error(self, message, *args):
        """
        Логирование ошибок
        
        Args:
            message: Сообщение
            *args: Аргументы для форматирования сообщения
        """
        self._log(LogLevel.ERROR, message, *args)
    
    def critical(self, message, *args):
        """
        Логирование критических ошибок
        
        Args:
            message: Сообщение
            *args: Аргументы для форматирования сообщения
        """
        self._log(LogLevel.CRITICAL, message, *args)
        
    def exception(self, message, exc_info=None):
        """
        Логирование исключений с трассировкой стека
        
        Args:
            message: Сообщение
            exc_info: Информация об исключении
        """
        if exc_info is None:
            exc_info = sys.exc_info()
        
        if exc_info[0] is not None:
            tb_lines = traceback.format_exception(*exc_info)
            error_message = f"{message}\n{''.join(tb_lines)}"
            self._log(LogLevel.ERROR, error_message)
        else:
            self._log(LogLevel.ERROR, message) 
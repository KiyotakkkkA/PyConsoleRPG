import time
import psutil
import gc
import sys
from src.services.output import Color
from src.services.frontend.core import Alignment
from src.services.frontend.ui.containers import Panel
from src.services.frontend.ui.general import Text

class PerformanceChecker(Panel):
    """
    Компонент для отображения подробной информации о производительности приложения
    """
    def __init__(self, x=0, y=0, width=40, height=14):
        """
        Инициализация компонента PerformanceChecker
        
        Args:
            x: Координата x компонента
            y: Координата y компонента
            width: Ширина компонента
            height: Высота компонента
        """
        super().__init__(x, y, width, height, "Производительность", " ", 
                         Alignment.LEFT, (1, 1, 1, 1), 
                         Color.BRIGHT_RED, Color.BLACK, Color.BRIGHT_WHITE)
        
        self.process = psutil.Process()
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.frame_count = 0
        self.total_frames = 0
        self.fps = 0
        self.avg_fps = 0
        self.update_interval = 1.0
        
        self.memory_usage = 0
        self.peak_memory = 0
        self.cpu_usage = 0
        self.obj_count = 0
        
        self.run_time = 0
        self.frame_time = 0
        self.gc_stats = None
        gc.enable()
        
        self.header_text = Text(1, 1, "Основные показатели:", fg_color=Color.BRIGHT_CYAN)
        self.fps_text = Text(1, 2, "FPS: 0 (Средний: 0)")
        self.frame_time_text = Text(1, 3, "Время кадра: 0 мс")
        self.cpu_text = Text(1, 4, "CPU: 0%")
        self.separator = Text(1, 5, "")
        
        self.memory_header = Text(1, 6, "Память:", fg_color=Color.BRIGHT_CYAN)
        self.memory_text = Text(1, 7, "Текущая: 0 МБ | Пик: 0 МБ")
        self.obj_count_text = Text(1, 8, "Объектов Python: 0")
        
        self.add_children([self.header_text, self.fps_text, self.frame_time_text, self.cpu_text,
                           self.separator, self.memory_header, self.memory_text, self.obj_count_text],
                                       ["header_text", "fps_text", "frame_time_text", "cpu_text",
                                        "separator", "memory_header", "memory_text", "obj_count_text"])
        
    
    def update(self):
        """
        Обновление информации о производительности
        """
        self.frame_count += 1
        current_time = time.time()
        elapsed_time = current_time - self.last_update_time
        
        if elapsed_time >= self.update_interval:
            self.fps = int(self.frame_count / elapsed_time)
            self.frame_count = 0
            self.last_update_time = current_time
            
            self.memory_usage = self.process.memory_info().rss / (1024 * 1024)
            self.obj_count = sys.getrefcount(self)
            self.cpu_usage = self.process.cpu_percent(interval=0)
            
            self.fps_text.set_text(f"FPS: {self.fps}")
            self.frame_time_text.set_text(f"Время кадра: {self.frame_time:.2f} мс")
            self.cpu_text.set_text(f"CPU: {self.cpu_usage:.1f}%")
            
            self.memory_text.set_text(f"Память: {self.memory_usage:.2f} МБ")
            self.obj_count_text.set_text(f"Объектов Python: {self.obj_count}")
            
            self.run_time = current_time - self.start_time
            self.frame_time = elapsed_time * 1000
            
            

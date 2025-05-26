from src.services.output import Color, Symbols
from src.services.frontend.core import Component

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.services.frontend.core.Screen import Screen

from src.services.frontend.core.Format import Alignment

class Panel(Component):
    def __init__(self, x: int, y: int, width: int,
                 height: int, title="Panel", filler=" ", title_alignment=Alignment.LEFT,
                 paddings: tuple = (1, 1, 1, 1),
                 border_color: str = Color.WHITE,
                 filler_color: str = Color.RESET,
                 title_color: str = Color.RESET,
                 border_color_selected: str = Color.BOLD_BRIGHT_RED):
        """
        Инициализация компонента Панель
        
        Args:
            x: Координата x компонента
            y: Координата y компонента
            width: Ширина компонента
            height: Высота компонента
            title: Заголовок компонента (по умолчанию 'Panel')
            filler: Заполнитель компонента (по умолчанию ' ')
            title_alignment: Выравнивание заголовка компонента (по умолчанию Alignment.LEFT)
            paddings: (pt, pb, pr, pl) по умолчанию (1, 1, 1, 1)
            border_color: Цвет границ компонента (по умолчанию Color.WHITE)
            filler_color: Цвет заполнителя компонента (по умолчанию Color.RESET)
            title_color: Цвет заголовка компонента (по умолчанию Color.RESET)
            border_color_selected: Цвет границ компонента при выборе (по умолчанию Color.BOLD_BRIGHT_RED)
        """  
        super().__init__(x, y, width, height, paddings)
        
        self.reactive('title', title)
        self.reactive('title_x', 0)
        self.reactive('filler', filler)
        self.reactive('title_alignment', title_alignment)
        
        self.reactive('filler_color', filler_color)
        self.reactive('border_color', border_color)
        self.reactive('border_color_selected', border_color_selected)
        self.reactive('title_color', title_color)
        
        self.reactive('selected', False)
        
        self.computed('true_width', lambda: max(len(self.title) + 2, self.width - 2), ['title', 'width'])
        
    def set_title(self, title: str):
        self.title = title
        
    def set_selected(self, selected: bool):
        self.selected = selected
        
    def calculate(self):
        """
        Вычисление размеров компонента
        """
        self._calculate_self_size()
        
        if self.title_alignment == Alignment.LEFT:
            self.title_x = self.x + 2
        elif self.title_alignment == Alignment.RIGHT:
            self.title_x = self.x + self.true_width - len(self.title) - 2
        elif self.title_alignment == Alignment.CENTER:
            self.title_x = self.x + (self.true_width // 2) - (len(self.title) // 2)
        
    
    def draw(self, screen: 'Screen'):
        """
        Отрисовка компонента на экране
        
        Args:
            screen: Экран, на который производится отрисовка
        """
        self.calculate()
        
        color = self.border_color
        if self.selected:
            color = self.border_color_selected
            
        screen.draw_text(self.x, self.y, "{}{}{}".format(Symbols.BORDERS.TOP_LEFT, Symbols.BORDERS.TOP * self.true_width, Symbols.BORDERS.TOP_RIGHT), color, Color.RESET)
        screen.draw_text(self.x, self.y + self.height - 1, "{}{}{}".format(Symbols.BORDERS.BOTTOM_LEFT, Symbols.BORDERS.BOTTOM * self.true_width, Symbols.BORDERS.BOTTOM_RIGHT), color, Color.RESET)
        for cy in range(self.y + 1, self.y + self.height - 1):
            screen.draw_text(self.x, cy, Symbols.BORDERS.LEFT, color, Color.RESET)
            screen.draw_text(self.x + 1, cy, "{}".format(self.filler * self.true_width), self.filler_color, Color.RESET)
            screen.draw_text(self.x + self.true_width + 1, cy, Symbols.BORDERS.RIGHT, color, Color.RESET)
        screen.draw_text(self.title_x, self.y, self.title, self.title_color, Color.RESET)
            
        for child in self.children:
            child.draw(screen)
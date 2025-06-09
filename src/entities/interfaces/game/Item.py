from src.services.output import Color
from enum import Enum


class ItemTypes(Enum):
    """
    Тип предмета
    """
    MATERIAL = ("material", "Материал", Color.BRIGHT_CYAN)
    """Материалы"""


class Rarity(Enum):
    """
    Редкость предмета
    """
    COMMON = ("Простой", "Прост.", Color.WHITE)
    
    """
    Простой
    """
    UNCOMMON = ("Необычный", "Необ.", Color.BRIGHT_GREEN)
    
    """
    Необычный
    """
    RARE = ("Редкий", "Редк.", Color.BRIGHT_BLUE)
    
    """
    Редкий
    """
    EPIC = ("Великолепный", "Велик.", Color.BRIGHT_MAGENTA)
    
    """
    Великолепный
    """
    LEGENDARY = ("Легендарный", "Легенд.", Color.YELLOW)
    
    """
    Легендарный
    """
    MYTHIC = ("Мифический", "Миф.", Color.BRIGHT_RED)
    
    """
    Мифический
    """
    


class Item:
    def __init__(self):
        self._id: int = None
        self._name: str = None
        self._description: str = None
        self._type: ItemTypes = None
        self._rarity: Rarity = None
        self._price: int = None
        self._weight: int = None
        
        self._level_need: int = None
        
    @property
    def id(self):
        """
        Уникальный идентификатор предмета
        """
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = f"{self._type.value[0]}_{value}"
        
    @property
    def name(self):
        """
        Название предмета
        """
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
        
    @property
    def description(self):
        """
        Описание предмета
        """
        return self._description
    
    @description.setter
    def description(self, value):
        self._description = value
        
    @property
    def type(self):
        """
        Тип предмета
        """
        return self._type
    
    @type.setter
    def type(self, value):
        self._type = value
        
    @property
    def rarity(self):
        """
        Редкость предмета
        """
        return self._rarity
    
    @rarity.setter
    def rarity(self, value):
        self._rarity = value
        
    @property
    def price(self):
        """
        Цена предмета
        """
        return self._price
    
    @price.setter
    def price(self, value):
        self._price = value
        
    @property
    def level_need(self):
        """
        Уровень, необходимый для предмета
        """
        return self._level_need
    
    @level_need.setter
    def level_need(self, value):
        self._level_need = value
        
    @property
    def weight(self):
        """
        Вес предмета
        """
        return self._weight
    
    @weight.setter
    def weight(self, value):
        self._weight = value
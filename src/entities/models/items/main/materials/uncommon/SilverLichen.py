from src.entities.interfaces.game import Material
from src.entities.interfaces.game.Item import Rarity

class SilverLichen(Material):
    def __init__(self):
        super().__init__()
        self.id = "silver_lichen"
        
        self.name = "Серебряный лишайник"
        
        self.description = "Уникальный вид лишайника, растущий только в Эльмирском Лесу, славится своими противодействием ядам."
        self.price = 0
        
        self.level_need = 2
        self.weight = 0.07
        
        self.rarity = Rarity.UNCOMMON
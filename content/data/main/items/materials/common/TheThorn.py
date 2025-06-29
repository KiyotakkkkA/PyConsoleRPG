from src.entities.interfaces.game import Material
from src.entities.interfaces.game.Item import Rarity

class TheThorn(Material):
    def __init__(self):
        super().__init__()
        self.id = "main_the_thorn"
        
        self.name = "Колючник"
        
        self.description = "Привередливый кустарник, но из его плодов готовят простые эликсиры."
        self.price = 0
        
        self.rarity = Rarity.COMMON
        self.weight = 0.05
        
        self.respawn_time = 5
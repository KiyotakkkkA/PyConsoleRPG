from src.entities.interfaces.game.Item import Item, ItemTypes

class Material(Item):
    def __init__(self):
        super().__init__()
        
        self.type = ItemTypes.MATERIAL
        
        self._respawn_time: int | None = None
        
    @property
    def respawn_time(self):
        """
        Время восстановления ресурса на локации (в секундах)
        """
        return self._respawn_time
    
    @respawn_time.setter
    def respawn_time(self, value):
        self._respawn_time = value
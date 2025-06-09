from src.entities.interfaces.game.Item import Item, ItemTypes

class Material(Item):
    def __init__(self):
        super().__init__()
        
        self.type = ItemTypes.MATERIAL
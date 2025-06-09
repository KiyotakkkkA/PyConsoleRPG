from src.entities.interfaces.game import Region

class SwardenfallEmpire(Region):
    def __init__(self):
        super().__init__()
        self.id = "main_swardenfall_empire"
        self.name = "Империя Сварденфолл"
        self.description = "Воинственная империя, расположившаяся на востоке континента. По слухам - армия Сварденфолла могла бы подчинить себе Королевство Тиренхолл, если бы их не разделял Великий Эльмирский Лес."

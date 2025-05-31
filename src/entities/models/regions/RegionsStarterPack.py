from src.entities.interfaces.game import Region

class TierenhallKingdom(Region):
    def __init__(self):
        super().__init__()
        self.id = "main_tierenhall_kingdom"
        self.name = "Королевство Тиренхолл"
        self.description = "Огромное королевство, расположившееся на западе континента. Обладает особой культурой и развитой экономикой."
        

class GreatElmiraForest(Region):
    def __init__(self):
        super().__init__()
        self.id = "main_great_elmira_forest"
        self.name = "Великий Лес Эльмира"
        self.description = "Великий лес, расположенный в середине континента. Является естественной границей между Королевством Тиренхолл и Империей Сварденфолл."


class SwardenfallEmpire(Region):
    def __init__(self):
        super().__init__()
        self.id = "main_swardenfall_empire"
        self.name = "Империя Сварденфолл"
        self.description = "Воинственная империя, расположившаяся на востоке континента. По слухам - армия Сварденфолла могла бы подчинить себе Королевство Тиренхолл, если бы их не разделял Великий Эльмирский Лес."

class NPC:
    """
    Интерфейс для NPC
    """
    
    def __init__(self):
        self._id = None
        self._name = None
        
    @property
    def id(self):
        """
        Уникальный идентификатор NPC (id из json текущей локализации)
        """
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value
    
    @property
    def name(self):
        """
        Название NPC
        """
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
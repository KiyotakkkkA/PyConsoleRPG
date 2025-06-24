class Region:
    """
    Интерфейс для региона
    """
    
    def __init__(self):
        self._id = None
        self._name = None
        self._description = None
        
    @property
    def id(self):
        """
        Уникальный идентификатор региона
        """
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value
    
    @property
    def name(self):
        """
        Название региона
        """
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def description(self):
        """
        Описание региона
        """
        return self._description
        
    @description.setter
    def description(self, value):
        self._description = value
    
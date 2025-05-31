class Location:
    def __init__(self):
        self.id = None
        self._name = None
        self._description = None
        
    @property
    def id(self):
        """
        Уникальный идентификатор локации
        """
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value
    
    @property
    def name(self):
        """
        Название локации
        """
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def description(self):
        """
        Описание локации
        """
        return self._description
        
    @description.setter
    def description(self, value):
        self._description = value
        
    @property
    def region(self):
        """
        Регион, в котором находится локация
        """
        return self._region
    
    @region.setter
    def region(self, value):
        self._region = value
    
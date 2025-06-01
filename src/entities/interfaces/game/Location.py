class Location:
    def __init__(self):
        self._id = None
        self._name = None
        self._description = None
        self._region = None
        self._connections = []
        
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
        
    @property
    def connections(self):
        """
        Список доступных для перехода локаций
        """
        return self._connections
    
    @connections.setter
    def connections(self, value):
        self._connections = value
    
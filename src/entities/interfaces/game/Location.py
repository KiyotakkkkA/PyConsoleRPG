class Location:
    """
    Интерфейс для локации
    """
    
    def __init__(self):
        self._id = None
        self._name = None
        self._description = None
        self._region = None
        self._connections = {}
        self._resources = {}
        self._npcs = []
        
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
        Словарь доступных для перехода локаций
        """
        return self._connections
    
    @connections.setter
    def connections(self, value):
        self._connections = value
        
    @property
    def resources(self):
        """
        Словарь доступных для сбора ресурсов
        """
        return self._resources
    
    @resources.setter
    def resources(self, value):
        self._resources = value
    
    @property
    def npcs(self):
        """
        Список NPC на локации
        """
        return self._npcs
    
    @npcs.setter
    def npcs(self, value):
        self._npcs = value
    
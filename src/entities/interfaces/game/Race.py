class Race:
    """
    Интерфейс для расы
    """
    
    def __init__(self):
        self._id = None
        self._name = None
        self._description = None
        
        self._race_chars = {
            'constitution': None,
            'intelligence': None,
            'endurance': None
        }
        
    @property
    def id(self):
        """
        Уникальный идентификатор расы
        """
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value
    
    @property
    def name(self):
        """
        Название расы (id из json текущей локализации)
        """
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def description(self):
        """
        Описание расы (id из json текущей локализации)
        """
        return self._description
    
    @description.setter
    def description(self, value):
        self._description = value
        
    @property
    def base_constitution(self):
        """
        Базовое телосложение
        """
        return self._race_chars['constitution']
    
    @property
    def base_intelligence(self):
        """
        Базовый интеллект
        """
        return self._race_chars['intelligence']
    
    @property
    def base_endurance(self):
        """
        Базовая выносливость
        """
        return self._race_chars['endurance']
    
    @base_constitution.setter
    def base_constitution(self, value):
        self._race_chars['constitution'] = value
    
    @base_intelligence.setter
    def base_intelligence(self, value):
        self._race_chars['intelligence'] = value
    
    @base_endurance.setter
    def base_endurance(self, value):
        self._race_chars['endurance'] = value
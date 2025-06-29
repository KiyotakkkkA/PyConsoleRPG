from src.services.backend.managers import ContentManager, LocaleManager
from src.services.utils import Logger
from abc import ABC, abstractmethod
from copy import deepcopy
import pkgutil
import importlib
import inspect

class Registry(ABC):
    """
    Базовый класс для регистраторов
    """
    
    _logger = Logger().get_instance()
    
    def setup_entities(self, entity_type: type, entity_group_name: str):
        """
        Подготовка регистратора на обработку указанного типа сущностей
        """
        self._logger.info(f"Получение информации о типе: <{entity_type.__name__}>")
        
        entity_dirs_attr_name = entity_group_name + "_dirs"
        
        setattr(self, entity_group_name, [])
        setattr(self, entity_dirs_attr_name, self._content_manager.get_modules(entity_group_name))
        
        entity_count = 0
        
        for entity_dir in getattr(self, entity_dirs_attr_name):
            for _, name, _ in pkgutil.walk_packages(entity_dir.__path__, entity_dir.__name__ + "."):
                module = importlib.import_module(name)
                for _, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, entity_type) and obj is not entity_type:
                        getattr(self, entity_group_name).append(obj())
                        entity_count += 1
                        
        self._logger.info(f"Загружено {entity_count} сущностей: <{entity_type.__name__}>")
    
    def __init__(self):
        self._content_manager = ContentManager.get_instance()
        self._locale_manager = LocaleManager.get_instance()
        self._json_view = {}
    
    def get_json_view(self):
        """
        Получение Атласа сущностей в формате JSON
        """
        return deepcopy(self._json_view)
    
    def get_by_id(self, id: str):
        """
        Получение сущности по ID
        """
        return deepcopy(self._json_view.get(id, None))
    
    @abstractmethod
    def load_to_json(self):
        """
        Загрузка сущностей в JSON
        """
        pass
    
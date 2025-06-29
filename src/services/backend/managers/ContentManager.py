from src.config.Config import Config
from src.services.utils import Logger
from types import ModuleType
import sys
import os
import json

class ContentManager:
    
    _instance = None
    
    _logger = Logger().get_instance()
    
    _types = {
        "items": "items",
        "locations": "locations",
        "regions": "regions",
        "races": "races",
        "npcs": "npcs"
    }
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        self.content = []
        self.modules = {}
        
        self.find_content()
        
    def get_content(self) -> list:
        """
        Получает список содержимого
        
        Returns:
            list: Список содержимого
        """
        return self.content
    
    def get_modules(self, key: str = None) -> list:
        """
        Получает список модулей
        
        Returns:
            list: Список модулей
        """
        return list(self.modules.get(key, None))
    
    def find_content(self):
        self._logger.info(f"Начало поиска содержимого...")
        for entity in os.listdir(Config.DATA_DIR):
            manifest = os.path.join(Config.DATA_DIR, entity, 'manifest.json')
            
            if os.path.exists(manifest):
                with open(manifest, 'r') as f:
                    data = json.load(f)
                    path = os.path.join(Config.DATA_DIR, entity)
                    abs_path = os.path.abspath(os.path.normpath(path))
                    
                    data["path"] = abs_path
                    
                    self.content.append(data)
                    
                    for _type in self._types:
                        if os.path.exists(os.path.join(path, _type)):
                             if _type in sys.modules:
                                 _module = sys.modules[_type]
                                 if abs_path not in _module.__path__:
                                     _module.__path__.append(abs_path)
                             else:
                                 _module = ModuleType(_type)
                                 _module.__path__ = [abs_path]
                                 sys.modules[_type] = _module
                             
                             if not self.modules.get(_type, None):
                                 self.modules[_type] = set()
                             self.modules[_type].add(_module)
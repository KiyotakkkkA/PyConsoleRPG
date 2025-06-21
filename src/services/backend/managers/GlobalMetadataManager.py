from src.config.Config import Config
import json

class GlobalMetadataManager:
    
    __instance = None
    
    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance
    
    def __init__(self):
        self.__global_meta = {}
        self.__load_global_meta()
        
    def get_value(self, key: str, default_value: any = None):
        """
        Получение значения метаданных по ключу
        
        Args:
            key: Ключ
            default_value: Значение по умолчанию
        """
        return self.__global_meta.get(key, default_value)
    
    def set_value(self, key: str, value: any):
        """
        Установка значения метаданных по ключу
        
        Args:
            key: Ключ
            value: Значение
        """
        self.__change_meta_with_key(key, value)
    
    def __load_global_meta(self):
        try:
            with open(f"{Config.SAVES_DIR}/{Config.GLOBAL_META_FILE}", "r") as f:
                self.__global_meta = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.__global_meta = {}
            
    def __change_meta_with_key(self, key: str, value: any):
        self.__global_meta[key] = value
        with open(f"{Config.SAVES_DIR}/{Config.GLOBAL_META_FILE}", "w") as f:
            json.dump(self.__global_meta, f)
from src.config.Config import Config
import os
import json

class LocaleManager:
    LOCALE_DIR = Config.LOCALE_DIR
    
    __instance = None
    
    __current_locale: str = None
    __current_locales: dict[str, dict[str, str]] = {}
    __current_locale_atlas = {}
    
    __base_locale: str = 'ru'
    
    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance
    
    def __init__(self):
        self.__load_locales_meta()
        self.set_locale(self.__base_locale)
        
    def __getitem__(self, key: str):
        return self.__current_locale_atlas.get(key, self.__current_locales[self.__current_locale]['error_msg'])
    
    def set_locale(self, locale: str):
        self.__current_locale = locale
        self.__load_current_locale()
        
    def get_current_locale_atlas(self) -> dict[str, str]:
        """
        Получение текущей локализации
        """
        return self.__current_locale_atlas
    
    def get_current_locales(self) -> dict[str, dict[str, str]]:
        """
        Получение всех локализаций
        """
        return self.__current_locales
    
    def get_all_locales_as_list(self) -> list[str]:
        """
        Получение всех локализаций в виде списка (название)
        """
        return [locale['locale_name'] for locale in self.__current_locales.values()]
    
    def get_all_locales_as_dict(self) -> dict[str, str]:
        """
        Получение всех локализаций в виде словаря (код: название)
        """
        return {locale['locale']: locale['locale_name'] for locale in self.__current_locales.values()}
    
    def get_all_locales_as_tuple(self) -> list[tuple[str, str]]:
        """
        Получение всех локализаций в виде списка кортежей (код, название)
        """
        return [(locale['locale'], locale['locale_name']) for locale in self.__current_locales.values()]
    
    def __load_locales_meta(self):
        for locale in os.listdir(self.LOCALE_DIR):
            with open(f"{self.LOCALE_DIR}/{locale}/manifest.json", "r", encoding="utf-8") as f:
                locale_meta = json.load(f)
                self.__current_locales[locale] = locale_meta
        
    def __load_current_locale(self):
        for entity in os.walk(f"{self.LOCALE_DIR}/{self.__current_locale}"):
            if entity[2] and 'manifest.json' in entity[2]: continue
            
            dir_to_file = f"{self.LOCALE_DIR}{entity[0].split(self.LOCALE_DIR)[1]}"
            
            for file in entity[2]:
                with open(f"{dir_to_file}/{file}", "r", encoding="utf-8") as f:
                    locale_data = json.load(f)
                    self.__current_locale_atlas.update(locale_data)
            
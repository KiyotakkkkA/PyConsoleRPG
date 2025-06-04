from pickle import dumps, loads

class Serialiazble:
    """
    Интерфейс для сериализации и десериализации объекта
    """
    
    def export_fields_as_dict(self):
        """
        Экспортирует значения полей объекта в словарь
        """
        _res = {}
        for field in self.__dict__:
            _res[field] = getattr(self, field)
        return _res
    
    def import_dict_to_fields(self, data: dict):
        """
        Импортирует значения полей объекта из словаря
        """
        for field in data:
            setattr(self, field, data[field])
    
    def load_to_dat_file(self, file_path: str):
        """
        Загружает данные объекта из файла
        """
        with open(file_path, "wb") as f:
            f.write(dumps(self.export_fields_as_dict()))
            
    def load_from_dat_file(self, file_path: str):
        """
        Загружает данные объекта из файла
        """
        with open(file_path, "rb") as f:
            data = f.read()
            self.import_dict_to_fields(loads(data))
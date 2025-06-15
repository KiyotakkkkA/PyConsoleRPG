import json
import enum
from typing import Any, Dict, Union, TypeVar
import os

from src.entities.interfaces.game.Item import ItemTypes, Rarity

T = TypeVar('T', bound='Serializable')

class Serializable:
    """
    Интерфейс для сериализации и десериализации объекта
    """
    
    __exclude__ = {'_computed_values', '_dependencies', '_dirty_flags', 
                  '_compute_functions', '_subscriptions', '__exclude__', '__primitive_types__', '__conversions__', '__enums__'}
    
    __primitive_types__ = (int, str, float, bool, list, set, tuple, type(None))
    
    __allowed_ext__ = {
        '.json': True,
        '.dat': True,
    }
    
    __conversions__ = {
        'int': int,
        'str': str,
        'float': float,
        'bool': bool,
        'list': list,
        'set': set,
        'tuple': tuple,
    }
    
    __enums__ = {
        'ItemTypes': ItemTypes,
        'Rarity': Rarity,
    }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Сериализует объект в словарь с информацией о типах
        """
        result = {}
        
        for field, value in self.__dict__.items():
            if field in self.__exclude__:
                continue
            
            if callable(value):
                continue
            
            if isinstance(value, dict):
                filtered_dict = {}
                for k, v in value.items():
                    if not callable(v):
                        try:
                            filtered_dict[k] = self._serialize_value(k, v)
                        except TypeError:
                            continue
                result[field] = {'type': 'dict', 'value': filtered_dict}
                continue
            
            try:
                result[field] = self._serialize_value(field, value)
            except TypeError:
                continue
            
        return result
    
    def _serialize_value(self, field: str, value: Any) -> Dict[str, Union[str, Any]]:
        """
        Сериализует отдельное значение с сохранением информации о типе
        """
        if value is None:
            return {'type': 'None', 'value': None}
            
        if isinstance(value, enum.Enum):
            return {
                'type': 'Enum',
                'enum_type': value.__class__.__name__,
                'enum_value': value.name,
                'is_serializable': True,
            }
            
        if isinstance(value, dict):
            return {
                'type': 'dict',
                'value': {k: self._serialize_value(k, v) for k, v in value.items()},
                'is_serializable': True,
            }
            
        if isinstance(value, self.__primitive_types__):
            type_name = type(value).__name__
            
            if isinstance(value, set):
                return {'type': 'set', 'value': list(value)}
            if isinstance(value, tuple):
                return {'type': 'tuple', 'value': list(value)}
                
            return {'type': type_name, 'value': value}
            
        if hasattr(value, 'to_dict'):
            return {
                'type': value.__class__.__name__,
                'value': value.to_dict(),
                'is_serializable': True,
            }
            
        return {'type': type(value).__name__, 'value': str(value)}
    
    def from_dict(self, data: Dict[str, Any]):
        """
        Десериализует объект из словаря
        """
        _data = self._deserialize_value(data)
        return _data
    
    def _deserialize_value(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Десериализует отдельное значение с учетом его типа
        """
        for field in data.keys():
            _type = data[field]['type']
            if self.__conversions__.get(_type) is not None and _type != 'dict':
                data[field] = self.__conversions__.get(_type)(data[field]['value'])
                continue
            if _type == 'dict':
                data[field] = self._deserialize_value(data[field]['value'])
                continue
            if _type == 'Enum':
                _curr_enum = self.__enums__.get(data[field]['enum_type'])
                if _curr_enum is not None:
                    data[field] = _curr_enum[data[field]['enum_value']]
                continue
        return data    
    
    def _to_json(self) -> str:
        """
        Сериализует объект в JSON строку
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    def dump_to_file(self, path: str):
        """
        Сериализует объект в JSON строку и записывает в файл
        """
        if os.path.splitext(path)[1] not in self.__allowed_ext__:
            raise ValueError(f"Недопустимый формат файла: {os.path.splitext(path)[1]}")
        if os.path.exists(path):
            os.remove(path)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self._to_json())
            
    def load_from_file(self, path: str) -> Dict[str, Any]:
        """
        Десериализует объект из JSON файла
        """
        if os.path.splitext(path)[1] not in self.__allowed_ext__:
            raise ValueError(f"Недопустимый формат файла: {os.path.splitext(path)[1]}")
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return self.from_dict(data)
        
    @classmethod
    def apply(cls, obj: T, path: str):
        data = obj.load_from_file(path)
        for field in data.keys():
            if field in obj.__dict__:
                setattr(obj, field.strip('_'), data[field])
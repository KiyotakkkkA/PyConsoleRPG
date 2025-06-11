from typing import Callable, Dict, Set, Any, Optional

class Computable:
    """
    Интерфейс для вычисляемых полей
    """
    
    def __init__(self):
        super().__init__()
        self._computed_values = {}
        self._dependencies = {}
        self._dirty_flags = {}
        self._compute_functions = {}
        self._subscriptions = {}
        
    def computed(self, name: str, compute_fn: Callable[[], Any], dependencies: list[str] = None):
        """
        Определяет вычисляемое поле
        
        Args:
            name: имя вычисляемого поля
            compute_fn: функция для вычисления значения
            dependencies: список имен полей, от которых зависит это поле
        """
        self._compute_functions[name] = compute_fn
        self._dirty_flags[name] = True
        self._dependencies[name] = set(dependencies) if dependencies else set()
        
        self._subscriptions[name] = []
        if dependencies:
            for dep in dependencies:
                handler = lambda data, field=name: self._mark_dirty(field)
                self._subscriptions[name].append((dep, handler))
                self.on_event(f"change:{dep}", handler)
                
        def getter(self=self, field_name=name):
            return self.get_computed(field_name)
        
        setattr(self.__class__, name, property(getter))
        
    def reactive(self, name: str, initial_value: Any = None):
        """
        Определяет реактивное поле, которое оповещает о своем изменении
        
        Args:
            name: имя реактивного поля
            initial_value: начальное значение
        """
        private_name = f"_{name}"
        setattr(self, private_name, initial_value)
        
        def getter(self=self, private=private_name):
            return getattr(self, private)
            
        def setter(self, value, private=private_name, field_name=name):
            old_value = getattr(self, private)
            if old_value != value:
                setattr(self, private, value)
                self.emit_event(f"change:{field_name}", {"old": old_value, "new": value})
                
        setattr(self.__class__, name, property(getter, setter))
        
    def _mark_dirty(self, name: str):
        """Помечает поле как требующее пересчета"""
        self._dirty_flags[name] = True
        
        for field, deps in self._dependencies.items():
            if name in deps:
                self._mark_dirty(field)
                
    def get_computed(self, name: str) -> Any:
        """Получает значение вычисляемого поля, при необходимости пересчитывает"""
        if name not in self._compute_functions:
            raise AttributeError(f"Вычисляемое поле '{name}' не определено")
            
        if self._dirty_flags.get(name, True):
            self._computed_values[name] = self._compute_functions[name]()
            self._dirty_flags[name] = False
            
        return self._computed_values[name]
        
    def __del__(self):
        """Отписываемся от всех событий при удалении объекта"""
        if hasattr(self, "unsubscribe"):
            for name, subs in self._subscriptions.items():
                for dep, handler in subs:
                    self.unsubscribe(f"change:{dep}", handler)
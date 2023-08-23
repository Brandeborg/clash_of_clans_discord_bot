from abc import ABC, abstractmethod

class Unit(ABC):
    def __init__(self, curr_level, name, unit_static: dict, th_level: int) -> None:
        self._th_level = th_level

        self.unit_static = unit_static
        self.curr_level = curr_level
        self.name = name
        self.max_level = self._get_max_level()
        self.max_level_th = self._get_max_level_th()

    @abstractmethod
    def _get_max_level_th(self):
        pass
    
    @abstractmethod
    def _get_max_level(self):
        pass
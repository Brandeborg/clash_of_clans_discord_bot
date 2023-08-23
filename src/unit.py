from abc import ABC, abstractmethod

class Unit(ABC):
    def __init__(self, curr_level, name, unit_static: dict) -> None:
        self.unit_static = unit_static
        self.curr_level = curr_level
        self.name = name

    @abstractmethod
    def get_max_level(self):
        pass

    @abstractmethod
    def get_max_level_th(self, th_level: int):
        pass
    
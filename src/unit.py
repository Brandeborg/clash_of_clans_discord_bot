from abc import ABC, abstractmethod
import bot_util

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

    def _get_upgrade_time(self, level: int, prefix: str) -> int:
        upgrade_time = 0

        h_key = prefix + "TimeH"
        d_key = prefix + "TimeD"

        if h_key in self.unit_static:
            upgrade_time += sum(self.unit_static[h_key][:level])

        if h_key in self.unit_static:
            upgrade_time += sum(self.unit_static[d_key][:level]) * 24

        return upgrade_time

    def _get_upgrade_cost(self, level: int, prefix: str) -> int:
        upgrade_cost = 0

        cost_key = prefix + "Cost"

        if cost_key in self.unit_static:
            upgrade_cost += sum(self.unit_static[cost_key][:level])

        return upgrade_cost
    
    def _get_upgrade_resource(self, prefix: str):
        name_map: dict = bot_util.load_json("../assets/pretty_name_map.json")

        resource_key = prefix + "Resource"

        return name_map["resource"][self.unit_static[resource_key][0]]
    
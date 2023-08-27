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

    def get_upgrade_time(self, level: int, prefix: str) -> int:
        upgrade_time = 0

        h_key = prefix + "TimeH"
        d_key = prefix + "TimeD"

        if h_key in self.unit_static:
            upgrade_time += sum(self.unit_static[h_key][:level])

        if d_key in self.unit_static:
            upgrade_time += sum(self.unit_static[d_key][:level]) * 24

        return upgrade_time

    def get_upgrade_cost(self, level: int, prefix: str) -> int:
        upgrade_cost = 0

        cost_key = prefix + "Cost"

        if cost_key in self.unit_static:
            upgrade_cost += sum(self.unit_static[cost_key][:level])

        return upgrade_cost
    
    def get_upgrade_resource(self, prefix: str):
        name_map: dict = bot_util.load_json("../assets/pretty_name_map.json")

        resource_key = prefix + "Resource"

        return name_map["resource"][self.unit_static[resource_key][0]]
    
    # static methods
    @staticmethod
    def display_units(units: list, unit_order: list, th_level: int) -> list[list]:
        # create list the length of units, 
        # so units can be placed directly at indices, in the right order
        display_lists = [None] * len(units)

        for unit in units:
            # list to hold unit attributes in a displayable manner
            # ex: ["name", "current level / max level", ...]
            display_list = []
            
            # name
            display_list.append(unit.name)

            # level
            max_level = unit.get_max_level_th(th_level)
            levels = f"{unit.curr_level} / {max_level}"
            display_list.append(levels)

            # time
            curr_time = unit.get_upgrade_time(unit.curr_level)
            dspl_curr_time = bot_util.display_hours_as_days(curr_time)
            max_time = unit.get_upgrade_time(max_level)
            dspl_max_time = bot_util.display_hours_as_days(max_time)

            time = f"{dspl_curr_time}{' / '}{dspl_max_time}"
            display_list.append(time)

            # cost
            curr_cost = bot_util.display_large_number(unit.get_upgrade_cost(unit.curr_level))
            max_cost = bot_util.display_large_number(unit.get_upgrade_cost(max_level))

            cost = f"{curr_cost}{' / '}{max_cost}"

            display_list.append(cost)

            # resource
            display_list.append(unit.get_upgrade_resource())

            i = unit_order.index(unit.name)
            display_lists[i] = display_list
        
        return display_lists
    
    @staticmethod
    def unit_is_available_th(production_building: str, th_level: int) -> bool:
        """Check whether a spell or troop can be available in the Forge / Barracks at th_level

        Returns:
            bool: A boolean value, true if unit is available at th_level
        """
        buildings = bot_util.load_json("../assets/buildings.json")
        pb_th_levels = buildings[production_building]["TownHallLevel"]
        return any(th_level >= pb_th_level for pb_th_level in pb_th_levels)


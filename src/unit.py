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
        name_map: dict = bot_util.load_json("assets/pretty_name_map.json")

        resource_key = prefix + "Resource"

        return name_map["resource"][self.unit_static[resource_key][0]]
    
    # static methods
    @staticmethod
    def display_units(units: list, unit_order: list) -> list[list]:
        # create list the length of units, 
        # so units can be placed directly at indices, in the right order
        display_lists = [None] * len(unit_order)

        for unit in units:
            # list to hold unit attributes in a displayable manner
            # ex: ["name", "remaining level / max level", ...]
            display_list = []
            
            # name
            display_list.append(unit["name"])

            # level
            levels = f"{unit['remaining_level']} / {unit['max_level']}"
            display_list.append(levels)

            # time
            dspl_curr_time = bot_util.display_hours_as_days(unit["remaining_time"])
            dspl_max_time = bot_util.display_hours_as_days(unit["max_time"])

            time = f"{dspl_curr_time}{' / '}{dspl_max_time}"
            display_list.append(time)

            # cost
            ## don't like this. What if change the key names in list_display_attributes? should probably make a key map in this file
            for remaining, max in [("remaining_elixir", "max_elixir"), ("remaining_dark_elixir", "max_dark_elixir"), ("remaining_gold", "max_gold")]:
                curr_cost = bot_util.display_large_number(unit[remaining])
                max_cost = bot_util.display_large_number(unit[max])

                cost = f"{curr_cost}{' / '}{max_cost}"
                display_list.append(cost)


            i = unit_order.index(unit["name"])
            display_lists[i] = display_list
        
        return display_lists
    
    @staticmethod
    def list_display_attributes(units: list, th_level: int) -> dict:
        """Extracts from units all the attributes needed to display, such as remaining level and max level.

        Args:
            units (list): List of Unit subtypes
            th_level (int): The level of the townhall used to determine max level of unit

        Returns:
            dict: _description_
        """
        dict_template = {"name": "", 
                            "remaining_level": 0, 
                            "max_level": 0, 
                            "remaining_time": 0, 
                            "max_time": 0,
                            "remaining_elixir": 0, 
                            "max_elixir": 0,
                            "remaining_dark_elixir": 0, 
                            "max_dark_elixir": 0,
                            "remaining_gold": 0,
                            "max_gold": 0}

        attribute_lists = []

        for unit in units:
            # disc to hold unit attributes used in display
            attribute_list = dict_template.copy()
            
            # name
            attribute_list["name"] = unit.name

            # level
            max_level = unit.get_max_level_th(th_level)
            rem_level = max(max_level - unit.curr_level, 0)

            attribute_list["remaining_level"] = rem_level
            attribute_list["max_level"] = max_level

            # time
            max_time = unit.get_upgrade_time(max_level)
            rem_time = max(max_time - unit.get_upgrade_time(unit.curr_level), 0)

            attribute_list["remaining_time"] = rem_time
            attribute_list["max_time"] = max_time

            # cost
            resource = unit.get_upgrade_resource()
            formatted_resource = "_".join(resource.lower().split(" "))
            remaining_cost_key = "remaining_" + formatted_resource
            remaining_max_key = "max_" + formatted_resource

            max_cost = unit.get_upgrade_cost(max_level)
            rem_cost = max(max_cost - unit.get_upgrade_cost(unit.curr_level), 0)

            attribute_list[remaining_cost_key] = rem_cost
            attribute_list[remaining_max_key] = max_cost

            attribute_lists.append(attribute_list)
        
        return attribute_lists

    
    @staticmethod
    def unit_is_available_th(production_building: str, th_level: int) -> bool:
        """Check whether a spell or troop can be available in the Forge / Barracks at th_level

        Returns:
            bool: A boolean value, true if unit is available at th_level
        """
        buildings = bot_util.load_json("assets/buildings.json")
        pb_th_levels = buildings[production_building]["TownHallLevel"]
        return any(th_level >= pb_th_level for pb_th_level in pb_th_levels)


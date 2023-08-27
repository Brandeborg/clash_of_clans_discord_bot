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
    def display_units(units: list, unit_order: list) -> list[list]:
        # create list the length of units, 
        # so units can be placed directly at indices, in the right order
        display_lists = [None] * len(unit_order)

        for unit in units:
            # list to hold unit attributes in a displayable manner
            # ex: ["name", "current level / max level", ...]
            display_list = []
            
            # name
            display_list.append(unit["name"])

            # level
            levels = f"{unit['current_level']} / {unit['max_level']}"
            display_list.append(levels)

            # time
            dspl_curr_time = bot_util.display_hours_as_days(unit["current_time"])
            dspl_max_time = bot_util.display_hours_as_days(unit["max_time"])

            time = f"{dspl_curr_time}{' / '}{dspl_max_time}"
            display_list.append(time)

            # cost
            ## don't like this. What if change the key names in list_display_attributes? should probably make a key map in this file
            for current, max in [("current_elixir", "max_elixir"), ("current_dark_elixir", "max_dark_elixir"), ("current_gold", "max_gold")]:
                curr_cost = bot_util.display_large_number(unit[current])
                max_cost = bot_util.display_large_number(unit[max])

                cost = f"{curr_cost}{' / '}{max_cost}"
                display_list.append(cost)


            i = unit_order.index(unit["name"])
            display_lists[i] = display_list
        
        return display_lists
    
    @staticmethod
    def list_display_attributes(units: list, th_level: int) -> dict:
        dict_template = {"name": "", 
                            "current_level": 0, 
                            "max_level": 0, 
                            "current_time": 0, 
                            "max_time": 0,
                            "current_elixir": 0, 
                            "max_elixir": 0,
                            "current_dark_elixir": 0, 
                            "max_dark_elixir": 0,
                            "current_gold": 0,
                            "max_gold": 0}
        totals = dict_template.copy()

        totals["name"] = "Total"
        attribute_lists = [totals]

        for unit in units:
            # disc to hold unit attributes used in display
            attribute_list = dict_template.copy()
            
            # name
            attribute_list["name"] = unit.name

            # level
            attribute_list["current_level"] = unit.curr_level
            attribute_lists[0]["current_level"] += attribute_list["current_level"]

            max_level = unit.get_max_level_th(th_level)
            attribute_list["max_level"] = max_level
            attribute_lists[0]["max_level"] += attribute_list["max_level"]

            # time
            curr_time = unit.get_upgrade_time(unit.curr_level)
            max_time = unit.get_upgrade_time(max_level)

            attribute_list["current_time"] = curr_time
            attribute_lists[0]["current_time"] += attribute_list["current_time"]

            attribute_list["max_time"] = max_time
            attribute_lists[0]["max_time"] += attribute_list["max_time"]

            # cost
            resource = unit.get_upgrade_resource()
            formatted_resource = "_".join(resource.lower().split(" "))
            current_cost_key = "current_" + formatted_resource
            current_max_key = "max_" + formatted_resource

            curr_cost = unit.get_upgrade_cost(unit.curr_level)
            max_cost = unit.get_upgrade_cost(max_level)

            attribute_list[current_cost_key] = curr_cost
            attribute_lists[0][current_cost_key] += attribute_list[current_cost_key]
            attribute_list[current_max_key] = max_cost
            attribute_lists[0][current_max_key] += attribute_list[current_max_key]

            attribute_lists.append(attribute_list)
        
        return attribute_lists

    
    @staticmethod
    def unit_is_available_th(production_building: str, th_level: int) -> bool:
        """Check whether a spell or troop can be available in the Forge / Barracks at th_level

        Returns:
            bool: A boolean value, true if unit is available at th_level
        """
        buildings = bot_util.load_json("../assets/buildings.json")
        pb_th_levels = buildings[production_building]["TownHallLevel"]
        return any(th_level >= pb_th_level for pb_th_level in pb_th_levels)


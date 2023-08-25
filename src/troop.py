from unit import Unit
import bot_util

class Troop(Unit):
    def __init__(self, curr_level, name, unit_static: dict) -> None:
        super().__init__(curr_level, name, unit_static)

        required_keys = ["LaboratoryLevel", "ProductionBuilding"]

        for key in required_keys:
            if key not in self.unit_static:
                raise Exception("unit_static does not contain required information. Should contain keys: ", required_keys)

    def get_max_level(self):
        """Deduce absolute max level of a hero by looking at the static data.

        Returns:
            int: max level
        """
        return len(self.unit_static["LaboratoryLevel"])
    
    def get_max_level_th(self, th_level: int):
        """Deduce the maximum troop level, at current th_level, from a list of "required townhall levels" of the form: 
        [9, 9, 9, 9, 9, 10, 10, 10, ...]. Assumes self.unit_static contains a ProductionBuilding and LaboratoryLevel key.

        Args:
            th_level (int): A player's current town hall level

        Returns:
            int: The max level of a given item (hero, building, etc.)
        """
        if not bot_util.troop_is_available_th(self.unit_static["ProductionBuilding"][0], th_level):
            return 0

        th2lab: dict = bot_util.get_th_lab_map()
        rq_lab_levels = self.unit_static["LaboratoryLevel"]
        if th2lab[th_level] < rq_lab_levels[1]:
            return 0
        return max(i+1 for i, rq_lab_level in enumerate(rq_lab_levels) if rq_lab_level <= th2lab[th_level])

    def get_upgrade_time(self, level: int) -> int:
        return super().get_upgrade_time(level, prefix="Upgrade")
    
    def get_upgrade_cost(self, level: int) -> int:
        return super().get_upgrade_cost(level, prefix="Upgrade")
    
    def get_upgrade_resource(self):
        return super().get_upgrade_resource(prefix="Upgrade")
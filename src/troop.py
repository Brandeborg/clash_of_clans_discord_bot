from unit import Unit
import bot_util

class Troop(Unit):
    def __init__(self, curr_level, name, unit_static: dict) -> None:
        super().__init__(curr_level, name, unit_static)

    def get_max_level(self):
        return len(self.unit_static["LaboratoryLevel"])
    
    def get_max_level_th(self, th_level: int):
        if not bot_util.troop_is_available_th(self.unit_static["ProductionBuilding"][0], th_level):
            return 0

        th2lab: dict = bot_util.get_th_lab_map()
        rq_lab_levels = self.unit_static["LaboratoryLevel"]
        if th2lab[th_level] < rq_lab_levels[1]:
            return 0
        return max(i+1 for i, rq_lab_level in enumerate(rq_lab_levels) if rq_lab_level <= th2lab[th_level])
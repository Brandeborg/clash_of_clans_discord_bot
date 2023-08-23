from unit import Unit

class Hero(Unit):
    def __init__(self, curr_level, name, unit_static: dict) -> None:
        super().__init__(curr_level, name, unit_static)

    def get_max_level(self):
        return len(self.unit_static["RequiredTownHallLevel"])

    def get_max_level_th(self, th_level: int):
        rq_th_levels = self.unit_static["RequiredTownHallLevel"]
        if self._th_level < rq_th_levels[0]:
            return 0
        return max(i+1 for i, rq_th_level in enumerate(rq_th_levels) if rq_th_level <= th_level)

    
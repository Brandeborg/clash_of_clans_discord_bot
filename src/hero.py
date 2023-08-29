from unit import Unit
import bot_util

class Hero(Unit):
    def __init__(self, curr_level, name, unit_static: dict) -> None:
        if "RequiredTownHallLevel" not in unit_static:
            raise Exception("unit_static does not contain required information. Should contain 'RequiredTownHallLevel' key.")
        
        super().__init__(curr_level, name, unit_static)

    def get_max_level(self) -> int:
        """Deducem absolute max level of a hero by looking at the static data.

        Returns:
            int: max level
        """
        return len(self.unit_static["RequiredTownHallLevel"])

    def get_max_level_th(self, th_level: int) -> int:
        """Deduce the maximum hero level, at current th_level, from a list of "required townhall levels" of the form: 
        [9, 9, 9, 9, 9, 10, 10, 10, ...]. Assumes self.unit_static contains a RequiredTownHallLevel key.

        Args:
            th_level (int): A player's current town hall level

        Returns:
            int: The max level of a given item (hero, building, etc.)
        """

        rq_th_levels = self.unit_static["RequiredTownHallLevel"]
        if th_level < rq_th_levels[0]:
            return 0
        return max(i+1 for i, rq_th_level in enumerate(rq_th_levels) if rq_th_level <= th_level)
    
    def get_upgrade_time(self, level: int) -> int:
        return super().get_upgrade_time(level, prefix="Upgrade")
    
    def get_upgrade_cost(self, level: int) -> int:
        return super().get_upgrade_cost(level, prefix="Upgrade")
    
    def get_upgrade_resource(self) -> str:
        return super().get_upgrade_resource(prefix="Upgrade")

    @staticmethod
    def create_hero_objects(translation: dict, unit_groups: dict, player: dict):
        heroes_static = bot_util.load_json("../assets/heroes.json")

        heroes = []
        for sc_name, hero_static in heroes_static.items():
            if "TID" not in hero_static: 
                continue
            
            name = translation[hero_static["TID"][0]][0] 
            if name not in unit_groups["home_heroes"]:
                continue

            hero_active = bot_util.search_unit(name, player["heroes"])
            if not hero_active:
                hero_active = {"level": 0}
            hero = Hero(curr_level=hero_active["level"], name=name, unit_static=hero_static)

            heroes.append(hero)

        return heroes
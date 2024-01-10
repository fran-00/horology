class Weapon:

    def __init__(self, name, damage):
        self.name = name
        self.damage = damage


class Melee(Weapon):

    def __init__(self, name, damage):
        super().__init__(name, damage)
    
    def weapon_type(self):
        return "melee"


class Ranged(Weapon):

    def __init__(self, name, damage):
        super().__init__(name, damage)

    def weapon_type(self):
        return "ranged"

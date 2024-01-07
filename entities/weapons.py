class Weapon:

    def __init__(self, name, damage):
        self.name = name
        self.damage = damage


class Melee(Weapon):

    def __init__(self, name, damage):
        super().__init__(name, damage)


class Ranged(Weapon):

    def __init__(self, name, damage):
        super().__init__(name, damage)

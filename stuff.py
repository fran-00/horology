
"""
Il piano è questo. Ci serve una classe "madre" chiamata WEAPON
e due sottoclassi "figlie" chiamate MELEE e CURSE.

Le due sottoclassi a loro volta devono contenere tutti gli oggetti che possono
essere raccolti nel layer "items" della mappa.


WEAPON (Object)
    > MELEE (Weapon)
        > Ramo corazzato(Melee)
        > Dito medio di galileo(Melee)
        > ...
    > CURSE (Weapon)
        > Sep(Curse)
        > Calulus(Curse)
        >...

Gli attributi sono gli stessi per tutti:
        self.id = numero intero usato nella mappa come proprietà dell'oggetto che serve a collegarlo a questa classe
        self.name = nome dell'oggetto
        self.description = descrizione dell'oggetto
        self.damage = danno causato ai nemici in battaglia dall'oggetto
        self.value = valore dell'oggetto per la vendita
        self.weight = peso dell'oggetto (ci sarà un limite di oggetti trasportabili)


"""


class Curse:
    def __init__(self):
        raise NotImplementedError("Do not create raw Curses objects")

class Sep(Curse):
    def __init__(self):
        self.id = 0
        self.name = "Somebody Else's Problem Field"
        self.description = "A SEP is something we can't see, or don't see, or our brain doesn't let us see, because we think that it's Somebody Else's Problem. The brain just edits it out, it's like a blind spot."
        self.damage = 60
        self.value = 150
        self.weight = 0

class Godel(Curse):
    def __init__(self):
        self.name = "Gödel's completeness theorem for first-order predicate calculus"
        self.description = "Every syntactically consistent, countable first-order theory has a finite or countable model. This establishes a correspondence between semantic truth and syntactic provability in first-order logic: Gödel proved that first order logic is semantically complete but it is not syntactically complete, since there are sentences expressible in the language of first order logic that can be neither proved nor disproved from the axioms of logic alone."
        self.damage = 10
        self.value = 20
        self.weight = 0

class Falsidical(Curse):
    def __init__(self):
        self.name = "falsidical paradox"
        self.description = "Packs a surprise, but it is seen as a false alarm when we solve the underlying fallacy. Good for Easy Enemies."
        self.damage = 65
        self.value = 100
        self.weight = 0
class Currency:
    def __init__(self, num):
        self.num = num
        self.value = (num, self.type)
        self.name = F"{num} {self.type}"


class gp(Currency):
    type = "gp"


class sp(Currency):
    type = "sp"


class cp(Currency):
    type = "cp"

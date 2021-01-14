from dataclasses import dataclass

@dataclass
class Parent:

    temperament: str = "Calm"
    cost_num: int = 0
    cost_type: str = "gp"


    def __post_init__(self):
        self.cost = (self.cost_num, self.cost_type)

    def test_func(self):
        print("Test sucessful")
        print(self.cost)

@dataclass
class Child(Parent):

    eyecolour: str = "Blue"

# @dataclass
# class Child(Parent):
#     pass
#
#
print(Child())

def def_x():
    global x
    x = 2

class Test:

    def __init__(self):
        self.test_func()

    def test_func(self):
        def_x()

class Second:


Test()
print(x)
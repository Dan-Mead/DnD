import inspect

class X:
    pass

x = X()

print(inspect.isclass(x))
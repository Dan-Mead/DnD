class Master:
    value = True

class Slave(Master):
    value = False


print(Slave.value)

class Test:
    test = True
    tribulation = False
    trial = ("test", "tribulation")


for t in Test.trial:
    print(t)
    print(getattr(Test, t))

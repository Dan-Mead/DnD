import pickle

name = "Ser Gorden Simpleton"

loc = f'saves/{name}.pkl'

file = open(loc, "rb")
info = pickle.load(file)
file.close()

print(info)

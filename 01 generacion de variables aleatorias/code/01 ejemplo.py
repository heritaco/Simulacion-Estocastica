import numpy as np


def h(u):
    return (b-a)*np.exp(a+(b-a)*u + (a+(b-a)*u)**2)


k = 1000
a = -2
b = 2
u = np.random.random(k)
h(u).mean()

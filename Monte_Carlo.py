import numpy as np
import math

#Integral to be evaluated
def f_x(x):
    return (1.0 / (x**2 + math.cos**2(x)))

n = 10000 #MC steps

#MONTE CARLO CRUDE IMPLEMENTATION
def crude_MC(n):
    upper_bound = math.pi
    lower_bound = 0
    sum_samples = 0

    for i in range(n):
        x = np.random.uniform(0,1)
        sum_samples += x

    return (upper_bound - lower_bound) * (sum_samples/n)

y = crude_MC(n)
print(y)

#MONTE CARLO CRUDE VARIANCE
def crude_MC_variance(n):
    up = math.pi
    low = 0
    samples = 0

    for i in range(n):
        x=np.random.uniform(0,1)
        samples += x**2
        sum = (up-low)*samples/n

    for i in range(n):
        x = np.random.uniform(0,1)
        samples += x
        sum_ave = (up-low)*(samples/n)**2

    return sum_ave - sum

z = crude_MC_variance(n)
print(z)

#MONTE CARLO CRUDE ERROR
def mc_error(n):
    return np.sqrt(z/n)

e = mc_error(n)
print(e)

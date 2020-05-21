import math
import numpy as np

def gauss(sigma):
''' Takes in sigmas as input. Gives two independent Gaussian random numbers obtained by sample transformation'''

    psi = np.random.uniform(0,2*math.pi)
    wf = -math.log(np.random.uniform(0,1))
    r = sigma * math.sqrt(2 * wf)
    x = r * math.cos(psi)
    y = r * math.sin(psi)
    return [x,y]

gauss(-1)

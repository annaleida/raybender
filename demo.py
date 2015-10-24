from numpy import *
from refraction import *

A = array([0.5, 1/sqrt(2), 0.5])
n0 = 1.0
n1 = 1.5
P = array([1.0,0.0,0.0])
Q = array([0.0,0.0,1.0])
ori = array([0.0,0.0,0.0])

returned = ComputeRefraction(n0, n1, P, Q, A, ori)
print 'Returned: ', returned

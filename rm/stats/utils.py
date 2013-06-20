"""
Utility functions for statistical calculations on Randomise Me
"""
import numpy as np
from statsmodels.stats.power import tt_ind_solve_power

def nobs(estimated=None, impressive=None):
    """
    Given the estimated and impressive figures,
    conduct a power calculation and return the
    number of required observations.

    Arguments:
    - `estimated`: int
    - `impressive`: int

    Return: int
    Exceptions: None
    """
    estimated, impressive = float(estimated), float(impressive)
    if abs(estimated/impressive) > 1:
        effect_size = abs(estimated/impressive)
    else:
        effect_size = abs(impressive/estimated)
    num = tt_ind_solve_power(effect_size=effect_size, alpha=0.05, power=0.8, nobs1=None)
    return int(num) * 2

def ttest(effect=None, alpha=None, power=None):
    num = tt_ind_solve_power(effect_size=effect, alpha=alpha, power=power, nobs1=None)
    return int(num) * 2

def sdiff(est, imp):
    diff = abs(est - imp)
    sd = 9.0/4.0
    sdiff = diff/sd
    return sdiff

def solve(eff):
    nobs = tt_ind_solve_power(effect_size=eff, alpha=0.05, power=0.8, nobs1=None)
    return int(nobs*2)

# From Sealed Envelope
def t(e, t):
     n = {.005: 2.576,
           .01: 2.326,
           .0125: 2.241,
           .025: 1.96,
           .05: 1.645,
           .1: 1.282,
           .15: 1.036,
           .2: .842,
           .25: .674,
           .3: .524,
           .4: .253,
           .5: 0
           }

     return np.power(n[e] + n[t], 2)

def binary_superiority(p1, p2, alpha, power):
    if p1 == p2:
        return "infinite"
    return int(np.ceil(t(alpha/2, power) * ((p1 * (100 - p1)) + (p2 * (100-p2 ))) / np.power(p1-p2, 2))) * 2

"""
Utility functions for statistical calculations on Randomise Me
"""
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

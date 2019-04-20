"""
Computes the scale factor on the probability distribution needed to yield a desired expected value of 95.025%
We use a root finder to solve the equation 100 * scale * EV = 95.025 for "scale", where EV is the 
expected return as a fraction of the total wagered
"""

import numpy as np
from cleoslots.slots_models import CleopatraModel
from scipy.optimize import root_scalar

desired_rtp = 0.95025


# We only include entries from index 1 and on because index 0 corresponds to losing (i.e. winning 0)
def expected(scale):
    cleo = CleopatraModel(nlines=1)
    avg = np.array([np.mean(x) for x in cleo.intervals[1:]])
    probs = scale * cleo.probabilities[1:]
    return np.sum(avg * probs) - desired_rtp


# For the line 1 model
cleopatra = CleopatraModel(nlines=1)

average = np.array([np.mean(x) for x in cleopatra.intervals[1:]])
probabilities = cleopatra.probabilities[1:]
print(probabilities)

# find the proper scale
proper_scale = root_scalar(expected, x0=.5, x1=.9).root
print('The proper scale is {}'.format(proper_scale))
probabilities *= proper_scale

expected_value = np.sum(average * probabilities)
print('The expected value of your return is {}'.format(expected_value))
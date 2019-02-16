import numpy as np
from slots_models import CleopatraModel
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import root_scalar

def expected(scale):
    cleo = CleopatraModel(nlines=1)
    intervals = cleo.intervals[1:]
    avg = np.array([np.mean(x) for x in intervals])
    probs = cleo.probabilities[1:]
    probs *= scale
    return np.sum(avg * probs) - .95025

cleo = CleopatraModel(nlines=1)
intervals = cleo.intervals[1:]
avg = np.array([np.mean(x) for x in intervals])
probs = cleo.probabilities[1:]
print(probs)

# find the proper scale
scale = root_scalar(expected, x0=.5, x1=.9).root
print('The proper scale is {}'.format(scale))
probs *= scale

expected_value = np.sum(avg * probs)
print('The expected value of your return is {}'.format(expected_value))
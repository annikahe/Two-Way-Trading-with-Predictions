import Simulations.offline as off

import numpy as np


def opt_off(exchange_rates):
    return off.monotonic_ends(exchange_rates)


def opt_off_distorted(exchange_rates, alpha, beta):
    pred_opt_off = opt_off(exchange_rates)

    choices = [-1, 0, 1]
    trans_prob = np.array([[alpha, beta, 1 - alpha - beta],  # probabilities to change somewhere from -1
                           [(1-alpha)/2, alpha, (1-alpha)/2],  # " " " from 0
                           [1 - alpha - beta, beta, alpha]])  # " " " from 1

    rng = np.random.default_rng()

    pred_distorted = []

    for pred in pred_opt_off:
        if pred == -1:
            pred_distorted.append(rng.choice(choices, p=trans_prob[0]))
        elif pred == 0:
            pred_distorted.append(rng.choice(choices, p=trans_prob[1]))
        else:
            pred_distorted.append(rng.choice(choices, p=trans_prob[2]))

    return pred_distorted


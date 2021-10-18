import offline as off

import numpy as np


def opt_off(exchange_rates):
    return off.monotonic_ends(exchange_rates)


def opt_off_distorted(exchange_rates):
    pred_opt_off = opt_off(exchange_rates)

    choices = [-1, 0, 1]
    trans_prob = np.array([[0.7,  0.2, 0.1 ],  # probabilities to change somewhere from -1
                           [0.15, 0.7, 0.15],  # " " " from 0
                           [0.1,  0.2, 0.7 ]])  # " " " from 1

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


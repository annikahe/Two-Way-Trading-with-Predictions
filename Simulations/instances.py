from numpy.random import default_rng
import numpy as np


def exchange_rates_uniform(phi, length):
    rng = default_rng()
    return rng.uniform(1, phi, length)


def exchange_rates_normal_from_last(phi, length, sigma):
    rng = default_rng()

    exchange_rates = []

    start = rng.uniform(1, phi)
    exchange_rates.append(start)

    for i in range(length):
        next = np.clip(rng.normal(exchange_rates[-1], sigma), 1, phi)
        exchange_rates.append(next)

    return exchange_rates


import algorithms as alg

import numpy as np


def monotonic_ends(input):
    input_tuples = zip(input, input[1:])
    inc_dec_list = [-1] + [1 if x <= y else -1 for (x, y) in input_tuples]  # compare two subsequent elements
    inc_dec_list_tuples = zip(inc_dec_list, inc_dec_list[1:])
    end_of_seq_list = [1 if x < y else (-1 if x > y else 0) for (x, y) in inc_dec_list_tuples] + [-1]

    return end_of_seq_list


def get_opt_off_return(exchange_rates):
    opt_pred = monotonic_ends(exchange_rates)
    off = alg.FtP(opt_pred)

    for e in exchange_rates:
        off.run(e)

    return off.payoff


def get_error_in_step(algo, off):
    if algo.x == off.x:
        return 0
    elif (algo.x == 0) or (off.x == 0):
        return 1
    else:
        return 2


def get_error(algo, exchange_rates):
    opt_pred = monotonic_ends(exchange_rates)
    off = alg.FtP(opt_pred)

    error = 0
    for e in exchange_rates:
        algo.run(e)
        off.run(e)
        error += get_error_in_step(algo, off)

    return error

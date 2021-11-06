import algorithms as alg

import numpy as np


def monotonic_ends(input):
    input_tuples = zip(input, input[1:])
    inc_dec_list = [-1] + [1 if x <= y else -1 for (x, y) in input_tuples]  # compare two subsequent elements
    inc_dec_list_tuples = zip(inc_dec_list, inc_dec_list[1:])
    end_of_seq_list = [1 if x < y else (-1 if x > y else 0) for (x, y) in inc_dec_list_tuples] + [-1]

    return end_of_seq_list

def monotonic_ends_indices(input):
    from itertools import compress
    input_tuples = zip(input, input[1:])
    inc_dec_list = [-1] + [1 if x <= y else -1 for (x, y) in input_tuples]  # compare two subsequent elements
    inc_dec_list_tuples = zip(inc_dec_list, inc_dec_list[1:])
    end_of_seq_list = [True if x != y else False for (x, y) in inc_dec_list_tuples] + [True]
    return [i for i, e in enumerate(end_of_seq_list) if e != 0]


def find_max_tuple(tuple_lists, input):
    max_gain = 0
    for i, inner_list in enumerate(tuple_lists):
        for j, tup in enumerate(inner_list):
            gain = input[tup[1]]/input[tup[0]]
            if gain > max_gain:
                max_gain = gain
                argmax_outer = i
                argmax_inner = j

    return argmax_outer, argmax_inner


def opt_bounded_k(input, k):
    I = [monotonic_ends_indices(input)]
    J = [[(a, b) for a in I[i] for b in I[i] if a <= b] for i in range(len(I))]
    M = [1]
    s = []

    for l in range(k+1):
        j, i = find_max_tuple(J, input)
        b_index = I[j].index(J[j][i][0])
        s_index = I[j].index(J[j][i][1])
        I = I[:j] + [I[j][:b_index]] + [I[j][b_index+1 : s_index]] + [I[j][s_index+1:]] + I[j+1:]
        J = J[:j] + [[(a, b) for a in I[j] for b in I[j] if a <= b]] + [[(a, b) for a in I[j+1] for b in I[j+1] if a <= b]] + [[(a, b) for a in I[j+2] for b in I[j+2] if a <= b]] + J[j+3:]

    return I, J


def get_opt_off_return(exchange_rates, k):
    if k == np.inf:
        opt_pred = monotonic_ends(exchange_rates)
    else:
        opt_pred = opt_bounded_k(exchange_rates, k) # TODO
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
